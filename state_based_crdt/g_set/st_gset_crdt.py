"""
Implemented Specification 11 State based GSet from A comprehensive study of Convergent and Commutative
Replicated Data Types -  https://hal.inria.fr/inria-00555588/document 
"""

import sys
sys.path.append('../')
from state_based_crdt import StateBasedCRDT
from abc import ABCMeta

class GSet(StateBasedCRDT):
	def __init__(self):
		#1: payload set A
		#2: initial empty set
		self.payload = set()	

	#5: query lookup (element e) : boolean b
	def lookup(self,e):
		return e in self.payload 		#6: let b = (e ∈ A)
	
	#3: update add (element e)			
	def add(self,e):
		self.payload.add(e)				#4: A := A ∪ {e}
		
	#7: compare (S, T) : boolean b		
	@classmethod
	def compare(cls,S,T):
		return S.payload.issubset(T.payload)		#8: let b = (S.A ⊆ T.A)
	
	#9: merge (S, T) : payload U
	@classmethod			
	def merge(cls,S,T):
		U = S.payload.union(T.payload)		#10: let U.A = S.A ∪ T.A
		return U

	
