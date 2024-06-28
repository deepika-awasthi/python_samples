package app

import (
    "context"
    "fmt"
    "go.temporal.io/sdk/client"
)

type WorkflowService struct {
    client client.Client
}

func NewWorkflowService(client client.Client) *WorkflowService {
    return &WorkflowService{client: client}
}

func BuildOrderWorkflowID(orderID string) string {
    return fmt.Sprintf("order-initiated-%s", orderID)
}

func (s *WorkflowService) QueryWorkflowState(ctx context.Context, orderID string) (WorkflowView, error) {
    workflowID := BuildOrderWorkflowID(orderID)

    resp, err := s.client.QueryWorkflow(ctx, workflowID, "", OrderWorkflowStateQuery)
    if err != nil {
        return WorkflowView{}, fmt.Errorf("error querying workflow %s: %+v", workflowID, err)
    }
    var result WorkflowView
    if err := resp.Get(&result); err != nil {
        return WorkflowView{}, fmt.Errorf("error recording workflow %s query result: %+v", workflowID, err)
    }
    return result, nil
}
