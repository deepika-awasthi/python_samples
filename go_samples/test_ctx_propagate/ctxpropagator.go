package app

import (
    "context"
    "log"

    "go.temporal.io/sdk/converter"
    "go.temporal.io/sdk/workflow"
)

type my_key string

const pass_test_key my_key = "trace_id"

type CustomContextPropagator struct{}

func (t *CustomContextPropagator) Inject(ctx context.Context, writer workflow.HeaderWriter) error {
    value := ctx.Value(pass_test_key)
    if value != nil {
        payload, err := converter.GetDefaultDataConverter().ToPayload(value)
        if err != nil {
            log.Printf("Inject: Error converting context value to payload: %v", err)
            return err
        }
        writer.Set(string(pass_test_key), payload)
        log.Printf("Inject: Trace ID injected into header: %s", value)
    }
    return nil
}

func (t *CustomContextPropagator) Extract(ctx context.Context, reader workflow.HeaderReader) (context.Context, error) {
    if payload, ok := reader.Get(string(pass_test_key)); ok {
        var my_id string
        if err := converter.GetDefaultDataConverter().FromPayload(payload, &my_id); err == nil {
            ctx = context.WithValue(ctx, pass_test_key, my_id)
            log.Printf("Extract: Trace ID extracted from header: %s", my_id)
        } else {
            log.Printf("Extract: Error converting payload to context value: %v", err)
            return ctx, err
        }
    }
    return ctx, nil
}

func (t *CustomContextPropagator) InjectFromWorkflow(ctx workflow.Context, writer workflow.HeaderWriter) error {
    value := ctx.Value(pass_test_key)
    if value != nil {
        payload, err := converter.GetDefaultDataConverter().ToPayload(value)
        if err != nil {
            log.Printf("InjectFromWorkflow: Error converting context value to payload: %v", err)
            return err
        }
        writer.Set(string(pass_test_key), payload)
        log.Printf("InjectFromWorkflow: Trace ID injected into header: %s", value)
    }
    return nil
}

func (t *CustomContextPropagator) ExtractToWorkflow(ctx workflow.Context, reader workflow.HeaderReader) (workflow.Context, error) {
    if payload, ok := reader.Get(string(pass_test_key)); ok {
        var my_id string
        if err := converter.GetDefaultDataConverter().FromPayload(payload, &my_id); err == nil {
            ctx = workflow.WithValue(ctx, pass_test_key, my_id)
            log.Printf("ExtractToWorkflow: Trace ID extracted from header: %s", my_id)
        } else {
            log.Printf("ExtractToWorkflow: Error converting payload to context value: %v", err)
            return ctx, err
        }
    }
    return ctx, nil
}
