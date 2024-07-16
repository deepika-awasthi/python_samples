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
    log.Println("Starting ...")
    expected_id := "default-test-workflow-id"
    s.env.OnActivity(CtxActivity, mock.Anything).Return(func(ctx context.Context) (string, error) {
        my_id := ctx.Value(pass_test_key).(string)
        logMessage := "id " + my_id
        log.Println(logMessage)
        s.Equal(expected_id, my_id)
        return logMessage, nil
    }).Times(3)

    var res string
    s.env.ExecuteWorkflow(CtxWorkflow)

    s.True(s.env.IsWorkflowCompleted())
    s.NoError(s.env.GetWorkflowError())
    err := s.env.GetWorkflowResult(&res)
    s.NoError(err)

    log.Println("completed successfully with result:", res)
}

func TestUnitTestSuite(t *testing.T) {
    suite.Run(t, new(UnitTestSuite))
}
