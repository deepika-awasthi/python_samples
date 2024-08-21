package main

import (
	"context"
	"log"

	"telemetry"
	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"go.temporal.io/sdk/interceptor"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	tp, err := telemetry.InitializeGlobalTracerProvider()
	if err != nil {
		log.Fatalln("Unable to create a global trace provider", err)
	}

	defer func() {
		if err := tp.Shutdown(ctx); err != nil {
			log.Println("Error shutting down trace provider:", err)
		}
	}()

	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()

	// Create a new tracing interceptor
	tracingInterceptor, err := telemetry.NewTracingInterceptor("my-span-ctx-key")
	if err != nil {
		log.Fatalf("unable to create tracing interceptor: %v", err)
	}

	customInterceptor := telemetry.NewWorkerInterceptor()

	// Create a worker
	w := worker.New(c, "opentelemetry", worker.Options{
		Interceptors: []interceptor.WorkerInterceptor{tracingInterceptor,
	customInterceptor,},
	})

    w.RegisterWorkflow(telemetry.Workflow)
    w.RegisterActivity(telemetry.Activity)

    err = w.Run(worker.InterruptCh())
    if err != nil {
        log.Fatalln("Worker run failed", err)
    }
}
