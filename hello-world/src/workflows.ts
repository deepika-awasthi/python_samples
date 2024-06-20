// // @@@SNIPSTART typescript-hello-workflow
// import { proxyActivities } from '@temporalio/workflow';
// // Only import the activity types
// import type * as activities from './activities';

// const { greet } = proxyActivities<typeof activities>({
//   startToCloseTimeout: '1 minute',
// });

// /** A workflow that simply calls an activity */
// export async function example(name: string): Promise<string> {
//   return await greet(name);
// }
// // @@@SNIPEND


import { proxyActivities, defineSignal, sleep, Trigger, setHandler } from '@temporalio/workflow';
import type * as activities from './activities';

const { sendSlackNotification } = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
});

export const completeSignal = defineSignal('completeConnection');

export async function waitForConnectionCompletion(id: string): Promise<boolean> {
  const completeTrigger = new Trigger<boolean>();
  setHandler(completeSignal, () => completeTrigger.resolve(true));
  const connectionCompleted = await Promise.race([completeTrigger, sleep('1 minutes')]);
  console.log('connectionCompleted:', connectionCompleted);
  if (connectionCompleted) {
    return true;
  } else {
    await sendSlackNotification(id);
    return false;
  }
}
