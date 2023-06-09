#!/usr/bin/python3

import unittest
import collections as clt

from heap import *
from enum import *
import re



log_level=1

def log( string, level=1):
	global log_level
	if log_level >= level:
		print(string)

class LabelException( Exception ): pass


class Walk(Enum):
	BFS=0
	DFS=1
	DIJKSTRA=2
	DAGSP=3

class Vertex():
	""" A vertex definition."""

	# These constants can be referred to afterwards as follows:
	#	Vertex.WHITE, Vertex.GRAY...
	WHITE = 0
	GRAY = 1
	BLACK = 2
	INFTY = 2**15
	
	def __init__(self, label=''):
		"""
		Initialize a vertex
		
		:param index: position in the vertex array
		:param label: human-friendly label
		:type index: int
		:type label: str
		"""

		# a label (the index itself, or a letter)		
		self.label = label
		self.short_label = label[0]

		# distance = infinity by default
		self.distance = Vertex.INFTY
		self.pi = None
		self.color = Vertex.WHITE
		
		# for depth-first search
		self.discovery = 0
		self.finish = 0

		self.coord=(0,0)

	def x(self): return self.coord[0]
	def y(self): return self.coord[1]

	def to_dot(self, walk=Walk.BFS, blank=False):
		"""
		Dot representation of the vertex.

		:param walk: the type of walk: BFS (the default), or DFS
		:type walk: Walk
		:return: a string that encodes the Vertex in dot format
		:rtype: str
		"""
		vs = []
		vs.append(self.label)

		if blank:
			return vs[0] + ';'

		vs.append('[')

		label_string = self.label
		font_string = ' fontname="DejaVu Serif"'

		if walk==Walk.BFS or walk==Walk.DIJKSTRA or walk==Walk.DAGSP:
			if self.distance==Vertex.INFTY:
				label_string += ':&infin;'
				font_string=' fontname="Symbol"'
			elif self.distance==-Vertex.INFTY:
				label_string += ':-&infin;'
				font_string=' fontname="Symbol"'
			else:
				label_string += ':{}'.format(self.distance)
		elif walk==Walk.DFS:
			label_string += ':{}:{}'.format( self.discovery if self.discovery else '-', self.finish if self.finish else '-' )
			
		vs.append('label="{}"{}'.format( label_string, font_string ))
		if self.color == Vertex.BLACK:
			vs.append( 'fontcolor=white style=filled fontname="time-bold" fillcolor=black')		
		elif self.color == Vertex.GRAY:
			vs.append( 'style=filled fontname="time-bold" fillcolor=gray52')		
		
		vs.append('];')
		return ' '.join(vs)

	def to_tikz(self, walk=Walk.BFS, blank=False):
		style='white'
		if self.color==Vertex.GRAY:
			style='gray'
		elif self.color==Vertex.BLACK:
			style='black'
			
		
		label_string = '${}'.format(self.label)

		if walk==Walk.BFS or walk==Walk.DIJKSTRA or walk==Walk.DAGSP:
			if self.distance==Vertex.INFTY:
				label_string += ':\infty$'
			elif self.distance==-Vertex.INFTY:
				label_string += ':-\infty$'
			else:
				label_string += ':{}$'.format(self.distance)
		elif walk==Walk.DFS:
			label_string += ':{}:{}$'.format( self.discovery if self.discovery else '-', self.finish if self.finish else '-' )
			
			
		node_string = "\\node [{}] ({}) at ({},{}) {{{}}};".format(style, self.label, self.x(), self.y(), label_string)
		return node_string	
	
	def copy(self):
		"""
		Provide a copy of this vertex.

		Note that the parent pointer (if not null) still points to the original vertex's parent after the copy.
		Its is up the caller function (typically: the Graph's copy function) to update the pointer to the proper node.
		
		:return: a copy of this vertex, with its attributes.
		:rtype: Vertex
		"""
		v = Vertex( self.label )
		v.short_label=v.short_label
		v.color = self.color
		v.distance = self.distance
		# parent pointer still points at the original graph's vertex at time
		# (transferring the pointer happens when copying the graph itself)
		v.pi = self.pi
		v.discovery = self.discovery
		v.finish = self.finish
		return v



	# overriding the > operator (for comparisons internal to the min-queue)
	def __gt__(self, other):
		if isinstance(other, Vertex):
			if self.distance == other.distance:
				return self.label > other.label
			return self.distance > other.distance
		return NotImplemented

	#def __lt__(self, other):
	#	if isinstance(other, Vertex):
	#		return self.label < other.label
	
	def __str__(self):
		return '({}:{} pi={} )'.format(self.label, self.distance, self.pi.label if self.pi else self.pi)

