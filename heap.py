#!/usr/bin/python3

import unittest
import sys

class MaxHeap(object):
	""" A heap-beased priority queue implementation. This is a generic priority queue structure:
		- it is initialized with the array of objects to be prioritized
		- any object attribute can be used as a comparison key (thus determining the position in the queue), by overriding the `__gt(obj1, obj2)__` ( obj1 > obj2 ) method in the object definition 
		- the priority queue maintains its own list of references to the object contained in the array passed in at the queue creation: this means that objects can be safely moved through the queue without affecting the order of the array passed in.

	For instance, in order to construct a Max-Priority queue out of a list of Vertex objects, that uses  the `distance` attribute for a comparison key:

	1. First override the inherited `__gt(obj1, obj2)__` method on the Vertex object::


		def __gt__(self, other):
			if isinstance(other, Vertex):
				return self.distance > other.distance
			return NotImplemented

	2. Then, in the `Graph` class (assuming that the vertex set is stored as a dictionary, where vertex references are keys in the dictionary `V`),  construct a new queue, with the following line::

		myMaxQueue = MaxHeap( self.V.values() ) 

	3. To use the queue::

		next_vertex = myMaxQueue.extract_max()

	In order to construct a Min-Priority queue, just use the `MinHeap()` constructor instead (there is no need to change the `__gt__` function), and call the appropriate method: `extract_min()`.
	
	"""

	def __init__(self, array):
		""" Create a new MaxHeap from an existing array.

		The newly created heap does not affect the original array.
		
		:param array: an array of objects, or numbers
		:type array: list
		"""
		# this ensures that we not manipulating the same items, in a
		# _new array_ (the original array stays untouched)
		self.array = [ item for item in array ]
		self.size = 0
		self.custom_type = False
		if not isinstance(self.array[0],(int,float,str)):
			self.custom_type = True

		self.build_heap()
	
	def list(self):
		"""
		Return a sorted list of the elements that are still in the heap.

		:return: a sorted list of values
		:rtype: list
		"""
		if self.is_empty():
			print("empty queue!", file=sys.stderr)
			return []
		return sorted(self.array[:self.size])




	def build_heap(self):
		""" Build a heap from an array of primitive types, or custom objects.

		If elements in the array are custom objects, decorate them with the following attributes
			- heap_index: keep track of the object position in the heap array
			- heap: a back reference to the heap itself
			- float_key(i): the decrease/increase key function
		 """
		self.size = len(self.array)
		for i in reversed (range (0, (len(self.array))//2)):
			self.heapify(i)

		# Add a heap-friendly attributes to the type being manipulated
		if self.custom_type:
			for idx in range(0, len(self.array)):
				self.array[idx].heap_index = idx		
				self.array[idx].heap = self
				self.array[idx].float_key = lambda x: self.float_key( x )
	
	
	def heapify(self, i):
		""" Float a key down the tree.

 		It can be used for Max and Min heaps, with the proper definition for the method self._compare().

		:param i: index in the heap array
		:type i: int
		"""

		l = self.left(i)
		r = self.right(i)
		#print 'l={}, r={}'.format(l,r)
		largest = i
		if l <= self.size-1 and self._compare(self.array[l], self.array[i]):
			largest = l
		if r <= self.size-1 and self._compare(self.array[r], self.array[largest]):
			largest = r
		if largest != i:
			temp = self.array[largest]
			self.array[largest] = self.array[i]
			self.array[i] = temp 

			if self.custom_type:
				self.array[largest].heap_index = largest
				self.array[i].heap_index = i

			self.heapify(largest)

	def float_key(self, i):
		"""
		Float a key up in the tree.

		This method does _not_ update the key: it just maintains the heap property after the key has been increased (MaxHeap) or decreased (MinHeap)

		:param i: index of the element whose key needs to float up.
		:type i: int
		"""
		parent_idx = self.parent(i)
		while i > 0 and self._compare(self.array[i], self.array[ self.parent(i) ]) :
			tmp = self.array[i]
			self.array[i] = self.array[ self.parent(i) ] 
			self.array[ self.parent(i) ] = tmp

			if self.custom_type:
				self.array[i].heap_index = i
				self.array[self.parent(i) ].heap_index = self.parent(i)

			i = self.parent(i)

	def extract_max(self):
		""" Extract the element with the largest key.

		:rtype: object
		"""
		
		return self.extract_first()

	def extract_first(self):
		"""
		Extract the top element in the heap.

		:rtype: object
		"""
		#if self._compare(0, 1):
			#print('extract_min( {} )'.format(self))
		#else:
		#	print('extract_max( {} )'.format(self))

		if self.size<1:
			raise Exception
		first = self.array[0]
		self.array[0] = self.array[self.size-1]

		if self.custom_type:
			self.array[0].heap_index = 0

		self.size -= 1
		self.heapify(0) 

		return first 

	def is_empty(self):
		""" Check if the queue is empty.

		:return: Return true if the priority queue is empty; false otherwise.
		:rtype: boolean
		"""
		return self.size == 0

	def sort(self):
		"""
		Sort in place
		""" 
		if len(self.array)==0:
			return
		while(self.size>1):
			# swap last with first
			tmp = self.array[ self.size-1 ]
			self.array[self.size-1] = self.array[0]
			self.array[0] = tmp
			self.size -= 1
			self.heapify(0)
			#print('{}'.format(self)) 
			

	def _compare(self, a1, a2):
		return a1 > a2

	def left(self, i):
		return 2*(i+1)-1

	def right(self, i):
		return 2*(i+1)

	def parent(self, i):
		return i//2

	def __str__(self):
		return '{}'.format([ str(item) for item in self.array[0:(self.size)] ])


class MinHeap( MaxHeap ):
	def _compare(self, a1, a2):
		return a2 > a1

	def extract_min(self):
		""" Extract the element with the smallest key.

		:rtype: object
		"""
		return self.extract_first()


class HeapUnitTest( unittest.TestCase ):

	def test_max_heap_creation_1(self):
		""" MaxHeap creation """
		h = MaxHeap([1,2,3,4,7,8,9,10,14,16] )
		self.assertEqual( h.array, [16, 14, 9, 10, 7, 8, 3, 1, 4, 2])

	def test_max_heap_creation_2(self):
		""" MaxHeap creation (Nodes) """
		h = MaxHeap([Node(1),Node(2),Node(3),Node(4),Node(7),Node(8),Node(9),Node(10),Node(14),Node(16)] )
		self.assertEqual( [ h.array[0].key, h.array[1].key,h.array[2].key,h.array[3].key ], [16, 14, 9, 10 ])

	def test_min_heap_creation_1(self):
		""" MinHeap creation"""
		h = MinHeap([16,14,10,9,8,7,4,3,2,1] )
		self.assertEqual( h.array, [1, 2, 4, 3, 8, 7, 10, 16, 9, 14])

	def test_min_heap_creation_2(self):
		""" MinHeap creation (nodes)  """
		h = MinHeap([Node(16),Node(14),Node(10),Node(9),Node(8),Node(7),Node(4),Node(3),Node(2),Node(1)] )
		self.assertEqual( [ h.array[0].key, h.array[1].key,h.array[2].key,h.array[3].key ], [1, 2, 4, 3 ])

	
	def test_min_queue_1(self):
		""" MinQueue creation (nodes)  """
		h = MinHeap([Node(16),Node(14),Node(10),Node(9),Node(8),Node(7),Node(4),Node(3),Node(2),Node(1)] )
		self.assertEqual( h.extract_min().key, 1 )

	def test_min_queue_2(self):
		""" MinQueue creation (nodes)  """
		h = MinHeap([Node(16),Node(14),Node(10),Node(9),Node(8),Node(7),Node(4),Node(3),Node(2),Node(1)] )
		h.extract_min()
		self.assertEqual( h.size, 9 )

	def test_heapsort(self):
		h = MinHeap( [ 1,3,2,4,6,5,11,10,15,9 ])
		h.sort()
		self.assertEqual( h.array, [15,11,10,9,6,5,4,3,2,1])

class Node(object):
	def __init__(self,key):
		self.key = key

	def __str__(self):
		return str(self.key)

	def __gt__(self, other):
		return self.key > other.key

def main():
	unittest.main()

if __name__ == '__main__':
	main()

