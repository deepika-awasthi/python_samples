// @@@SNIPSTART hello-world-project-template-go-worker
package main

import (
	"log"

	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"hello-world-temporal/app" // Import your workflow package
)

func main() {
	// Create Temporal client
	c, err := client.NewClient(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create Temporal client", err)
	}
	defer c.Close()

	// Create a worker to listen on the task queue
	w := worker.New(c, "test-selector-task-queue", worker.Options{})

	// Register the workflow and activity
	w.RegisterWorkflow(app.TestSelector)
	w.RegisterActivity(app.Test1)

	// Start the worker
	err = w.Run(worker.InterruptCh())
	if err != nil {
		log.Fatalln("Unable to start worker", err)
	}
}
