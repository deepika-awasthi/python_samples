package main

import (
	"context"
	"log"
	// "time"

	"go.temporal.io/sdk/client"
	"hello-world-temporal/app" // Import your workflow package
)

func main() {
	// Create Temporal client
	c, err := client.NewClient(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create Temporal client", err)
	}
	defer c.Close()

	// Define workflow execution options
	workflowOptions := client.StartWorkflowOptions{
		ID:        "test-selector-workflow",
		TaskQueue: "test-selector-task-queue", // Task queue where workers are listening
	}

	// Start workflow
	args := app.TestSelectorArgs{
		List: []string{"item1", "item2", "item3", "item4", "item5", "item6", "item7"},
	}
	we, err := c.ExecuteWorkflow(context.Background(), workflowOptions, app.TestSelector, args)
	if err != nil {
		log.Fatalln("Unable to start workflow execution", err)
	}

	// Wait for workflow result
	var result []string
	err = we.Get(context.Background(), &result)
	if err != nil {
		log.Fatalln("Unable to get workflow result", err)
	}

	log.Println("Workflow result:", result)
}
