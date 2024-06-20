import { Runtime, DefaultLogger, Worker, LogEntry } from '@temporalio/worker';
import { WorkflowCoverage } from '@temporalio/nyc-test-coverage';
import { TestWorkflowEnvironment } from '@temporalio/testing';
import { v4 as uuid } from 'uuid';


import * as activities from '../activities';
import { waitForConnectionCompletion } from '../workflows';

const workflowCoverage = new WorkflowCoverage();
let testEnv: TestWorkflowEnvironment;

const mockActivities: Partial<typeof activities> = {
  sendSlackNotification: () => {
    return Promise.resolve({ success: true, metadata: {} });
  },
};

describe('waitForConnectionCompletionWorkflow', () => {

  before(() => {
    // Use console.log instead of console.error to avoid red output
    // Filter INFO log messages for clearer test output
    Runtime.install({
      logger: new DefaultLogger('INFO', (entry: LogEntry) =>
        // eslint-disable-next-line no-console
      {
        console.log(`[${entry.level}]`, entry.message);
      }


      ),
    });
  });

  describe('if the connection does not complete within 10 minutes',async () => {
    before(async () => {
      try {
        testEnv = await TestWorkflowEnvironment.createTimeSkipping();
        console.log(testEnv);
      } 
      catch (error) {
        throw error;
    }
    });

    after(async () => {
      await testEnv?.teardown();
    });

    after(() => {
      jest.clearAllMocks();
      workflowCoverage.mergeIntoGlobalCoverage();
    });

    it('returns a completed status and connection_completed as false', async () => {
      const { client, nativeConnection } = testEnv as TestWorkflowEnvironment;
      const worker = await Worker.create(
        workflowCoverage.augmentWorkerOptions({
          connection: nativeConnection,
          taskQueue: 'test',
          workflowsPath: require.resolve('../index'),
          activities: mockActivities,
        })

      );

      const result = await worker.runUntil(async () => {
        return await client.workflow.execute(waitForConnectionCompletion, {
          taskQueue: 'test',
          workflowId: `connecting_${uuid()}`,
          args: ['id'],
        });
      });
      expect(result).toEqual(false);
    });
  });
});