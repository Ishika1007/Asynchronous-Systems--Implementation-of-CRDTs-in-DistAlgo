from abc import abstractmethod, abstractproperty, ABCMeta
import re

def get_process_uuid(pid):
	m = re.search(r'(?<=:)\w+[^>]', str(pid))
	return m.group(0)         

class StateBasedCRDT(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def value(self):
		pass

	@abstractmethod
	def merge(cls,X,Y):
		pass

	@abstractmethod
	def compare(cls,X,Y):
		pass

	