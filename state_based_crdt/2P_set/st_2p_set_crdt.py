"""
Implemented Specification 12 State based 2P-Set from A comprehensive study of Convergent and Commutative
Replicated Data Types -  https://hal.inria.fr/inria-00555588/document 
"""

import sys
sys.path.append('../')
from state_based_crdt import StateBasedCRDT
from abc import ABCMeta

class StateBased2PSet(StateBasedCRDT):
	def __init__(self):
		#1: payload set A, set R ⊲ A: added; R: removed
		#2: initial empty set, empty set
		self.Apayload = set()
		self.Rpayload = set()	

	#3: query lookup (element e) : boolean b
	def lookup(self,e):
		return e in self.Apayload and e not in self.Rpayload	#4: let b = (e ∈ A ∧ e /∈ R)
	
	#5: update add (element e)			
	def add(self,e):
		self.Apayload.add(e)				#6: A := A ∪ {e}

	#7: update remove (element e)
	def remove(self,e):
		if self.lookup(e):					#8: pre lookup(e)
			self.Rpayload.add(e)		#9: R := R ∪ {e}
		
	#10: compare (S, T) : boolean b		
	@classmethod
	def compare(cls,S,T):
		return S.Apayload.issubset(T.Apayload) or S.Rpayload.issubset(T.Rpayload)		#11: let b = (S.A ⊆ T.A ∨ S.R ⊆ T.R)
	
	#12: merge (S, T) : payload U
	@classmethod			
	def merge(cls,S,T):
		U = S.Apayload.union(T.Apayload)		#13: let U.A = S.A ∪ T.A
		V = S.Rpayload.union(T.Rpayload)		#14: let U.R = S.R ∪ T.R
		return U,V
