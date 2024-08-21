package main

import (
	"context"
	"log"
	"time"

	"telemetry" // Your package where SignalData and InitializeGlobalTracerProvider are defined
	"go.temporal.io/sdk/client"
	"go.opentelemetry.io/otel/trace"
)

func main() {
	// Create a context with cancel
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Initialize the global tracer provider
	tp, err := telemetry.InitializeGlobalTracerProvider()
	if err != nil {
		log.Fatalf("Unable to create a global trace provider: %v", err)
	}
	defer func() {
		if err := tp.Shutdown(ctx); err != nil {
			log.Printf("Error shutting down trace provider: %v", err)
		}
	}()

	// Create Temporal client
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalf("Unable to create client: %v", err)
	}
	defer c.Close()

	// Define workflow options
	workflowOptions := client.StartWorkflowOptions{
		ID:        "otel_workflowID",
		TaskQueue: "opentelemetry",
	}

	// Execute the workflow
	we, err := c.ExecuteWorkflow(ctx, workflowOptions, telemetry.Workflow, "Temporal")
	if err != nil {
		log.Fatalf("Unable to execute workflow: %v", err)
	}

	log.Printf("Started workflow: WorkflowID=%s, RunID=%s", we.GetID(), we.GetRunID())

	// Wait for a while before sending the signal
	time.Sleep(10 * time.Second)

	// Extract the current span from the context
	span := trace.SpanFromContext(ctx)
	if span == nil {
		log.Fatal("No span found in context")
	}

	// Extract trace and span IDs
	spanContext := span.SpanContext()
	traceID := spanContext.TraceID().String()
	spanID := spanContext.SpanID().String()

	// Log trace information
	log.Printf("Extracted TraceID: %s, SpanID: %s", traceID, spanID)

	// Create SignalData with trace context
	signalData := telemetry.SignalData{
		Message: "test",
		TraceID: traceID,
		SpanID:  spanID,
	}

	// Log signal data
	log.Printf("SIGNAL data: %+v", signalData)

	// Send a signal to the workflow with trace context
	err = c.SignalWorkflow(ctx, we.GetID(), we.GetRunID(), "my-signal", signalData)
	if err != nil {
		log.Fatalf("Unable to send signal: %v", err)
	}

	// Log that the signal was sent
	log.Printf("Signal sent: %+v", signalData)

	// Retrieve and log the workflow result
	var result string
	err = we.Get(ctx, &result)
	if err != nil {
		log.Fatalf("Unable to get workflow result: %v", err)
	}
	log.Printf("Workflow result: %s", result)
}
