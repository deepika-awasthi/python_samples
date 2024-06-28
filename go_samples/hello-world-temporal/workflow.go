package app

import (
    "go.temporal.io/sdk/workflow"
    "time"
)

// func GreetingWorkflow(ctx workflow.Context, name string) (string, error) {
//     options := workflow.ActivityOptions{
//         StartToCloseTimeout: time.Second * 5,
//     }

//     ctx = workflow.WithActivityOptions(ctx, options)

//     var result string
//     err := workflow.ExecuteActivity(ctx, ComposeGreeting, name).Get(ctx, &result)

//     return result, err
// }


const OrderWorkflowStateQuery = "OrderWorkflowStateQuery"

type WorkflowView struct {
    OrderID  string
    ClientID int
    State    OrderWorkflowState
    App    *App
}

type OrderWorkflowState struct {
    Error    error
    Complete bool
    LIC      *string
    Releases []string
}

type App struct {
    ID string
}

func OrderWorkflow(ctx workflow.Context, orderID string) error {

    workflow.SetQueryHandler(ctx, OrderWorkflowStateQuery, func() (WorkflowView, error) {
        return WorkflowView{
            OrderID:  orderID,
            ClientID: 1234,
            State: OrderWorkflowState{
                Error:    nil,
                Complete: false,
                LIC:      nil,
                Releases: nil,
            },
        }, nil
    })

    // Simulate some work
    workflow.Sleep(ctx, 1*time.Minute)
    return nil
}