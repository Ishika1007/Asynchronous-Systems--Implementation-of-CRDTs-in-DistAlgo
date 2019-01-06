"""
Created by Md Majid Jahangir
Implemented Specification 6 from A comprehensive study of Convergent and Commutative
Replicated Data Types -  https://hal.inria.fr/inria-00555588/document 
"""
import sys
sys.path.append('../')
from state_based_crdt import StateBasedCRDT, get_process_uuid
from abc import ABCMeta
import re

class IncrementOnlyCounter(StateBasedCRDT):
	def __init__(self,process_id,process_set):
		self.uid = get_process_uuid(process_id)		# 4: let g = myID()
		# 1: payload integer[n] P
		# 2: initial [0, 0, . . . , 0]
		self.payload = {re.search(r'(?<=:)\w+[^>]', str(p)).group(0):0 for p in process_set}

	# 3: update increment ()
	def increment(self):
		try:
			self.payload[self.uid] = self.payload[self.uid] + 1		# 5: P[g] := P[g] + 1
		except KeyError:
			print("Key error in mapping.")

	# 6: query value () : integer v
	def value(self):
		return sum(self.payload.values())		# 7: let v = sum (P[i])

	# 8: compare (X, Y) : boolean b
	@classmethod
	def compare(cls, X, Y):
		# 9: let b = (∀i ∈ [0, n − 1] : X.P [i] ≤ Y.P [i])
		return all(X.payload.get(key, 0) <= Y.payload.get(key, 0)
					for key in Y.payload.keys())
		
	# 10: merge (X, Y ) : payload Z 
	@classmethod
	def merge(cls, X, Y):
		keys = set(X.payload.keys()) | set(Y.payload.keys())
		Z = { k:max(X.payload[k],Y.payload[k]) for k in keys}		# 11: let ∀i ∈ [0, n − 1] : Z.P [i] = max(X.P [i], Y.P [i])
		return Z


        