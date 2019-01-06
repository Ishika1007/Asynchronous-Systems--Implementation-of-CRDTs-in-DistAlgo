import sys
sys.path.append('../')
from op_based_crdt import OperationBasedCRDT

class Counter(OperationBasedCRDT):
	def __init__(self, i):							#1: payload integer i
		self.i = i                                  #2: initial 0

	def update_increment_atSource(self):			#5: update increment ()	
		pass										#6  No precond: delivery order is empty

	def update_increment_downstream(self):			#6: downstream () 
		self.i = self.i + 1							#7: i := i + 1

	def update_decrement_atSource(self):			#8: update decrement ()
		pass										#9 No precond: delivery order is empty

	def update_decrement_downstream(self):			#9: downstream ()
		self.i = self.i - 1							#10: i := i − 1

	def value(self):								#3: query value () : integer j
		return self.i                               #4: let j = i