class Graph():
	""" A graph definition """


	def __init__(self,v=(),e=(), directed=False):
		""" Create graph with given vertices 

		:param v: labels, i.e. integers, or alphabetical labels
		:param e: edges, i.e pairs of labels
		:param directed: if True, create a directed graph; False otherwise (the default).
		:type v: tuple
		:type e: tuple	
		:type directed: bool
		"""
		self.weighted = False

		# Reads the vertex labels and create corresponding Vertex objects in V
		# Note: this is an ordered dictionary: pairs (key, value) are listed
		# in the order they were inserted, which is convenient for testing
		self.V = clt.OrderedDict()

		for label in sorted(v):
			self.V[label] = Vertex( label ) 
			
		# List of adjacency lists:  list containg |V| lists
		self.Adj  =  { vertex: [] for label, vertex in self.V.items() }

		# matrix representation
		self.Matrix = { v1: { v2: None for v2 in self.V.values() } for v1 in self.V.values() } 

		# Read the edges (pairs of labels) and create corresponding entries
		# in Adj
		for edge in e:
			v1, v2 = ( self.V[ edge[0] ], self.V[ edge[1] ])
			self.Adj[ v1 ].append( v2 )
			self.Matrix[ v1 ][ v2 ] = 1
			if not directed:
				self.Adj[v2].append( v1 )
				self.Matrix[ v2 ][ v1 ] = 1

			# storing weights in the matrix
			if (len(edge)>2):
				self.weighted = True
				self.Matrix[v1][v2] = edge[2]
				if not directed:
					self.Matrix[v2][v1]=edge[2]


		self.directed = directed

		self.time = 0
	

	def breadth_first(self,source, file_prefix='', blank=False ):
		""" Breadth-First search of the graph.

		:param source: label or index of the source vertex 
		:type source: str
		:param file_prefix: if provided, the procedure generates .dot diagrams for each step; dot filenames concatenate this prefix with a number suffix.
		:type file_prefix: str
		:param blank: if True, the procedure generates only .dot templates for each step; the colors and attributes of the node are not shown.
		:param blank: bool
		"""
		queue = []
		s = self.V[source ]
		s.distance = 0
		s.color = Vertex.GRAY
		queue.append( s )

		
		def queue_string(q):
			if blank:
				return 'Q='
			return 'Q={}'.format([vtx.label for vtx in q ])
	

		file_number = 0

		if file_prefix!='':
				file_number += self.to_dot_file( '{}{}'.format(file_prefix,file_number), legend=queue_string(queue), blank=blank)
		while queue:
			u = queue.pop()
			#print('Popping vertex {} with adjacency list: {}'.format(u.label, self.Adj[u]))
			for v in sorted( self.Adj[ u ], key=lambda x: x.label):
				log("\tVisiting vertex {}".format(v.label),3)
				
				if v.color == Vertex.WHITE:
					v.color = Vertex.GRAY
					v.distance = u.distance + 1
					v.pi = u
					queue.insert(0,v)

			u.color = Vertex.BLACK

			if file_prefix!='':
				file_number += self.to_dot_file( '{}{:02}'.format(file_prefix,file_number), legend=queue_string(queue), blank=blank)


		if file_prefix!='' and not blank:
			self.get_tree().to_dot_file( '{}{:02}'.format(file_prefix,file_number), legend=queue_string(queue))

			

	def depth_first(self, file_prefix='', blank=False):
		""" Depth-First search.

		:param file_prefix: if provided, the procedure generates .dot diagrams for each step; dot filenames concatenate this prefix with a number suffix.
		:type file_prefix: str
		:param blank: if True, the procedure generates only .dot templates for each step; the colors and attributes of the node are not shown.
		:param blank: bool
		"""	
		#log("Starting DFS...")
		time = 0


		def depth_first_visit(u, spacer=''):
			""" Recursive procedure, for depth-first search

			:param u: the vertex under examination
			:type u: Vertex
			"""
			nonlocal time
			time += 1	


			log(spacer+'depth_first_visit({}) at time {}:00'.format( u.label, time ),3)
			u.discovery = time
			u.color = Vertex.GRAY

			if file_prefix != '':
				self.to_dot_file( '{}{:02}'.format(file_prefix,time), Walk.DFS, blank=blank )

			for v in  sorted( self.Adj[ u ], key=lambda x: x.label):
				if v.color == Vertex.WHITE:
					v.pi = u
					depth_first_visit( v, spacer+'\t' )
					
			u.color = Vertex.BLACK
			#print('{}.color={}'.format( u.label, u.color))
			time += 1
			u.finish = time

			if file_prefix != '':
				self.to_dot_file( '{}{:02}'.format(file_prefix,time), Walk.DFS, blank=blank )

			log(spacer+'finish {} at time {}:00'.format( u.label, time ),3)

		for v in self.V.values():
			if v.color == Vertex.WHITE:
				depth_first_visit( v, '')
	
		if not blank and file_prefix != '':
			self.to_dot_file( '{}{:02}'.format(file_prefix,time), Walk.DFS, blank=blank)

			self.get_tree().to_dot_file( '{}{:02}'.format(file_prefix,time+1), Walk.DFS, blank=blank)
	

	def topo_sort(self, file_prefix='', blank=False):
		""" Topological sort: return a topologically sorted list of vertices.

		:param file_prefix: if provided, the procedure generates .dot diagrams for each step; dot filenames concatenate this prefix with a number suffix.
		:type file_prefix: str
		:param blank: if True, the procedure generates only .dot templates for each step; the colors and attributes of the node are not shown.
		:param blank: bool
		:return: a topologically sorted list of Vertex objects
		:rtype: list
		"""	
		#log("Starting topological sort...")

		time = 0

		def topo_string(lst):
			"""
			Display the content of the topologically sorted list
			"""
			if blank:
				return 'S='
			return 'Sorted list S=[{}]'.format(', '.join([ v.label for v in lst ]))

		def depth_first_topo(u, spacer=''): 
			""" Recursive procedure, for depth-first search.

			:param u: the vertex under examination
			:type u: Vertex
			:type topo: list
			"""
			nonlocal time
			time += 1	
			log(spacer+'depth_first_visit({}) at time {}:00'.format( u.label, time ),3)
			u.discovery = time
			u.color = Vertex.GRAY

			if file_prefix != '':
				self.to_dot_file( '{}{:02}'.format(file_prefix,time), Walk.DFS, legend=topo_string(topo),  blank=blank )

			for v in sorted( self.Adj[ u ], key=lambda x: x.label):
				if v.color == Vertex.WHITE:
					v.pi = u
					depth_first_topo( v, spacer+'\t' )
			u.color = Vertex.BLACK
			time += 1
			u.finish = time
			
			topo.insert(0, u)


			if file_prefix != '':
				self.to_dot_file( '{}{:02}'.format(file_prefix,time), Walk.DFS, legend=topo_string(topo), blank=blank )

			log(spacer+'finish {} at time {}:00'.format( u.label, time ),3)

		topo=[]

		for v in self.V.values():
			if v.color == Vertex.WHITE:
				depth_first_topo( v, '' )
		
		if not blank and file_prefix != '':
			self.to_dot_file( '{}{:02}'.format(file_prefix,time), Walk.DFS, legend=topo_string(topo), blank=blank)

			self.get_tree().to_dot_file( '{}{:02}'.format(file_prefix,time+1), Walk.DFS, blank=blank)

		return topo


	def dag_shortest_path(self, source, file_prefix='', blank=False):
		""" DAG Shortest path algorithm.

		:param source: source vertex
		:type source: str
		:param file_prefix: if provided, the procedure generates .dot diagrams for each step; dot filenames concatenate this prefix with a number suffix.
		:type file_prefix: str
		:param blank: if True, the procedure generates only .dot templates for each step; the colors and attributes of the node are not shown.
		:param blank: bool
		"""
		log("Starting DAG shortest path...",3)

		def topo_string(lst):
			"""
			Display the content of the topologically sorted list
			"""
			if blank:
				return 'S='
			return 'Sorted list S=[{}]'.format(', '.join([ v.label for v in lst ]))

		s = self.V[source]
		sorted_vertices = self.topo_sort()

		
		self.initialize_single_source(s)

		file_number=0
		if file_prefix != '':
			file_number+=self.to_dot_file( '{}{:02}'.format(file_prefix,file_number), Walk.DAGSP, legend=topo_string( sorted_vertices), blank=blank)

		while len(sorted_vertices)>0:

			u = sorted_vertices.pop(0)
			log("-- u={} -- ".format(u.label),3)

			for v in self.Adj[ u ]:
				self.relax(u, v)
			u.color=Vertex.BLACK

			if file_prefix != '':
				file_number += self.to_dot_file( '{}{:02}'.format(file_prefix,file_number), Walk.DAGSP, legend=topo_string( sorted_vertices), blank=blank)
				

		if file_prefix!='' and not blank:
			self.get_tree().to_dot_file( '{}{:02}'.format(file_prefix,file_number), Walk.DAGSP) 


	def initialize_single_source(self, s):
		""" Initialize the graph.

		:param s: source vertex
		:type s: Vertex
		"""
		for label, v in self.V.items():
			v.color=Vertex.WHITE
			v.distance = Vertex.INFTY
			v.pi = None
		s.distance = 0

	def dijkstra(self, s, file_prefix='', blank=False):
		""" Dijkstra's shortest path algorithm.

		:param s: source vertex (a label)
		:type s: str
		:param file_prefix: if provided, the procedure generates .dot diagrams for each step; dot filenames concatenate this prefix with a number suffix.
		:type file_prefix: str
		:param blank: if True, the procedure generates only .dot templates for each step; the colors and attributes of the node are not shown.
		:param blank: bool
		"""

		def queue_string(q):
			if blank:
				return 'minQ='
			return 'minQ={}'.format(', '.join([vtx.label for vtx in q.list() ]))

		#log("Starting Dijkstra...")
		self.initialize_single_source( self.V[s] )
		S = []

		minQueue = MinHeap( self.V.values() )

		file_number=0

		if file_prefix!='':
				file_number += self.to_dot_file( '{}{}'.format(file_prefix, file_number),#
								legend=queue_string(minQueue),
								blank=blank)
		while minQueue.size > 0:
			u = minQueue.extract_min()
			u.color=Vertex.BLACK
			log("Extract vertex {} (d={})".format(u.label, u.distance),3)
			S.append( u )
			for v in self.Adj[ u ]:
				self.relax( u, v )

			if file_prefix!='':
				file_number += self.to_dot_file( '{}{:02}'.format(file_prefix,file_number),#
								legend=queue_string(minQueue),
								blank=blank)
		
	
		if not blank and file_prefix != '':
			self.get_tree().to_dot_file( '{}{:02}'.format(file_prefix,file_number), Walk.DIJKSTRA, blank=blank)
			


	def relax(self, u, v ):
		"""
		Relax vertex v through u

		:param u: vertex u
		:param v: vertex v
		:type u: Vertex
		:type v: Vertex
		"""
		if v.distance > (u.distance + self.Matrix[u][v] ):
			log('relax({},{}): {} --> {}'.format(u.label, v.label, v.distance, (u.distance + self.Matrix[u][v])),3)
			v.distance = (u.distance + self.Matrix[u][v] )

			if hasattr(v,'heap') and v.heap is not None:
				v.float_key( v.heap_index )
			v.pi = u


	def unique_edges(self):
		"""
		"""

		checked_matrix = { v1: { v2: False for v2 in self.V.values() } for v1 in self.V.values() }
		edges = []

		for u in self.V.values():
			for v in self.Adj[u]:
				if not self.directed:
					if not checked_matrix[u][v] and not checked_matrix[v][u]:
						checked_matrix[u][v]=True
						checked_matrix[v][u]=True
						edges.append( (u,v) )
				else:
					edges.append( (u,v) )
		return edges


	def to_dot_file(self, filename, walk=Walk.BFS, legend='', blank=False):
		"""
		Dump the graph to a dot file.
		
		:param filename: the file to be written
		:type filename: str
		:param walk: the family of algorithms (DFS or BFS), that determines the information to be displayed with a node label (distances or discovery:finish times)
		:type walk: Walk
		:param legend: an optional string to be added to the graph (a caption, or the state of data structure)
		:type legend: str
		"""
		out = open('{}.dot'.format( filename), 'w')
		out.write( self.to_dot(walk, legend, blank=blank))
		out.close()
		return 1


	def to_dot(self, walk, legend='', blank=False):
		"""
		Return a string representation of the graph, in dot format.

		:param walk: the family of algorithms (DFS or BFS), that determines the information to be displayed with a node label (distances or discovery:finish times)
		:type walk: Walk
		:param legend: an optional string to be added to the graph (a caption, or the state of data structure)
		:type legend: str
		:return: a string representation of the graph, in DOT (Graphviz) format
		:rtype: str
		"""
		gs = []

		if self.directed:
			gs.append('Digraph {')
		else:
			gs.append( 'Graph {' )
		
		for v in self.V.values():
			gs.append( v.to_dot(walk, blank) )	

		for edge in self.unique_edges():
			u,v = edge
			penwidth=1 
			if self.directed:
				if not blank and v.pi is u:
					penwidth=3
				gs.append( '{}->{}[label="{}", penwidth={}];'.format(u.label, v.label, self.Matrix[u][v] if self.weighted else '', penwidth))
			else:
				if not blank and u.pi is v or v.pi is u:
					penwidth=3
				gs.append( '{}--{}[label="{}", penwidth={}];'.format(u.label, v.label, self.Matrix[u][v] if self.weighted else '', penwidth))
		if legend != '':
			gs.append( 'label="{}" fontname="DejaVu Serif"'.format( legend ))
		
		gs.append( '}')

		return('\n'.join(gs))


	def to_tree(self):
		"""After DFS or BFS, remove the edges that are not in the resulting subgraph.

		"""
		edges_to_remove=[]

		for u,lst in self.Adj.items():
			for v in lst:
				if v.pi is not u:
					edges_to_remove.append( (u, v) )

		for edge in edges_to_remove:
			u,v=edge
			self.Adj[u].remove(v)
			self.Matrix[u][v]=None
		for v in self.V.values():
			v.color = Vertex.WHITE

	def get_tree(self):
		
		g = self.copy()
		g.to_tree()
		return g

	@classmethod
	def from_dot_to_lists(cls, dotfile):
		"""
		Load a graph from a dot file, and construct lists of vertices and edges.

		:param dotfile: the name of a graph-definition file, in DOT format.
		:type dotfile: str
		:return: a pair: the first element is a list of vertex labels, the second is a list of edges (pairs of labels)
		:rtype: tuple
		"""
		pass
		

	@classmethod
	def from_dot( cls, dotfile ):
		"""
		Load a graph from a dot file.

		:param dotfile: the name of a graph-definition file, in DOT format.
		:type dotfile: str
		:return: a Graph object;  an edge numerical label in the dot file is interpreted as an edge weight.
		:rtype: Graph
		"""
		gf = open(dotfile, 'r')
		
		directed=False

		v=[]
		e=[]
		
		# 'Digraph {' or 'Graph {'
		graph_re = re.compile(r'(Digraph|Graph)\s*{')

		# 'u [ label="u:3" style=filled fontname="time-bold" fillcolor=gray52 ];'
		vertex_re = re.compile(r"^\s*(\w+)\s*\[.*\]\s*;")


		# 'w--s[label="", penwidth=3];' or 'w--s[label="7", penwidth=3];
		edge_re = re.compile(r'^\s*(\w+)\s*-[->]\s*(\w+)\s*(\[.*\])?\s*;')

		label_re = re.compile(r'.*label="(-?\d+)".*')

		for line in gf:
			v_match = vertex_re.match( line )
			e_match = edge_re.match( line )
			g_match = graph_re.match( line )
			if g_match and g_match.group(1)=='Digraph':
				directed=True
			if v_match:
				v.append( v_match.group(1) )
			elif e_match:
				#print(e_match, e_match.lastindex)
				v1,v2  = e_match.group(1), e_match.group(2)
				if not directed and v1 > v2:
						v2,v1 = v1,v2
				weight=None
				if e_match.lastindex==3:
						label_match = label_re.match( e_match.group(3) )
						if label_match:
							#print("Found weight")
							e.append( ( v1, v2, int(label_match.group(1))))
						else: e.append( (v1,v2) )
				else:
					e.append( (v1, v2))
		gf.close()			

		return cls(v, e, directed)
		

	def copy(self):
		"""
		Return a copy of this graph.

		The vertex and edge attributes of the new graph are the vertex and edge attributes of the original graph at the time of the copy.
		:return: a graph that has the same vertex set and the same edges.
		:rtype: Graph
		"""
		g = self.__class__( directed=self.directed )
		for label, vtx in self.V.items():
			g.V[label]=vtx.copy()
		# so far, parent pointers still point to the original
		# vertices: we need to update them
		for lbl,vtx in g.V.items():
			if vtx.pi is not None:
				vtx.pi = g.V[vtx.pi.label]
			

		for u, l in self.Adj.items():
			g_u = g.V[u.label]
			g.Adj[g_u] = [ g.V[v.label] for v in self.Adj[u] ]

		g.Matrix = { v1: { v2: None for v2 in g.V.values() } for v1 in g.V.values() } 
		for u in self.Matrix.keys():
			for v in self.Matrix[u]:
				g_u = g.V[u.label]
				g_v = g.V[v.label]
				g.Matrix[g_u][g_v]=self.Matrix[u][v]
		log(g,3)
		return g	
	

	def load_coordinates(self, template):
		
		cf = open( template, 'r')	

		width_re = re.compile('^\s*(\d+)\s*$')
		empty_re = re.compile('^\s*$')

		width = 0

		# array of reversed grid rows
		grid = []
		
		for line in cf:
			width_match = width_re.match( line )
			if width_match:
				width = width_match.group(0)
			elif not empty_re.match(line):
				grid.insert(0, line )
		cf.close()
			

		print( grid )
		print(self.V.keys())
		# reading the grid rows
		for r in range(0, len(grid)):
			vertices = [ label.strip() for label in grid[r].split('&') ]
			print(vertices)
			for c in range(0,len(vertices)):
				if vertices[c] != '':
					self.V[ vertices[c] ].coord = (c, r)
			
			
		
		
		
	
	def __str__(self):
		output = 'V=['
		for v in self.V:
			output += str(v)+'\n'	
		output += ']\n'
		for u in self.Adj.keys():
			output += '{}: '.format(u)
			for v in self.Adj[u]:
				output += ' {}'.format(v)
			output += '\n'
		return output

		
