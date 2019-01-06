import sys
sys.path.append('../')
from abc import ABC, abstractmethod, ABCMeta

class SetCRDT(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def lookup(self, e):
		pass

	@abstractmethod
	def update_add_atSource(self, e):
		pass

	@abstractmethod
	def update_add_downstream(self, e):
		pass

	@abstractmethod
	def update_remove_atSource(self, e):
		pass

	@abstractmethod
	def update_remove_downstream(self, e):
		pass


