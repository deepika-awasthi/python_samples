package app

import (
    "testing"
    "time"

    "github.com/stretchr/testify/require"
    "go.temporal.io/sdk/testsuite"
)

func Test_OrderWorkflow(t *testing.T) {
    ts := &testsuite.WorkflowTestSuite{}
    env := ts.NewTestWorkflowEnvironment()

    w := false
    env.RegisterDelayedCallback(func() {
        queryAndVerify(t, env, WorkflowView{
            OrderID:  "Orders",
            ClientID: 1234,
            State: OrderWorkflowState{
                Error:    nil,
                Complete: false,
                LIC:      nil,
                Releases: nil,
            },
        })
        w = true
    }, time.Minute*1)

    env.ExecuteWorkflow(OrderWorkflow, "Orders")
    require.True(t, env.IsWorkflowCompleted())
    require.NoError(t, env.GetWorkflowError())
    require.True(t, w, "state at timer not verified")
    queryAndVerify(t, env, WorkflowView{
        OrderID:  "Orders",
        ClientID: 1234,
        State: OrderWorkflowState{
            Error:    nil,
            Complete: false,
            LIC:      nil,
            Releases: nil,
        },
    })
}

func queryAndVerify(t *testing.T, env *testsuite.TestWorkflowEnvironment, expectedState WorkflowView) {
    result, err := env.QueryWorkflow(OrderWorkflowStateQuery)
    require.NoError(t, err)
    var state WorkflowView
    err = result.Get(&state)
    require.NoError(t, err)
    require.Equal(t, expectedState, state)
}