class GraphUnitTest( unittest.TestCase ):


	def atest_weight_graph_creation(self):

		g = self.make_dijkstra_graph()
		#print('{}'.format(g.Matrix))
		#self.assertEqual( g.Matrix[0][1], 10)
		#self.assertEqual( g.Matrix[0][3], 5)


	def atest_dag_shortest_path_1(self):
		""" Cormen Figure 24.5, p. 656 """
		g = self.make_weighted_dag()
		g.dag_shortest_path('s') 

		self.assertEqual( g.V['z'].pi, g.V['y'])
		self.assertEqual( g.V['y'].pi, g.V['x'])
		self.assertEqual( g.V['x'].pi, g.V['s'])
		self.assertEqual( g.V['t'].pi, g.V['s'])


	def atest_dag_shortest_path_2(self):
		""" Cormen Figure 24.5, p. 656 """
		g = self.make_weighted_dag()
		g.dag_shortest_path('s') 

		self.assertEqual( g.V['z'].distance, 3)
		self.assertEqual( g.V['y'].distance, 5)
		self.assertEqual( g.V['x'].distance, 6)
		self.assertEqual( g.V['t'].distance, 2)
		self.assertEqual( g.V['s'].distance, 0)
		self.assertEqual( g.V['r'].distance, Vertex.INFTY)

	def atest_dag_shortest_path_3(self):
		g = self.make_weighted_dag_2()
		g.dag_shortest_path('b') 

		self.assertEqual( g.V['g'].pi, g.V['f'])
		self.assertEqual( g.V['f'].pi, g.V['d'])
		self.assertEqual( g.V['e'].pi, g.V['c'])
		self.assertEqual( g.V['d'].pi, g.V['b'])
		self.assertEqual( g.V['c'].pi, g.V['b'])

	def atest_dag_shortest_path_4(self):
		g = self.make_weighted_dag_2()
		g.dag_shortest_path('b') 

		self.assertEqual( g.V['g'].distance, 2)
		self.assertEqual( g.V['f'].distance, 1)
		self.assertEqual( g.V['e'].distance, 3)
		self.assertEqual( g.V['d'].distance, 3)
		self.assertEqual( g.V['c'].distance, 4)
		self.assertEqual( g.V['b'].distance, 0)
		self.assertEqual( g.V['a'].distance, Vertex.INFTY)

	def atest_dijkstra_1(self):
		""" Cormen Figure 24.6, p. 659 """
		g = self.make_dijkstra_graph()
		g.dijkstra( 's' )		

		self.assertEqual( g.V['s'].distance, 0)
		self.assertEqual( g.V['t'].distance, 8)
		self.assertEqual( g.V['x'].distance, 9)
		self.assertEqual( g.V['y'].distance, 5)
		self.assertEqual( g.V['z'].distance, 7)

	def atest_dijkstra_2(self):
