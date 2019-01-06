import sys
sys.path.append('../')
from state_based_crdt import StateBasedCRDT, get_process_uuid
from abc import ABCMeta
import re

class LWWRegister(StateBasedCRDT):
	def __init__(self, x, t):
		#1: payload X x, timestamp t ⊲ X: some type
		#2: initial ⊥, 0
		self.x = x
		self.t = t
		
	#5: query value () : X w
	def value(self):
		return self.x	#6: let w = x

	#7: compare (R, R′) : boolean b
	@classmethod
	def compare(cls, R1, R2):
		return R1.t <= R2.t	#8: let b = (R.t ≤ R′.t)

	#3: update assign (X w)
	def assign(self, w, t):
		#4: x, t := w, now() ⊲ Timestamp, consistent with causality
		self.x = w
		self.t = t

	#9: merge (R, R′) : payload R′′
	@classmethod
	def merge(cls, R1, R2):
		R3 = LWWRegister(0, 0)
		#10: if R.t ≤ R′.t then R′′.x, R′′.t = R′.x, R′.t

		if(R2.t>R1.t):
			R3.x,R3.t = R2.x, R2.t
		else: 			#11: else R′′.x, R′′.t = R.x, R.t
			R3.x,R3.t = R1.x, R1.t
		return R3

