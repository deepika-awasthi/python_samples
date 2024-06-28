// @@@SNIPSTART hello-world-project-template-go-start-workflow
package main

import (
	"context"
	"hello-world-temporal/app"
	"log"
	"go.temporal.io/sdk/client"
)

func main() {

	// Create the client object just once per process
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("unable to create Temporal client", err)
	}
	defer c.Close()

	options := client.StartWorkflowOptions{
		ID:        app.BuildOrderWorkflowID("R53J8X2KZ"),
		TaskQueue: app.GreetingTaskQueue,
	}

	// Start the Workflow
	// name := "World"
	we, err := c.ExecuteWorkflow(context.Background(), options, app.OrderWorkflow, "R53J8X2KZ")
	if err != nil {
		log.Fatalln("Unable to execute workflow", err)
	}

	log.Printf("Started workflow %s\n", we.GetID())
}


// @@@SNIPEND
