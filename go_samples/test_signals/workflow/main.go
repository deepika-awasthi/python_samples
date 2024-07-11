// @@@SNIPSTART hello-world-project-template-go-start-workflow
package main

import (
	"test_signals/app"
	"context"
	"log"
	"go.temporal.io/sdk/client"
	
	"time"
)

func main() {

	// Create the client object just once per process
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("unable to create Temporal client", err)
	}
	defer c.Close()

	options := client.StartWorkflowOptions{
		ID:        "my-test-signal",
		TaskQueue: "test-signal-with-runtime-payload-queue",
		WorkflowExecutionTimeout: 5 * time.Minute,
		// WorkflowExecutionTimeout: time.Minute * 10, // Adjust the timeout as needed
		// WorkflowRunTimeout:       time.Minute * 5,  // Adjust the timeout as needed
		// WorkflowTaskTimeout:      time.Minute * 1,  // Adjust the timeout as needed
	}

	// Start the Workflow
	we, err := c.ExecuteWorkflow(context.Background(), options, app.NewWorkflowToTestSignal)
	if err != nil {
		log.Fatalln("Unable to execute workflow", err)
	}

	log.Println("Started workflow", "WorkflowID", we.GetID(), "RunID", we.GetRunID())

	log.Println("Sending signals")

	log.Printf("Started workflow %s\n", we.GetID())

	err = c.SignalWorkflow(context.Background(), we.GetID(), we.GetRunID(), "test-signal", nil)
		if err != nil {
			log.Fatalln("Unable to signals workflow", err)
		}
		log.Println("Sent " + "test-signal")
		time.Sleep(2 * time.Second)
}


// @@@SNIPEND
