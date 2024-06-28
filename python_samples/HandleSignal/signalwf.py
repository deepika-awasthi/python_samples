import asyncio
from typing import Any, List

from temporalio import workflow

@workflow.defn
class MySignalWorkflow:
	def __init__(self) -> None:
		self._pending_task : asyncio.Queue[str] = asyncio.Queue()
		self._exit = False


	@workflow.run
	async def run(self) -> List[str]:
		work_list:List[str] = []
		while True:
			await workflow.wait_condition(
				lambda : not self._pending_task.empty() or self._exit
			)

			while not self._pending_task.empty():
				work_list.append(f"Count, {self._pending_task.get_nowait()}")

			if self._exit:
				return work_list


	@workflow.signal
	async def submit_pending_task(self, name : str) -> None:
		await self._pending_task.put(name)

	@workflow.signal 
	def exit(self) -> None:
		self._exit = True


	@workflow.signal(name = "my tests signal")
	async def name_for_my_signal(self, name : str) -> None:
		await self._pending_task.put(name)