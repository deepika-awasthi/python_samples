package app

import (
	"go.temporal.io/sdk/workflow"
	"time"
	"context"
	"go.temporal.io/sdk/activity"
	// "go.temporal.io/sdk/temporal"
)
	

func NewWorkflowToTestSignal(ctx workflow.Context) (string, error){
	// logger := workflow.GetLogger(ctx)

	// create a signal channel

	ch := workflow.GetSignalChannel(ctx, "test-signal")

	for {
		var signal string
		ch.Receive(ctx, &signal)

		switch signal {
		case "do-activity":
			ao := workflow.ActivityOptions{
				StartToCloseTimeout: time.Minute,
			}
			ctx = workflow.WithActivityOptions(ctx, ao)
			var result string
			err := workflow.ExecuteActivity(ctx, SomeActivity, "param").Get(ctx, &result)
			if err != nil {
				return "", err
			}
			workflow.GetLogger(ctx).Info("Activity result", "result", result)
		case "exit":
			return "workflow completed", nil
		}

		// if signal == "do-activity" {
		// 	workflow.GetLogger(ctx).Info("Changing workflow v1 running activity")
		// 	ao := workflow.ActivityOptions{
		// 		StartToCloseTimeout: 1 * time.Minute,
		// 		// RetryPolicy:            &temporal.RetryPolicy{MaximumAttempts: 2},
		// 	}
		// 	ctx := workflow.WithActivityOptions(ctx, ao)

		// 	var result string

		// 	err := workflow.ExecuteActivity(ctx, SomeActivity, "v1").Get(ctx1, &result)
		// 	if err != nil {
		// 		return err
		// 	}
		// } else {
		// 	workflow.GetLogger(ctx).Info("Activity result", "result", result)
		// 	return nil
		// }
	}

	// for{
	// 	var value string
	// 	ch.Receive(ctx, &value)
	// 	logger.Info("Received signal", "value", value)
	// 	if value == "exit"{
	// 		break
	// 	}
	// 	else {
	// 		workflow.GetLogger(ctx).Info("Concluding workflow v1b")
	// 		break
	// 	}
	// }

	// logger.Info("Workflow completed")

	// return nil
}


func SomeActivity(ctx context.Context, calledBy string) (string, error) {
	activity.GetLogger(ctx).Info("SomeActivity executing", "called by", calledBy)
	return calledBy, nil
}