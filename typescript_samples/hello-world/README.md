```
 ~/temporal/my_python_samples/test_python_sdk  main !1  cd typescript_samples                                                                                                                 ok  to py  04:18:50 AM

 ~/temporal/my_python_samples/test_python_sdk/typescript_samples  main !1  ls -lrt                                                                                                            ok  to py  04:18:54 AM
total 0
drwxr-xr-x@ 15 dawasthi  staff  480 Jun 21 01:35 hello-world

 ~/temporal/my_python_samples/test_python_sdk/typescript_samples  main !1  cd hello-world                                                                                                     ok  to py  04:18:56 AM

 ~/t/my_python_samples/test_python_sdk/typescript_samples/hello-world  main !1  ls -lrt                                                                                                       ok  to py  04:18:59 AM
total 24
drwxr-xr-x@   7 dawasthi  staff    224 Jun 21 01:31 src
-rw-r--r--@   1 dawasthi  staff    252 Jun 21 01:31 tsconfig.json
-rw-r--r--@   1 dawasthi  staff   1427 Jun 21 02:21 package.json
drwxr-xr-x@ 360 dawasthi  staff  11520 Jun 21 02:21 node_modules
-rw-r--r--@   1 dawasthi  staff     22 Jun 21 04:18 README.md

 ~/t/my_python_samples/test_python_sdk/typescript_samples/hello-world  main !1  npm install                                                                                                   ok  to py  04:19:01 AM

up to date, audited 626 packages in 2s

78 packages are looking for funding
  run `npm fund` for details

6 vulnerabilities (4 moderate, 2 high)

To address issues that do not require attention, run:
  npm audit fix

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.

 ~/t/my_python_samples/test_python_sdk/typescript_samples/hello-world  main !1  npm test                                                                                                      ok  to py  04:19:07 AM

> temporal-hello-world@0.1.0 test
> mocha --exit --require ts-node/register --require source-map-support/register src/mocha/*.test.ts



  waitForConnectionCompletionWorkflow
    if the connection does not complete within 10 minutes
      1) "before all" hook for "returns a completed status and connection_completed as false"
      2) "after all" hook for "returns a completed status and connection_completed as false"


  0 passing (2s)
  2 failing

  1) waitForConnectionCompletionWorkflow
       if the connection does not complete within 10 minutes
         "before all" hook for "returns a completed status and connection_completed as false":
     Error: Timeout of 2000ms exceeded. For async tests and hooks, ensure "done()" is called; if returning a Promise, ensure it resolves. (/Users/dawasthi/temporal/my_python_samples/test_python_sdk/typescript_samples/hello-world/src/mocha/workflows.test.ts)
      at listOnTimeout (node:internal/timers:573:17)
      at processTimers (node:internal/timers:514:7)

  2) waitForConnectionCompletionWorkflow
       if the connection does not complete within 10 minutes
         "after all" hook for "returns a completed status and connection_completed as false":
     ReferenceError: jest is not defined
      at Context.<anonymous> (src/mocha/workflows.test.ts:52:7)









```