#		""" Cormen Figure 24.6, p. 659 """
		g = self.make_dijkstra_graph()
		g.dijkstra( 's' )		
#
		self.assertEqual( g.V['s'].pi, None)
		self.assertEqual( g.V['t'].pi, g.V['y'])
		self.assertEqual( g.V['x'].pi, g.V['t'])
		self.assertEqual( g.V['y'].pi, g.V['s'])
		self.assertEqual( g.V['z'].pi, g.V['y'])
#
	def atest_dijkstra_3(self):
#		""" Gross & Yellen, p. 180 """
		g = self.make_dijkstra_graph_2()
		g.dijkstra( 's' )		
#
		self.assertEqual( g.V['s'].distance, 0)
		self.assertEqual( g.V['a'].distance, 5)
		self.assertEqual( g.V['b'].distance, 7)
		self.assertEqual( g.V['c'].distance, 13)
		self.assertEqual( g.V['d'].distance, 12)
		self.assertEqual( g.V['e'].distance, 4)
		self.assertEqual( g.V['f'].distance, 12)
		self.assertEqual( g.V['g'].distance, 5)
#
	def atest_dijkstra_4(self):
#		""" Gross & Yellen, p. 180 """
		g = self.make_dijkstra_graph_2()
		g.dijkstra( 's' )		

		self.assertEqual( g.V['s'].pi, None)
		self.assertEqual( g.V['a'].pi, g.V['s'])
		self.assertEqual( g.V['b'].pi, g.V['s'])
		self.assertEqual( g.V['c'].pi, g.V['e'])
		self.assertEqual( g.V['d'].pi, g.V['e'])
		self.assertEqual( g.V['e'].pi, g.V['s'])
		self.assertEqual( g.V['f'].pi, g.V['e'])
		self.assertEqual( g.V['g'].pi, g.V['s'])
