package telemetry

import (
    "context"
    "fmt"
    "time"

    "go.temporal.io/sdk/contrib/opentelemetry"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/trace"
    "go.temporal.io/sdk/activity"
    "go.temporal.io/sdk/workflow"
    "go.temporal.io/sdk/interceptor"
)

var tracer = otel.Tracer("temporal-tracer")
const spanKey = "my-span-ctx-key"


func NewTracingInterceptor(spanContextKey string) (interceptor.Interceptor, error) {
    options := opentelemetry.TracerOptions{
        SpanContextKey: spanContextKey,
    }
    return opentelemetry.NewTracingInterceptor(options)
}

// Workflow is a sample Temporal workflow that processes signals.
func Workflow(ctx workflow.Context, name string) error {
    logger := workflow.GetLogger(ctx)
    logger.Info("Workflow started", "name", name)

    // Create a signal channel for the "my-signal" signal
    signalChan := workflow.GetSignalChannel(ctx, "my-signal")


    // Define a variable to hold the received signal data
    var signalData SignalData

    signalReceived := signalChan.Receive(ctx, &signalData)
    logger.Info("signalllllll ", signalReceived)
    if !signalReceived {
        return fmt.Errorf("failed to receive signal")
    }

    span, ok := ctx.Value(spanKey).(trace.Span)

    if signalData.Message == "test" {
    	logger.Info("handle signalllllll : workflowwwwwww ", signalReceived)

    	spanContext := span.SpanContext()
        traceID := spanContext.TraceID().String()
        spanID := spanContext.SpanID().String()
        logger.Info("When signal message is receivedddddd", "TraceID", traceID, "SpanID", spanID)

		signalSpanCtx := trace.ContextWithSpanContext(context.Background(), spanContext)

        _, signalSpan := tracer.Start(signalSpanCtx, "Signal-Handler", trace.WithAttributes(
            attribute.String("siganl", name),
            attribute.String("trace_id", traceID),
            attribute.String("span_id", spanID),
        ))
        defer signalSpan.End()
    }
    
    if ok {
        // Extract TraceID and SpanID from the span
        spanContext := span.SpanContext()
        traceID := spanContext.TraceID().String()
        spanID := spanContext.SpanID().String()
        logger.Info("Span found in context", "TraceID", traceID, "SpanID", spanID)

        // Create a new span within the existing trace context
        // ctx = context.WithValue(ctx, spanKey, span)
        workflowSpanCtx := trace.ContextWithSpanContext(context.Background(), spanContext)

        _, workflowSpan := tracer.Start(workflowSpanCtx, "Workflow-Span", trace.WithAttributes(
            attribute.String("workflow.name", name),
            attribute.String("trace_id", traceID),
            attribute.String("span_id", spanID),
        ))
        defer workflowSpan.End()

        // Set up activity options
        activityCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
            StartToCloseTimeout: 20 * time.Second,
        })

        signalData := SignalData{
            Message: "execute activity from workflow",
            TraceID: traceID,
            SpanID:  spanID,
        }

        // Execute activity with the message from the signal
        err := workflow.ExecuteActivity(activityCtx, Activity, signalData).Get(activityCtx, nil)
        if err != nil {
            logger.Error("Activity failed.", "Error", err)
            return err
        }
    } else {
        logger.Info("No span found in context")
    }

    logger.Info("Workflow completed.")
    return nil
}

// Activity is a sample Temporal activity that processes a signal.
func Activity(ctx context.Context, signalData SignalData) error {
    logger := activity.GetLogger(ctx)

    // Recreate the trace context from the received signal data
    traceID, err := trace.TraceIDFromHex(signalData.TraceID)
    if err != nil {
        return fmt.Errorf("failed to parse TraceID from signal data: %w", err)
    }
    spanID, err := trace.SpanIDFromHex(signalData.SpanID)
    if err != nil {
        return fmt.Errorf("failed to parse SpanID from signal data: %w", err)
    }
    spanContext := trace.NewSpanContext(trace.SpanContextConfig{
        TraceID: traceID,
        SpanID:  spanID,
        TraceFlags: trace.FlagsSampled,
    })

    activitySpanCtx := trace.ContextWithSpanContext(ctx, spanContext)

    // Start a new span within the existing trace context
    _, span := tracer.Start(activitySpanCtx, "Activity-Span", trace.WithAttributes(
        attribute.String("activity.message", signalData.Message),
    ))
    defer span.End()

    // Add attributes to the span
    span.SetAttributes(attribute.String("activity.message", signalData.Message))

    // Simulate some work
    time.Sleep(1 * time.Second)

    // Add an event to the span
    span.AddEvent("Activity completed")
    logger.Info("Activity completed")

    return nil
}
