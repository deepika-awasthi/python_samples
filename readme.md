define search attributes for namespace

```
temporal operator search-attribute create --name="CustomSA" --type="Keyword"
```

start workflow with search attributes:

```
temporal workflow start --task-queue hello_workflow_tq --type "HelloWorkflow" --workflow-id "hello_workflow_id" --input '"temporal_python_sdk"' --search-attribute CustomSA=\"SearchAttributeCustomSA\"
```