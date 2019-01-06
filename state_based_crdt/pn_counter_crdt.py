"""
Created by Md Majid Jahangir
Implemented Specification 7 State based PN-Counter from A comprehensive study of Convergent and Commutative
Replicated Data Types -  https://hal.inria.fr/inria-00555588/document 

"""

import sys
sys.path.append('../')
from state_based_crdt import StateBasedCRDT, get_process_uuid
from abc import ABCMeta
import re

class PNCounter(StateBasedCRDT):
	def __init__(self,process_id,process_set):
		self.uid = get_process_uuid(process_id)			# 4: let g = myID() ⊲ g: source replica
		# 1: payload integer[n] P, integer[n] N ⊲ One entry per replica
		# 2: initial [0, 0, . . . , 0], [0, 0, . . . , 0]
		self.ppayload = {re.search(r'(?<=:)\w+[^>]', str(p)).group(0):0 for p in process_set}
		self.npayload = {re.search(r'(?<=:)\w+[^>]', str(p)).group(0):0 for p in process_set}

	# 3: update increment ()
	def increment(self):
		try:
			self.ppayload[self.uid] = self.ppayload[self.uid] + 1		# 5: P[g] := P[g] + 1
		except KeyError:
			print("Key error in mapping.")

	# 6: update decrement ()
	def decrement(self):
		try:
			self.npayload[self.uid] = self.npayload[self.uid] + 1		# 8: N[g] := N[g] + 1
		except KeyError:
			print("Key error in mapping.")

	# 9: query value () : integer v
	def value(self):
		return sum(self.ppayload.values())-sum(self.npayload.values())			# 10: let v =sum( P[i]) − sum(N[i])

	# 11: compare (X, Y) : boolean b
	@classmethod
	def compare(cls, X, Y):
		# 12: let b = (∀i ∈ [0, n − 1] : X.P [i] ≤ Y.P [i] ∧ ∀i ∈ [0, n − 1] : X.N[i] ≤ Y.N[i])
		return all(X.ppayload.get(key, 0) <= Y.ppayload.get(key, 0)
					for key in Y.ppayload.keys()) and all(X.npayload.get(key, 0) <= Y.npayload.get(key, 0)
					for key in Y.npayload.keys())

	# 13: merge (X, Y ) : payload Z
	@classmethod
	def merge(cls, X, Y):
		keys = set(X.ppayload.keys()) | set(Y.ppayload.keys())
		Z = { k:max(X.ppayload[k],Y.ppayload[k]) for k in keys}		# 14: let ∀i ∈ [0, n − 1] : Z.P [i] = max(X.P [i], Y.P [i])
		W = { k:max(X.npayload[k],Y.npayload[k]) for k in keys}		# 15: let ∀i ∈ [0, n − 1] : Z.N[i] = max(X.N[i], Y.N[i])
		return Z,W