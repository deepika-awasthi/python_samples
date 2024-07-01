go run worker/main.go

```
2024/06/28 15:41:58 INFO  No logger configured for temporal client. Created default one.
2024/06/28 15:41:58 INFO  Started Worker Namespace default TaskQueue GREETING_TASK_QUEUE WorkerID 44637@Deepikas-MacBook-Pro.local@
2024/06/28 15:42:30 DEBUG NewTimer Namespace default TaskQueue GREETING_TASK_QUEUE WorkerID 44637@Deepikas-MacBook-Pro.local@ WorkflowType OrderWorkflow WorkflowID order-initiated-R53J8X2KZ RunID 0879c9b5-a15b-4acf-9fb7-b3bfeb50afca Attempt 1 TimerID 5 Duration 1m0s
```

> go run start/main.go
```
2024/06/28 15:42:30 INFO  No logger configured for temporal client. Created default one.
2024/06/28 15:42:30 Started workflow order-initiated-R53J8X2KZ
```

 ~/t/my_p/test_python_sdk/g/hello-world-temporal  main  go test
 ```                                                                  ok  3s  12:04:03 AM 
2024/07/01 00:04:39 DEBUG Auto fire timer TimerID 0 TimerDuration 1m0s TimeSkipped 1m0s
PASS
ok  	hello-world-temporal/app	0.326s

```