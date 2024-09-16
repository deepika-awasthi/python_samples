from dataclasses import asdict, is_dataclass
from typing import Any, Optional, Type, Union

from temporalio import activity, workflow
from temporalio.worker import (
    ActivityInboundInterceptor,
    ExecuteActivityInput,
    ExecuteWorkflowInput,
    Interceptor,
    WorkflowInboundInterceptor,
    WorkflowInterceptorClassInput,
)

with workflow.unsafe.imports_passed_through():
    import sentry_sdk
    from sentry_sdk import Hub, capture_exception, set_context, set_tag

# Activity Inbound Interceptor
class _SentryActivityInboundInterceptor(ActivityInboundInterceptor):
    def __init__(  # pylint: disable=redefined-builtin
        self,
        next: ActivityInboundInterceptor,
        error_deny_list: list[Type[Exception]] | None = None,
    ) -> None:
        super().__init__(next)
        self.error_deny_list = error_deny_list if error_deny_list is not None else []

    async def execute_activity(
        self, input: ExecuteActivityInput  # pylint: disable=redefined-builtin
    ) -> Any:
        with sentry_sdk.isolation_scope() as scope:

            activity_info = activity.info()

            # add contextual info
            scope.set_tag("temporal.type", "activity")
            scope.set_tag("temporal.task_queue", activity_info.task_queue)
            scope.set_tag("temporal.namespace", activity_info.workflow_namespace)

            # add workflow info
            scope.set_tag("temporal.workflow.id", activity_info.workflow_id)
            scope.set_tag("temporal.workflow.run_id", activity_info.workflow_run_id)
            scope.set_tag("temporal.workflow.type", activity_info.workflow_type)

            # add activity info
            scope.set_tag("temporal.activity.id", activity_info.activity_id)
            scope.set_tag("temporal.activity.type", activity_info.activity_type)

            try:
                return await super().execute_activity(input)
            except Exception as err:
                if not any(
                    isinstance(err, ignore_error)
                    for ignore_error in self.error_deny_list
                ):
                    set_context("temporal.activity.info", activity.info().__dict__)
                    capture_exception()
                raise err

# Workflow Inbound Interceptor
class _SentryWorkflowInterceptor(WorkflowInboundInterceptor):
    WORKFLOW_DENY_LIST_EXTERN_FUNCTION_NAME = "__sentry_workflow_interceptor_error_deny_list"

    def __init__(  # pylint: disable=redefined-builtin
        self,
        next: WorkflowInboundInterceptor,
        error_deny_list: list[Type[Exception]] | None = None,
    ) -> None:
        super().__init__(next)
        extern_deny_func = workflow.extern_functions().get(
            self.WORKFLOW_DENY_LIST_EXTERN_FUNCTION_NAME, lambda: []
        )
        self.error_deny_list = (
            error_deny_list if error_deny_list is not None else extern_deny_func()
        )

    async def execute_workflow(self, input: ExecuteWorkflowInput) -> Any:
        # https://docs.sentry.io/platforms/python/troubleshooting/#addressing-concurrency-issues
        with sentry_sdk.isolation_scope() as scope:
            workflow_info = workflow.info()

            # add contextual info
            scope.set_tag("temporal.type", "workflow")
            scope.set_tag("temporal.task_queue", workflow_info.task_queue)
            scope.set_tag("temporal.namespace", workflow_info.namespace)

            # add workflow info
            scope.set_tag("temporal.workflow.id", workflow_info.workflow_id)
            scope.set_tag("temporal.workflow.run_id", workflow_info.run_id)
            scope.set_tag("temporal.workflow.type", workflow_info.workflow_type)
            try:
                return await super().execute_workflow(input)
            except Exception as err:
                if not any(
                    isinstance(err, ignore_error)
                    for ignore_error in self.error_deny_list
                ):
                    set_context("temporal.workflow.info", workflow.info().__dict__)
                    if not workflow.unsafe.is_replaying():
                        with workflow.unsafe.sandbox_unrestricted():
                            capture_exception()
                raise err

# Sentry Interceptor
class SentryInterceptor(Interceptor):
    """Temporal Interceptor class which will report workflow & activity exceptions to Sentry"""

    def __init__(
        self,
        activity_error_deny_list: list[Type[Exception]],
        workflow_error_deny_list: list[Type[Exception]],
    ) -> None:
        self.activity_error_deny_list = activity_error_deny_list
        self.workflow_error_deny_list = workflow_error_deny_list

    def intercept_activity(
        self, next: ActivityInboundInterceptor
    ) -> ActivityInboundInterceptor:
        return _SentryActivityInboundInterceptor(
            super().intercept_activity(next),
            self.activity_error_deny_list,
        )

    def workflow_interceptor_class(
        self, input: WorkflowInterceptorClassInput
    ) -> Optional[Type[WorkflowInboundInterceptor]]:
        # Inject the deny-list into each instance of _SentryWorkflowInterceptor
        sentry_workflow_interceptor_functions = {
            _SentryWorkflowInterceptor.WORKFLOW_DENY_LIST_EXTERN_FUNCTION_NAME: lambda: self.workflow_error_deny_list
        }
        input.unsafe_extern_functions.update(**sentry_workflow_interceptor_functions)
        return _SentryWorkflowInterceptor