#
	def atest_dijkstra_5(self):
#		""" Gross & Yellen, p. 180, directed version """
		g = self.make_dijkstra_graph_3()
		g.dijkstra( 's' )		

		self.assertEqual( g.V['s'].distance, 0)
		self.assertEqual( g.V['a'].distance, 4)
		self.assertEqual( g.V['b'].distance, 7)
		self.assertEqual( g.V['c'].distance, 7)
		self.assertEqual( g.V['d'].distance, 7)
		self.assertEqual( g.V['e'].distance, 3)
		self.assertEqual( g.V['f'].distance, 9)
		self.assertEqual( g.V['g'].distance, 8)
#
	def atest_dijkstra_6(self):
#		""" Gross & Yellen, p. 180, directed version """
		g = self.make_dijkstra_graph_3()
		g.dijkstra( 's' )		

		self.assertEqual( g.V['s'].pi, None)
		self.assertEqual( g.V['a'].pi, g.V['e'])
		self.assertEqual( g.V['b'].pi, g.V['s'])
		self.assertEqual( g.V['c'].pi, g.V['e'])
		self.assertEqual( g.V['d'].pi, g.V['e'])
		self.assertEqual( g.V['e'].pi, g.V['s'])
		self.assertEqual( g.V['f'].pi, g.V['c'])
		self.assertEqual( g.V['g'].pi, g.V['a'])

	def atest_breadth_first_1(self):
		g = self.make_sample_undirected_graph()

		g.breadth_first( 'a' )

		self.assertEqual(g.vertex('a').distance,0)

	def atest_topological(self):
		g = self.make_dag()

		g.topo_sort()

	
	def atest_depth_first_1(self):
		"""" Discovery time """
		g = self.make_sample_undirected_graph()

		g.depth_first()

		self.assertEqual(g.V['a'].discovery, 1)
		self.assertEqual(g.V['b'].discovery, 2)
		self.assertEqual(g.V['c'].discovery, 3)
		self.assertEqual(g.V['d'].discovery, 4)
		self.assertEqual(g.V['e'].discovery, 5)
		self.assertEqual(g.V['f'].discovery, 11)
		self.assertEqual(g.V['g'].discovery, 7)
		self.assertEqual(g.V['h'].discovery, 6)

	def atest_depth_first_2(self):
		"""" Finish time """
		g = self.make_sample_undirected_graph()

		g.depth_first()

		self.assertEqual(g.V['a'].finish, 16)
		self.assertEqual(g.V['b'].finish, 15)
		self.assertEqual(g.V['c'].finish, 14)
		self.assertEqual(g.V['d'].finish, 13)
		self.assertEqual(g.V['e'].finish, 10)
		self.assertEqual(g.V['f'].finish, 12)
		self.assertEqual(g.V['g'].finish, 8)
		self.assertEqual(g.V['h'].finish, 9)


	def atest_depth_first_3(self):
		"""" Digraph: discovery time """
		g = self.make_sample_digraph_2()

		g.depth_first()

		self.assertEqual(g.V['a'].discovery, 1)
		self.assertEqual(g.V['b'].discovery, 2)
		self.assertEqual(g.V['c'].discovery, 3)
		self.assertEqual(g.V['d'].discovery, 4)
		self.assertEqual(g.V['e'].discovery, 9)
		self.assertEqual(g.V['f'].discovery, 13)
		self.assertEqual(g.V['g'].discovery, 5)
		self.assertEqual(g.V['h'].discovery, 10)
		self.assertEqual(g.V['i'].discovery, 17)
		self.assertEqual(g.V['j'].discovery, 18)

	def atest_depth_first_4(self):
		"""" Digraph: finish time """
		g = self.make_sample_digraph_2()

		g.depth_first()

		self.assertEqual(g.V['a'].finish, 16)
		self.assertEqual(g.V['b'].finish, 15)
		self.assertEqual(g.V['c'].finish, 8)
		self.assertEqual(g.V['d'].finish, 7)
		self.assertEqual(g.V['e'].finish, 12)
		self.assertEqual(g.V['f'].finish, 14)
		self.assertEqual(g.V['g'].finish, 6)
		self.assertEqual(g.V['h'].finish, 11)
		self.assertEqual(g.V['i'].finish, 20)
		self.assertEqual(g.V['j'].finish, 19)

	def atest_breadth_first_1(self):
		"""" Predecessors """
		g = self.make_sample_undirected_graph()

		g.breadth_first( 'a' )

		# predecessor of H is E
		self.assertEqual(g.V['h'].pi, g.V['e'] )
		self.assertEqual(g.V['g'].pi, g.V['d'] )
		self.assertEqual(g.V['f'].pi, g.V['b'] )
		self.assertEqual(g.V['e'].pi, g.V['b'] )
		self.assertEqual(g.V['c'].pi, g.V['a'] )
		self.assertEqual(g.V['b'].pi, g.V['a'] )
		self.assertEqual(g.V['d'].pi, g.V['a'] )
	
	def atest_breadth_first_2(self):
		"""" Distances """
		g = self.make_sample_undirected_graph()

		g.breadth_first( 'a' )

		self.assertEqual(g.V['a'].distance, 0)
		self.assertEqual(g.V['b'].distance, 1)
		self.assertEqual(g.V['c'].distance, 1)
		self.assertEqual(g.V['d'].distance, 1)
		self.assertEqual(g.V['e'].distance, 2)
		self.assertEqual(g.V['f'].distance, 2)
		self.assertEqual(g.V['g'].distance, 2)
		self.assertEqual(g.V['h'].distance, 3)
	
	
	def atest_breadth_first_3(self):
		"""" Digraph: predecessors """
		g = self.make_sample_digraph()

		g.breadth_first( 'a' )

		# predecessor of H is E
		self.assertEqual(g.V['h'].pi, g.V['e'] )
		self.assertEqual(g.V['g'].pi, g.V['d'] )
		self.assertEqual(g.V['f'].pi, g.V['b'] )
		self.assertEqual(g.V['e'].pi, g.V['b'] )
		self.assertEqual(g.V['c'].pi, g.V['b'] )
		self.assertEqual(g.V['b'].pi, g.V['a'] )
		self.assertEqual(g.V['d'].pi, g.V['a'] )
	
	def atest_breadth_first_4(self):
		"""" Digraph: distances """
		g = self.make_sample_digraph()

		g.breadth_first( 'a' )

		self.assertEqual(g.V['a'].distance, 0)
		self.assertEqual(g.V['b'].distance, 1)
		self.assertEqual(g.V['c'].distance, 2)
		self.assertEqual(g.V['d'].distance, 1)
		self.assertEqual(g.V['e'].distance, 2)
		self.assertEqual(g.V['f'].distance, 2)
		self.assertEqual(g.V['g'].distance, 2)
		self.assertEqual(g.V['h'].distance, 3)
	
	def atest_graph_creation_1(self):
		print("Test create undirected graph")
		
		g = self.make_sample_undirected_graph()

	def atest_graph_creation_2(self):
		
		g = self.make_sample_undirected_graph()
		
	def atest_graph_creation_3(self):
		print("Test create directed graph")
		
		g = self.make_sample_digraph()

	
	def test_load_from_template(self):

		g = Graph(('m','n','o','p','q','r','s','t','u','v','w','x','y','z'),
			(('m','q'),('m','r'),('m','x'),('n','o'),('n','q'),('n','u'),('o','r'),('o','s'),('o','v'),
			('p','o'),('p','s'),('p','z'),('q','t'),('r','u'),('r','y'),('s','r'),('u','t'),('v','w'),('v','x'),
			('y','v')),
			directed=True
		)
	
		g.load_coordinates('examples/dag_228_clrs.template')

		self.assertEqual(g.V['m'].coord, (0,3))
		self.assertEqual(g.V['n'].coord, (2,3))
		self.assertEqual(g.V['o'].coord, (4,3))
		self.assertEqual(g.V['p'].coord, (6,3))
		self.assertEqual(g.V['q'].coord, (1,2))
		self.assertEqual(g.V['r'].coord, (3,2))
		self.assertEqual(g.V['s'].coord, (5,2))
		self.assertEqual(g.V['t'].coord, (0,1))
		self.assertEqual(g.V['u'].coord, (2,1))
		self.assertEqual(g.V['v'].coord, (4,1))
		self.assertEqual(g.V['w'].coord, (6,1))
		self.assertEqual(g.V['x'].coord, (1,0))
		self.assertEqual(g.V['y'].coord, (3,0))
		self.assertEqual(g.V['z'].coord, (5,0))


	@classmethod
	def make_sample_undirected_graph(cls):
		
		g = Graph( 
			('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'), 
			(	('a','b'), ('a','c'), ('a','d'), 
				('b','a'),('b','c'),('b','e'),('b','f'), 
				('c','a'),('c','b'),('c','d'),('c','f'), 
				('d','a',),('d','c'),('d','e'),('d','f'),('d','g'),
				('e','b'),('e','d'),('e','h'), 
				('f','b'),('f','c'),('f','d'), 
				('g','d'),('g','h'), 
				('h','e'),('h','g')))
		return g

	@classmethod
	def make_clrs_bfs_undirected_graph(cls):
		g = Graph(
			('r','s','t','u','v','w','x','y'),
			(('r','s'),('r','v'),
			('s','w'),('w','t'),('w','x'),
			('t','x'),('t','u'),('u','x'),
			('u','y'),('x','y')
			),
		)
		return g

	@classmethod
	def make_sample_digraph(cls):
		
		g = Graph( 
			('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'), 
			(	('a','b'), ('a','d'), 
				('b','c'),('b','e'),('b','f'), 
				('c','a'),('c','d'),
				('d','g'), 
				('e','d'),('e','h'), 
				('f','c'),('f','d'), 
				('h','g')), directed=True)
		return g

	@classmethod
	def make_sample_digraph_2(cls):
		
		g = Graph( 
			('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'), 
			(	('a','b'), ('a','d'), 
				('b','c'),('b','e'),('b','f'), 
				('c','a'),('c','d'),
				('d','g'), 
				('e','d'),('e','h'), 
				('f','c'),('f','d'), 
				('h','g'),
				('i','g'),('i','j'),
				('j','j')), directed=True)
		return g

	@classmethod
	def make_dag(cls):
		g = Graph(
			('undershorts', 'pants','belt','socks','shoes','watch','shirt','tie','jacket'),
			( 	('undershorts','pants'),
			 	('undershorts','shoes'),
				('pants','belt'),
				('pants','shoes'),
				('belt','jacket'),
				('shirt','belt'),
				('shirt','tie'),
				('socks','shoes')), directed=True)
		return g


	@classmethod
	def make_dijkstra_graph(cls):
		""" Cormen Figure 24.6, p. 659 """
		g = Graph(
			('s', 't', 'x', 'y', 'z'),
			(	('s','t',10), ('s','y',5),
				('t','x',1), ('t','y',2),
				('x','z',4),
				('y','t',3),('y','x',9),('y','z',2),
				('z','s',7),('z','x',6)),
				directed=True)
		return g
	
	@classmethod
	def make_dijkstra_graph_2(cls):
		""" Gross & Yellen, p. 180 """
		g = Graph(
			('s', 'a', 'b', 'c', 'd', 'e', 'f', 'g'),
			(	('s','a',5),('s','b',7), ('s','e',4),('s','g',5),
				('a','s',5),('a','g',4),
				('b','s',7),('b','c',9),('b','f',8),
				('c','b',9),('c','d',7),('c','e',9),('c','f',11),
				('d','e',8),('d','c',7),
				('e','s',4),('e','c',9),('e','d',8),('e','f',8),
				('f','b',8),('f','c',11),('f','e',8),
				('g','s',5),('g','a',4)))
		return g
	
	
	@classmethod
	def make_dijkstra_graph_3(cls):
		""" Gross & Yellen, p. 180, modified (directed) """
		g = Graph(
			('s', 'a', 'b', 'c', 'd', 'e', 'f', 'g'),
			(	('s','a',5),('s','b',7), ('s','e',3),
				('a','g',4),
				('b','c',9),('b','f',8),
				('c','d',7),('c','f',2),
				('d','e',8),('d','c',1),
				('e','a',1),('e','c',4),('e','d',4),('e','f',12),
				('f','c',11),
				('g','s',5)), directed=True)
		return g
	
	

	@classmethod
	def make_weighted_dag(cls):
		""" Cormen Figure 24.5, p. 656 """
		g = Graph(
			('r', 's', 't', 'x', 'y', 'z'),
			(	('r','s',5),('r','t',3),
				('s','t',2),('s','x',6),
				('t','x',7),('t','y',4),('t','z',2),
				('x','y',-1),('x','z',1),
				('y','z',-2)
			), directed=True
		)
		return g
	
	@classmethod
	def make_weighted_dag_2(cls):
		g = Graph(
			('a', 'b', 'c', 'd', 'e', 'f', 'g'),
			(	('a','b',8),('a','d',1),
				('b','c',4),('b','d',3),
				('c','d',5),('c','e',-1),('c','f',2),
				('d','e',6),('d','f',-2),
				('e','f',1),('e','g',3),
				('f','g',1)
			), directed=True
		)
		return g
	

def main():
        unittest.main()

if __name__ == '__main__':
        main()


