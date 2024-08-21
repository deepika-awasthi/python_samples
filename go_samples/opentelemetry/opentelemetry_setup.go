package telemetry

import (
	"context"
	"log"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
)

func InitializeGlobalTracerProvider() (*sdktrace.TracerProvider, error) {
	ctx := context.Background()

	// Initialize OTLP trace exporter
	clientOTel := otlptracegrpc.NewClient()
	exp, err := otlptrace.New(ctx, clientOTel)
	if err != nil {
		log.Fatalf("Failed to initialize exporter: %v", err)
	}

	// Initialize the tracer provider with the exporter
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exp),
		sdktrace.WithResource(resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName("temporal-example"),
			semconv.ServiceVersion("0.0.1"),
		)),
	)
	otel.SetTracerProvider(tp)

	otel.SetTextMapPropagator(
		propagation.NewCompositeTextMapPropagator(
			propagation.TraceContext{},
			propagation.Baggage{},
		),
	)

	return tp, nil
}
