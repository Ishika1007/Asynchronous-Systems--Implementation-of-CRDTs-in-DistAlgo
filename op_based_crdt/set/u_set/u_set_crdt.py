import sys
sys.path.append('../')
from abstract_set_crdt import SetCRDT

#Specification 13: U-Set: Op-based 2P-Set with unique elements
class USet(SetCRDT):

	def __init__(self):
		self.S = set() 						#1: payload set S #2: initial ∅

	def lookup(self, e):					#3: query lookup (element e) : boolean b
		return e in self.S                  #4: let b = (e ∈ S)

	def update_add_atSource(self, e):		#5: update add (element e) #6: atSource (e)
		return e not in self.S			#7: pre e is unique

	def update_add_downstream(self, e):		#8: downstream (e)
		self.S.add(e)						#9: S := S ∪ {e}

	def update_remove_atSource(self, e):	#10: update remove (element e) #11: atSource (e)
		return self.lookup(e)				#12: pre lookup(e) [2P-Set precondition]

	def update_remove_downstream(self, e):	#13: downstream (e)
		if(self.lookup(e)):					#14: pre add(e) has been delivered [using queue to]
			self.S.remove(e)				#15: S := S \ {e}

