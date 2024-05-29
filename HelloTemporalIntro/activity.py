import logging
from temporalio import activity
from welcome_msg import WelcomeMessage

@activity.defn
async def hello_activity(input: WelcomeMessage) -> str:
    return f"{input.greeting}, {input.name}!"