import itertools
import esper


class Event:
	def __init__(self):
		self.type = ''

class EventManager:
	def __init__(self):
		self._events = []
		self._next_events = []

	def read(self):
		return iter(self._events)

	def send(self, event):
		pass

	def update(self):
		self._events = self._next_events
		self._next_events = []


class System(esper.Processor):
	event_types = []

	def __init__(self):
		super().__init__();
		self.events = EventManager()


class World(esper.World):
	def __init__(self):
		super().__init__()
		self._systems_by_event = {}

	def _send_event(self, event):
		systems = self._systems_by_event.get(event.type) or []
		for system in systems:
			system.events._next_events.append(event)

	def _register_system(self, system):
		for event_type in system.event_types:
			systems = self._systems_by_event.setdefault(event_type, [])
			systems.append(system)
		system.events.send = self._send_event

	def add_system(self, system, priority=0):
		self._register_system(system)
		super().add_processor(system, priority)


	def update_events(self):
		for system in set(itertools.chain.from_iterable(self._systems_by_event.values())):
			system.events.update()