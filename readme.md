define search attributes for namespace

```
temporal operator search-attribute create --name="CustomSA" --type="Keyword"
```

start workflow with search attributes:

```
temporal workflow start --task-queue hello_workflow_tq --type "HelloWorkflow" --workflow-id "hello_workflow_id" --input '"temporal_python_sdk"' --search-attribute CustomSA=\"SearchAttributeCustomSA\"
```


HeartBeats: 

while activity/activities are running you can see last heartbeat details in "pending activities" view
heartbeats are not recorded in event history

```

sum(rate(temporal_cloud_v0_frontend_service_request_count{temporal_namespace=~"$temporal_namespace"}[$__rate_interval])) by (temporal_namespace,operation)
```


