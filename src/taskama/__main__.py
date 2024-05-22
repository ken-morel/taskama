'''\
Taskama:
it helps you monitor cpu and memory usage of your machine using psutil
'''
from ttkbootstrap import *  # for ui
from pyoload import *  # internal for typechecking and casting
import psutil  # system calls to get cpu, memory and battery usage

from pathlib import Path
import json  # for parsing the sattings file


type JSONSerializable = str | int | float | list | tuple  # type for json
                                                          # serializable data


@annotate
class Settings(dict):
	'''\
	@annotate
	class Settings(dict)
	
	Holds ant interfaces the json settings file
	'''
	class CouldNotSaveError(OSError):
		pass

	path: Path  #the path to json file

	def __init__(self: Any, path: Cast(Path)):
		'''def __init__(self: Any, path: Cast(Path))
		
		:param path: The path to the json settings file
		:return: the Settings object
		'''
		super().__init__()
		self.path = path
		self.load()

	def load(self: Any) -> None:
		'''\
		def load(self: Any) -> None

		loads or reloads the setting file into the Settings dict-like object
		'''
		self.empty()
		try:
			json_text = self.path.read_text()
			data = json.loads(json_text)
			assert typeMatch(data, dict[str, JSONSerializable]), ('wrong '
															    'json file')
		except (OSError, AssertionError):
			pass
		else:
			self.update(data)
	def dump(self: Any):
		'''def dump(self: Any)
		Saves the current settings as json file
		'''
		try:
			json_text = json.dumps(self)
			self.path.write_text(json_text)
		except OSError as e:
			raise Settings.CouldNotSaveError(self.path) from e


class Root(Frame):
	settings: Settings
	@annotate
	def __init__(self:Any, settings: Cast(Settings) = 'taskama-settings.json'):
		super().__init__(
			themename=self.settings.get('themename', 'vapor'),
		)

		self.create_widgets()

	def create_widgets(self: Any) -> None:
		self.pr_memory = ProgressBar(self)
		self.pr_memory.grid(column=0, row=0)

		self.pr_battery = ProgressBar(self)
		self.pr_battery.grid(column=0, row=0)

		self.pr_cpu = ProgressBar(self)
		self.pr_cpu.grid(column=0, row=0)

	def update_widgets(self: Any) -> None:
		pass

	def update(self:Any):
		self.update_widgets()
		super().__update__()

@annotate
def smoothener(stack_size: int = 10):
	stack = [0]
	while True:
		value = yield sum(stack) / len(stack)
		stack.append(value)
		stack = stack[-10:]



root = Root()

root.mainloop()