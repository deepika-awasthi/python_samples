from temporalio import activity

@activity.defn
async def start(user: str) -> str:
	return f"Activity started for {user}"


@activity.defn
async def startwithtimestamp(user: str, timestamp : str) -> str:
	return f"Activity started for {user} at {timestamp}"