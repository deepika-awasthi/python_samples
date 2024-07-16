package app

import (
    "log"
    "time"

    "go.temporal.io/sdk/workflow"
)

func CtxWorkflow(ctx workflow.Context) (string, error) {
    log.Println("Starting...")

    // Extract the ID from the workflow context
    wk_id := workflow.GetInfo(ctx).WorkflowExecution.ID
    log.Printf("Trace ID set in workflow context: %s", wk_id)

    ctx = workflow.WithValue(ctx, pass_test_key, wk_id)

    // Define activity options
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: time.Second * 10,
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    // Execute the activity
    var result string
    err := workflow.ExecuteActivity(ctx, CtxActivity).Get(ctx, &result)
    if err != nil {
        log.Printf("Error executing activity: %v", err)
        return "", err
    }

    log.Printf("completed successfully with result: %s", result)
    return result, nil
}