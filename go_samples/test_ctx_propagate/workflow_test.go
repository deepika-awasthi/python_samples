package app

import (
    "context"
    "log"
    "testing"

    "github.com/stretchr/testify/mock"
    "github.com/stretchr/testify/suite"
    "go.temporal.io/sdk/testsuite"
    "go.temporal.io/sdk/workflow"
)

type UnitTestSuite struct {
    suite.Suite
    testSuite *testsuite.WorkflowTestSuite
    env       *testsuite.TestWorkflowEnvironment
}

func (s *UnitTestSuite) SetupTest() {
    log.Println("Setting up UnitTestSuite...")
    s.testSuite = &testsuite.WorkflowTestSuite{}
    s.env = s.testSuite.NewTestWorkflowEnvironment()
    s.env.SetContextPropagators([]workflow.ContextPropagator{&CustomContextPropagator{}})
    s.env.RegisterWorkflow(CtxWorkflow)
    s.env.RegisterActivity(CtxActivity)
    log.Println("UnitTestSuite setup complete")
}

func (s *UnitTestSuite) TestCtxWorkflow() {
    log.Println("Starting TestSampleWorkflow...")
    expectedTraceID := "default-test-workflow-id"
    s.env.OnActivity(CtxActivity, mock.Anything).Return(func(ctx context.Context) (string, error) {
        traceID := ctx.Value(pass_test_key).(string)
        logMessage := "TestSampleWorkflow: Trace ID in Activity: " + traceID
        log.Println(logMessage)
        s.Equal(expectedTraceID, traceID)
        return logMessage, nil
    }).Times(3) // Allowing for up to 3 retries

    var workflowResult string
    s.env.ExecuteWorkflow(CtxWorkflow)

    s.True(s.env.IsWorkflowCompleted())
    s.NoError(s.env.GetWorkflowError())
    err := s.env.GetWorkflowResult(&workflowResult)
    s.NoError(err)

    log.Println("TestSampleWorkflow completed successfully with result:", workflowResult)
}

func TestUnitTestSuite(t *testing.T) {
    suite.Run(t, new(UnitTestSuite))
}
