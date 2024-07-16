package main

import (
    "context"
    "log"
    "test_ctx_propagate/app"
    "go.temporal.io/sdk/client"
)

func main() {
    // Create a new Temporal client
    c, err := client.NewClient(client.Options{})
    if err != nil {
        log.Fatalln("Unable to create client", err)
    }
    defer c.Close()

    // Start a workflow
    options := client.StartWorkflowOptions{
        ID:        "ctx_workflow",
        TaskQueue: "ctx-task-queue",
    }

    we, err := c.ExecuteWorkflow(context.Background(), options, app.CtxWorkflow)
    if err != nil {
        log.Fatalln("Unable to execute workflow", err)
    }

    log.Printf("Started workflow with ID: %s, RunID: %s", we.GetID(), we.GetRunID())

    // Wait for workflow to complete (optional)
    var result string
    err = we.Get(context.Background(), &result)
    if err != nil {
        log.Fatalln("Unable to get workflow result", err)
    }

    log.Printf("Workflow result: %s", result)
}
