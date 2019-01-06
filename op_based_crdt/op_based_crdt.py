from abc import ABC, abstractmethod, ABCMeta

class OperationBasedCRDT(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		pass
	
	@abstractmethod
	def value(): 
		pass
