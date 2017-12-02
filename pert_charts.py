#!/usr/bin/python3

import unittest

from graph import *


class PERTGraph ( Graph ):

	def dag_longest_path(self,source, file_prefix='', blank=False):
		"""
		Run the DAG longest-path algorithm.

		:param source: label or index of the source vertex 
		:type source: str
		:param file_prefix: if provided, the procedure generates .dot diagrams for each step; dot filenames concatenate this prefix with a number suffix.
		:type file_prefix: str
		:param blank: if True, the procedure generates only .dot templates for each step; the colors and attributes of the node are not shown.
		:param blank: bool
		"""
		self.dag_shortest_path(source, file_prefix=file_prefix, blank=blank)

	def dag_critical_path(self,source):
		""" Compute a critical path in the graph.

		:param source: label or index of the source vertex 
		:type source: str
		:return: the list of vertices that represent a longest path from the source vertex.
		:rtype: list
		"""
		self.dag_longest_path(source )
		return self.get_critical_path(source )

	def initialize_single_source(self, s):
		""" Initialize the graph

		:param s: source vertex
		:type s: Vertex
		"""
		#print("PERT initialize single source")
		for label, v in self.V.items():
			v.color=Vertex.WHITE
			v.distance = -Vertex.INFTY
			v.pi = None
		s.distance = 0
		
	def relax(self, u, v ):
		"""
		Relax vertex v through u

		:param u: vertex u
		:param v: vertex v
		:type u: Vertex
		:type v: Vertex
		"""
		if v.distance < (u.distance + self.Matrix[u][v] ):
			#log('PERT relax({},{}): {} --> {}'.format(u.label, v.label, v.distance, (u.distance + self.Matrix[u][v])),3)
			v.distance = (u.distance + self.Matrix[u][v] )

			if hasattr(v,'heap') and v.heap is not None:
				v.float_key( v.heap_index )
			v.pi = u

	
	def get_critical_path(self, source):
		"""
		Compute a critical path in the longest-path tree.

		:param source: the source vertex
		:type source: str
		:return: a list of vertices, that represent a longest path from the root to a leaf, in the tree obtained by DAG-Longest-Path, 
		:rtype: list
		"""
		# find vertex with largest distance
		distance = -Vertex.INFTY
		furthest = source
		for v in self.V.values():
			if v.distance > distance:
				distance = v.distance
				furthest = v
		path = [] 
		current = furthest
		while current is not None:
			path.insert(0, current )
			current = current.pi
		return path


	@classmethod
	def from_dot( cls, dotfile ):
		"""
		Load a graph from a dot file.

		:param dotfile: the name of a graph-definition file, in DOT format.
		:type dotfile: str
		:return: a Graph object;  an edge numerical label in the dot file is interpreted as an edge weight.
		:rtype: Graph
		"""
		
		#sorted_edges = sorted( e, key=lambda x: x[0])
		#print(sorted_edges)

		v, e, directed = Graph.from_dot_to_lists( dotfile )

		return PERTGraph( v, e, directed )

class PERTGraphUnitTest( unittest.TestCase ):



	def test_pert_chart_1(self):
		g = self.make_pert_chart()
		critical_path = g.dag_critical_path('s') 

		self.assertEqual( [ v.label for v in critical_path], ['s', 'h', 'i', 'j', 'd', 'g', 'l', 'n', 'r', 't', 'u'] ) 
		self.assertEqual( critical_path[-1].distance, 12)

		
	def test_pert_chart_2(self):
		g = self.make_pert_chart_space_probe()
		critical_path = g.dag_critical_path('s') 

		self.assertEqual( [ v.label for v in critical_path], ['s', 'a', 'b', 'c', 'l', 'i', 'k', 't'])
		self.assertEqual( critical_path[-1].distance, 22)

		

	#### AUXILIARY FUNCTIONS ####

	@classmethod
	def make_pert_chart(cls):
		g = PERTGraph(
			('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u'),
			(	('s','a',0),
				('s','h',0),
				('s','o',0),
				('a','b',0),
				('b','c',1),
				('b','f',1),
				('c','d',0),
				('d','e',1),
				('d','g',2),
				('d','k',1),
				('f','d',0),
				('g','l',3),
				('k','l',3),
				('h','i',0),
				('i','j',2),
				('j','d',0),
				('j','m',1),
				('l','n',2),
				('n','r',1),
				('r','t',1),
				('t','u',1),
				('o','p',1),
				('p','q',2),
				('q','u',1)), directed=True)
		return g


	@classmethod
	def make_pert_chart_space_probe(cls):
		g = PERTGraph(
			('s','a','b','c','d','e','f','g','h','i','j','k','l','t'),
			( 	('s','a',12),
				('s','e',3),
				('s','f',3),
				('a','b',2),
				('b','c',2),
				('b','h',1),
				('c','l',0),
				('h','l',0),
				('l','i',1),
				('e','f',2),
				('f','d',1),
				('f','g',1),
				('f','i',3),
				('i','j',1),
				('i','k',4),
				('k','t',1)), directed=True)
		return g
def main():
        unittest.main()

if __name__ == '__main__':
        main()


