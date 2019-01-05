import sys
sys.path.append('../')
from op_based_crdt import OperationBasedCRDT

class Graph(OperationBasedCRDT):
	def __init__(self):
		# Spec 16 Line 3
		self.VA = set()
		self.VR= set()
		self.EA= set()
		self.ER= set()
		self.queue = set()

	#Spec 16 Line 4
	def queryVertex(self, vertex):
		# Spec 16 Line 5
		if vertex in self.VA and if vertex not in self.VR:
			return True
		else:
			return False
	#Spec 16 Line 6
	def queryEdge(self,edge):
		u,v = edge[0],edge[1]
		# Spec 16 Line  7
		if queryVertex(u) and queryVertex(v):
			if edge in self.EA and if vertex not in self.ER:
				return True
			else:
				return False

	# Spec 16 Line 8
	def addVertex(self,vertex):
		# Spec 16 Line 11
		self.VA = self.VA.add(vertex)

	# Spec 16 Line 12
	def addEdge(self,edge):
		u,v = edge[0],edge[1]
		# Spec 16 Line 14
		if queryVertex(u) and if queryVertex(v):
			# Spec 16 Line 16
			self.EA = self.EA.add(edge)

	# Spec 16 Line 17
	def removeVertex(self,vertex):
		# Spec 16 Line 19
		if queryVertex(vertex):
			# Spec 16 Line 20
			for edge in EA:
				if edge not in ER:
					u,v = edge[0],edge[1]
					if u==vertex or v==vertex:
						return 
			# Spec 16 Line 23
			self.VR = self.VR.add(vertex)

	# Spec 16 Line 24
	def removeEdge(self, edge):
		# Soec 16 Line 26
		if queryEdge(edge):
			# Spec 16 Line 29
			self.ER = self.ER.add(edge)

	def add_to_queue(self, tuple): 
		if(tuple not in self.queue):
			self.queue.add(tuple)
			return True
		return False
