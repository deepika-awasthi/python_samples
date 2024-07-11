package app

import (
	// "context"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
	// "go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/testsuite"
	"github.com/stretchr/testify/mock"
)

// TestNewWorkflowToTestSignal tests the NewWorkflowToTestSignal workflow.
func TestNewWorkflowToTestSignal(t *testing.T) {
	suite := &testsuite.WorkflowTestSuite{}
	env := suite.NewTestWorkflowEnvironment()

	// Register the workflow and activities
	env.RegisterWorkflow(NewWorkflowToTestSignal)
	env.RegisterActivity(SomeActivity)

	// Mock the activity to return both result and error
	env.OnActivity(SomeActivity, mock.Anything, mock.Anything).Return("one", nil)

	// Register delayed callback to send the "do-activity" signal
	env.RegisterDelayedCallback(func() {
		env.SignalWorkflow("test-signal", "do-activity")
	}, time.Second*1)

	// Register delayed callback to send the "exit" signal
	env.RegisterDelayedCallback(func() {
		env.SignalWorkflow("test-signal", "exit")
	}, time.Second*3)

	// Start the workflow
	env.ExecuteWorkflow(NewWorkflowToTestSignal)

	// Wait for the workflow to complete
	var result string
	err := env.GetWorkflowResult(&result)

	// Assert that the workflow completed successfully
	require.True(t, env.IsWorkflowCompleted())
	require.NoError(t, err)
	require.NoError(t, env.GetWorkflowError())
}
