worker.py

```
~/t/my_p/test_python_sdk/p/NumPollerMetricsTest  main !8 ?4  python3 -m venv path/to/venv                                          ok  to py  03:52:20 PM 

 ~/t/my_p/test_python_sdk/p/NumPollerMetricsTest  main !8 ?4  cd path/to/venv/bin                                                   ok  to py  03:52:29 PM 

 ~/t/my_p/test_python_sdk/p/N/p/t/v/bin  main !8 ?4  source activate                                                                ok  to py  03:52:33 PM 

 ~/t/my_p/test_python_sdk/p/N/p/t/v/bin  main !8 ?4  pip3 install prometheus_client                                                 ok  to py  03:52:35 PM 

Collecting prometheus_client
  Using cached prometheus_client-0.20.0-py3-none-any.whl.metadata (1.8 kB)
Using cached prometheus_client-0.20.0-py3-none-any.whl (54 kB)
Installing collected packages: prometheus_client
Successfully installed prometheus_client-0.20.0

[notice] A new release of pip is available: 24.0 -> 24.1.2
[notice] To update, run: pip install --upgrade pip

 ~/t/my_p/test_python_sdk/p/N/p/t/v/bin  main !8 ?4  pip3 install temporalio                                                        ok  to py  03:52:41 PM 
Collecting temporalio
  Using cached temporalio-1.6.0-cp38-abi3-macosx_11_0_arm64.whl.metadata (71 kB)
Collecting protobuf>=3.20 (from temporalio)
  Using cached protobuf-5.27.2-cp38-abi3-macosx_10_9_universal2.whl.metadata (592 bytes)
Collecting types-protobuf>=3.20 (from temporalio)
  Using cached types_protobuf-5.27.0.20240626-py3-none-any.whl.metadata (2.0 kB)
Collecting typing-extensions<5.0.0,>=4.2.0 (from temporalio)
  Using cached typing_extensions-4.12.2-py3-none-any.whl.metadata (3.0 kB)
Using cached temporalio-1.6.0-cp38-abi3-macosx_11_0_arm64.whl (9.5 MB)
Using cached protobuf-5.27.2-cp38-abi3-macosx_10_9_universal2.whl (412 kB)
Using cached types_protobuf-5.27.0.20240626-py3-none-any.whl (68 kB)
Using cached typing_extensions-4.12.2-py3-none-any.whl (37 kB)
Installing collected packages: typing-extensions, types-protobuf, protobuf, temporalio
Successfully installed protobuf-5.27.2 temporalio-1.6.0 types-protobuf-5.27.0.20240626 typing-extensions-4.12.2

[notice] A new release of pip is available: 24.0 -> 24.1.2
[notice] To update, run: pip install --upgrade pip


 ~/t/my_p/test_python_sdk/p/NumPollerMetricsTest  main !8 ?3  python3 worker.py                                                 ok  9s  to py  03:55:59 PM 
INFO:root:DescribeTaskQueue response for hello-task-queue: 3 pollers
INFO:root:DescribeTaskQueue response for hello-task-queue: 4 pollers

```

starter.py

```
enable virtual env in new terminal

 ~/t/my_p/test_python_sdk/p/NumPollerMetricsTest  main !8 ?4  python3 starter.py                                                    ok  to py  03:54:45 PM 
Workflow result: <temporalio.client.WorkflowHandle object at 0x1036b7500>

```
