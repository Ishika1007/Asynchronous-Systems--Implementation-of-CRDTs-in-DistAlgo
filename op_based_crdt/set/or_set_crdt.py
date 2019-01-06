"""
Created by Md Majid Jahangir
Implemented Specification 15 Operation based Observed-Remove Set from A comprehensive study of Convergent and Commutative
Replicated Data Types -  https://hal.inria.fr/inria-00555588/document 

"""

import sys
import uuid
sys.path.append('../')
from abstract_set_crdt import SetCRDT

class ORSet(SetCRDT):
	def __init__(self):
		# 1: payload set S ⊲ set of pairs { (element e, unique-tag u), . . . }
		#2: initial empty set
		self.S = dict()

	#3: query lookup (element e) : boolean b
	def lookup(self,e):
		b = False
		#4: let b = (∃u : (e, u) ∈ S)
		if e in self.S:
			b = len(self.S[e])>0
		return b

	#5: update add (element e)

	#6: atSource (e)
	def update_add_atSource(self,e):
		alpha = str(uuid.uuid4())				#7: let α = unique() ⊲ unique() returns a unique value
		self.update_add_downstream(e,alpha)				#8: downstream (e, α)
		return alpha

	#8: downstream (e, α)
	def update_add_downstream(self,e,alpha):
		if e not in self.S:
			self.S[e]= set()
		self.S[e].add(alpha)					#9: S := S ∪ {(e, α)}

	#10: update remove (element e)

	#11: atSource (e)
	def update_remove_atSource(self,e):
		R = dict()
		if self.lookup(e):						#12: pre lookup(e)
			R[e] = { x for x in self.S[e]}		#13: let R = {(e, u)|∃u : (e, u) ∈ S}
		self.update_remove_downstream(R)		#14: downstream (R)
		return R


	#14: downstream (R)
	def update_remove_downstream(self,R):
		b = False
		elem = None
		for e,u in R.items():
			elem = e
			if e in self.S:
				b = all([True if x in self.S[e] else False for x in u])		#15: pre ∀(e, u) ∈ R : add(e, u) has been delivered ⊲ U-Set precondition; causal order suffices

		#16: S := S \ R ⊲ Downstream: remove pairs observed at source
		if b==True:
			self.S[elem] -= R[elem]
		if elem != None and len(self.S[elem])==0:
			del self.S[elem]

	def getr(self):
		print(self.S)