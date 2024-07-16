package main

import (
    "log"

    "test_ctx_propagate/app"
    "go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"
    "go.temporal.io/sdk/workflow"
)

func main() {

    log.Println("Starting worker...")

    // Create a new Temporal client
    c, err := client.Dial(client.Options{
        HostPort:           client.DefaultHostPort,
        ContextPropagators: []workflow.ContextPropagator{&app.CustomContextPropagator{}},
    })
    if err != nil {
        log.Fatalln("Unable to create client", err)
    }
    defer c.Close()

    // Create a new worker that listens on the "sample-task-queue"
    w := worker.New(c, "ctx-task-queue", worker.Options{
         EnableLoggingInReplay: true,
    })

    log.Println("Worker created")

    // Register the workflow and activity with the worker
    w.RegisterWorkflow(app.CtxWorkflow)
    w.RegisterActivity(app.CtxActivity)


    log.Println("Registered workflow and activities")
    // Start the worker
    err = w.Run(worker.InterruptCh())
    if err != nil {
        log.Fatalln("Unable to start worker", err)
    }

    log.Println("Worker started")
}
