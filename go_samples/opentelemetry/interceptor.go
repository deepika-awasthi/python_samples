package telemetry

import (
	"context"
	"go.temporal.io/sdk/interceptor"
	"go.temporal.io/sdk/log"
	"go.temporal.io/sdk/workflow"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/trace"
	"go.opentelemetry.io/otel/attribute"
	"encoding/hex"
	"encoding/json"
	"fmt"
)


type SignalData struct {
	Message string `json:"message"`
	TraceID string `json:"trace_id"`
	SpanID  string `json:"span_id"`
}


// Custom worker interceptor
type workerInterceptor struct {
	interceptor.WorkerInterceptorBase
	tracer trace.Tracer
}

func NewWorkerInterceptor() interceptor.WorkerInterceptor {
	return &workerInterceptor{
		tracer: otel.Tracer("temporal-tracer"),
	}
}

func (w *workerInterceptor) InterceptActivity(
	ctx context.Context,
	next interceptor.ActivityInboundInterceptor,
) interceptor.ActivityInboundInterceptor {
	i := &activityInboundInterceptor{root: w}
	i.Next = next
	return i
}

type activityInboundInterceptor struct {
	interceptor.ActivityInboundInterceptorBase
	root *workerInterceptor
}

func (a *activityInboundInterceptor) Init(outbound interceptor.ActivityOutboundInterceptor) error {
	i := &activityOutboundInterceptor{root: a.root}
	i.Next = outbound
	return a.Next.Init(i)
}

type activityOutboundInterceptor struct {
	interceptor.ActivityOutboundInterceptorBase
	root *workerInterceptor
}

func (a *activityOutboundInterceptor) GetLogger(ctx context.Context) log.Logger {
	logger := a.Next.GetLogger(ctx)
	return logger
}

func (w *workerInterceptor) InterceptWorkflow(
	ctx workflow.Context,
	next interceptor.WorkflowInboundInterceptor,
) interceptor.WorkflowInboundInterceptor {
	i := &workflowInboundInterceptor{root: w}
	i.Next = next
	return i
}

type workflowInboundInterceptor struct {
	interceptor.WorkflowInboundInterceptorBase
	root *workerInterceptor
}

func (w *workflowInboundInterceptor) Init(outbound interceptor.WorkflowOutboundInterceptor) error {
	i := &workflowOutboundInterceptor{root: w.root}
	i.Next = outbound
	return w.Next.Init(i)
}

type workflowOutboundInterceptor struct {
	interceptor.WorkflowOutboundInterceptorBase
	root *workerInterceptor
}


// // Implement the WorkflowInboundInterceptor interface
// func (w *workflowInboundInterceptor) ExecuteWorkflow(
// 	ctx workflow.Context,
// 	in *interceptor.ExecuteWorkflowInput,
// ) (interface{}, error) {
// 	// Start a new span for workflow execution
// 	logger := workflow.GetLogger(ctx)
// 	span, ok := ctx.Value(spanKey).(trace.Span)
// 	if ok {
// 		spanContext := span.SpanContext()
//         traceID := spanContext.TraceID().String()
//         spanID := spanContext.SpanID().String()
//         logger.Info("Span found in context", "TraceID", traceID, "SpanID", spanID)
// 	}
// 	defer span.End()

// 	// Continue with the workflow execution
// 	return w.Next.ExecuteWorkflow(ctx, in)
// }


func (w *workflowInboundInterceptor) HandleSignal(
	ctx workflow.Context,
	in *interceptor.HandleSignalInput,
) error {
	// Create a new span using Temporal's context

	// span, ok := ctx.Value(spanKey).(trace.Span)

	// if ok {

		// only pulling infos from async signal context, no info about workflow span
		// spanContext := span.SpanContext()

		// signalSpanCtx := trace.ContextWithSpanContext(context.Background(), spanContext)
		// traceID := spanContext.TraceID().String()
		// spanID := spanContext.SpanID().String()


		// _, signalSpan := tracer.Start(signalSpanCtx, "Signal-Span", trace.WithAttributes(
        //     attribute.String("workflow.name", "name"),
        //     attribute.String("trace_id", traceID),
        //     attribute.String("span_id", spanID),
        // ))
		// defer signalSpan.End()


	// }

	
	// Continue with handling the signal
	// return w.Next.HandleSignal(ctx, in)


	// Extract SignalData from the signal input
	// Extract SignalData from the signal input
	var signalData SignalData
	if in.Arg != nil {
		for _, payload := range in.Arg.Payloads {
			var data SignalData
			if err := json.Unmarshal(payload.Data, &data); err != nil {
				return fmt.Errorf("failed to unmarshal payload data: %w", err)
			}
			signalData = data
		}
	}

	// Create a new span using Temporal's context
	span, ok := ctx.Value(spanKey).(trace.Span)
	if ok {
		spanContext := span.SpanContext()
		ctxWithSpan := trace.ContextWithSpanContext(context.Background(), spanContext)

		_, signalSpan := w.root.tracer.Start(ctxWithSpan, "Signal-Handler", trace.WithAttributes(
			attribute.String("workflow.name", "name"),
			attribute.String("trace_id", signalData.TraceID),
			attribute.String("span_id", signalData.SpanID),
		))
		defer signalSpan.End()
	}

	// Continue with handling the signal
	return w.Next.HandleSignal(ctx, in)
}


// Convert traceID from string to TraceID
func traceIDFromString(id string) (trace.TraceID, error) {
	var traceID trace.TraceID
	idBytes, err := hex.DecodeString(id)
	if err != nil {
		return traceID, err
	}
	copy(traceID[:], idBytes)
	return traceID, nil
}

// Convert spanID from string to SpanID
func spanIDFromString(id string) (trace.SpanID, error) {
	var spanID trace.SpanID
	idBytes, err := hex.DecodeString(id)
	if err != nil {
		return spanID, err
	}
	copy(spanID[:], idBytes)
	return spanID, nil
}