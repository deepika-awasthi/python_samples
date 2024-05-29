from temporalio.client import Client

class ValidateSingleInstance(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class TemporalClient(metaclass=ValidateSingleInstance):
    def __init__(self):
        self.client = None

    async def get_client(self):
        if self.client is None:
            self.client = await Client.connect("localhost:7233")
        return self.client