package app

import (
    "context"
    "time"

    "go.temporal.io/sdk/workflow"
)

type TestSelectorArgs struct {
    List []string
}

func TestSelector(ctx workflow.Context, args TestSelectorArgs) ([]string, error) {
    options := workflow.ActivityOptions{
        StartToCloseTimeout: time.Minute,
    }
    log := workflow.GetLogger(ctx)
    ctx = workflow.WithActivityOptions(ctx, options)

    results := []string{}
    selector := workflow.NewSelector(ctx)
    sem := workflow.NewSemaphore(ctx, 5)


    // Timer to release semaphore after a certain duration
    releaseTimer := workflow.NewTimer(ctx, time.Second*10) // 10-second timer
    selector.AddFuture(releaseTimer, func(f workflow.Future) {
        log.Info("Timer triggered: Releasing semaphore manually")
        sem.Release(1) // Release semaphore after timer expires
    })


    // Loop through all items and start activities, limiting concurrency to 5
    for _, item := range args.List {
        // Acquire semaphore before launching an activity
        log.Info("Acquiring semaphore for " + item)
        sem.Acquire(ctx, 1) // Block until the semaphore allows activity execution

        // Execute the activity and add the future to the selector
        future := workflow.ExecuteActivity(ctx, Test1, item)
        selector.AddFuture(future, func(f workflow.Future) {
            var result string
            err := f.Get(ctx, &result)
            if err != nil {
                log.Error("Activity failed", "Error", err)
            } else {
                log.Info("Activity completed", "Result", result)
                results = append(results, result)
            }

            // Release the semaphore after the activity completes
            sem.Release(1)
            log.Info("Released semaphore for " + result)
        })
    }



    // Use the selector to wait for all futures to complete
    log.Info("Processing futures")
    for selector.HasPending() {
        log.Info("Selecting next future")
        selector.Select(ctx) // Select and process the next future
        log.Info("Future processed")
    }

    // Final log and return results
    log.Info("Workflow completed, final results: ", "Results", results)
    return results, nil
}

func Test1(ctx context.Context, name string) (string, error) {
    time.Sleep(time.Second * 10) // Simulate some work
    return name, nil
}
