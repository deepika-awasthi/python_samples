package app

import (
    "context"
    "log"
)

func CtxActivity(ctx context.Context) (string, error) {
    payload_id := ctx.Value(pass_test_key).(string)
    logMessage := "Trace ID in Activity: " + payload_id
    log.Println(payload_id)
    return logMessage, nil
}
