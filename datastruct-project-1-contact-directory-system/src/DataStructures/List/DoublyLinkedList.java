package DataStructures.List;

import java.util.Iterator;

/**
 * I have decided to-implement a doubly linked list with dummy head/tail from scratch in order to see how good I can make it by myself.
 * I also used DoublyLinkedList because that's the default for the test cases.
 * 
 * @author DanielFebles
 * @param <E>
 */
public class DoublyLinkedList<E> implements List<E>{
	
		@SuppressWarnings("unused")
		
		/**
		 * Node class that I need for the list, including the necessary
		 * variables, constructors, and any methods I will or might
		 * need to use.
		 * 
		 * @param <E>	The givent type that the container should hold
		 */
		private class Node<E>{
			/**
			 * Variable responsible for linking the nodes together
			 * and containing the given element E.
			 * 
			 * @var next	Points to the node following this one.
			 * @var prev	Points to the node preceding this one.
			 * @var elm		Contains an element of the decleared type E>
			 */
			private Node<E> next;
			private Node<E> prev;
			private E elm;
			
			/**
			 * Three constructors for the node: a generic one,
			 * one with elm defined, and another with all
			 * parameters defined. Bon-defined parameters
			 * are set to null.
			 * 
			 * @param elm		Sets the initial object in the node.
			 * @param prev,next	Sets the pointers for the node.
			 */
			public Node() {
				next = null;
				prev = null;
				elm = null;
			}
			public Node(E elm) {
				next = null;
				prev = null;
				this.elm = elm;
			}
			public Node(Node<E> next, Node<E> prev, E elm) {
				this.next = next;
				this.prev = prev;
				this.elm = elm;
			}

			/**
			 * Getters and setters for each variable respectively
			 * 
			 * @return next, prev, elm	The respective variable it contains.
			 * @param next, prev, elm	Replaces the respective variable.
			 */
			public Node<E> getNext(){ return next;}
			public Node<E> getPrev(){ return prev;}
			public E getElm() { return elm;}
			public void setNext(Node<E> next) { this.next = next;}
			public void setPrev(Node<E> prev) { this.prev = prev;}
			public void setElm(E elm) { this.elm = elm;}
			public void clear() {next = null; prev = null; elm = null;}
		
		}
		
		/**
		 * Now to set up the doubly linked list itself. The three
		 * variables I will be using will be the size of the list,
		 * the head, and the tail, with the latter two being dummies.
		 * 
		 * @var head	Dummy node that points (forward) to the first node on the list.
		 * @var tail	Dummy node that points (behind) to the last node on the list.
		 * @var size	States the number of nodes in the list (excluding head/tail).
		 */
		private Node<E> head;
		private Node<E> tail;
		private int size;
		
		/**
		 * A basic generic constructor.
		 */
		public DoublyLinkedList() {
			head = new Node<E>(tail,null,null);
			tail = new Node<E>(null,head,null);
			size = 0;
		}
		
		/**
		 * Size-based methods, which just return an int size
		 * and a boolean for if the list is empty
		 * 
		 * @return size		How many non-head/tail nodes there are.
		 * @return isEmpty	If the are currently no ndoes between head and tail.
		 */
		@Override
		public int size() {
			return size;
		}
		@Override
		public boolean isEmpty() {
			return size == 0;
		}
		
		/**
		 * Two add methods I implemented, one for the last position
		 * and another for any position
		 * 
		 * @param obj	Object that the new node will be currently holding.
		 * @param index	Index at which to place new node. Throws if out of range.
		 */
		@Override
		public void add(E obj) {
			Node<E> newNode = new Node<E>(tail,tail.getPrev(),obj);
			tail.getPrev().setNext(newNode);
			tail.setPrev(newNode);
			size++;
		}
		@Override
		public void add(int index, E obj) {
			if (index < 0 || index > size) throw new IndexOutOfBoundsException("Inputted index does not fit the range of 0 to " + size);
			if (index == size)
				add(obj);
			else {
				Node<E> refNode = head;
				for (int i = 0; i < index; i++) {
					refNode = refNode.getNext();
				}
				Node<E> newNode = new Node<E>(refNode.getNext(),refNode,obj);
				refNode.getNext().setPrev(newNode);
				refNode.setNext(newNode);
				size++;
			}
		}
		
		/**
		 * The multiple remove functions I added, one with index,
		 * one with the first node containing a particular element,
		 * and one for all of a particular element.
		 * 
		 * @param index		Index of the node to be remvoed. Throws if out of range.
		 * @param obj		The contents of the node(s) to be removed.
		 * @return remove	Whether or not a node was successfully removed.
		 * @return kills	How many elements with specified object were removed durign the process.
		 */
		@Override
		public boolean remove(int index) {
			if (index < 0 || index >= size) throw new IndexOutOfBoundsException("Inputted index does not fit the range of 0 to " + (size - 1));
			Node<E> refNode = head.getNext();
			Node<E> prevNode = head;
			for (int i = 0; i < size; i++) {
				if (i == index) {
					prevNode.setNext(refNode.getNext());
					refNode.getNext().setPrev(prevNode);
					refNode.clear();
					size--;
					return true;
				}
				prevNode = refNode;
				refNode = refNode.getNext();
			}
			return false;
		}
		@Override
		public boolean remove(E obj) {
			Node<E> refNode = head.getNext();
			for (int i = 0; i < size; i++) {
				if (refNode.getElm().equals(obj)) {
					return remove(i);
				}
				refNode.getNext();
			}
			return false;
		}
		@Override
		public int removeAll(E obj) {
			int kills = 0;
			while (contains(obj)) {
				remove(obj);
				kills++;
			}
			return kills;
		}
		
		/**
		 * Basic setter method. Iterates through every node until
		 * reaching the specified index, then replacing the node's
		 * contents with a given element. Returns the original value.
		 * 
		 * @param index		Location of the node to update. Throws if out of range.
		 * @param obj		Object to replace onto the node's container.
		 * @return oldval	Original value that the node contained.
		 */
		@Override
		public E set(int index, E obj) {
			if (index < 0 || index >= size) throw new IndexOutOfBoundsException("Inputted index does not fit the range of 0 to " + (size - 1));
			E oldval;
			Node<E> refNode = head.getNext();
			for (int i = 0; i < size; i++) {
				if (i == index) {
					oldval = refNode.getElm();
					refNode.setElm(obj);
					return oldval;
				}
				refNode = refNode.getNext();
			}
			return null;
		}
		
		/**
		 * Three getter methods. One for finding node at an index,
		 * another for finding the first node with a particular object.
		 * and one more for finding the last node with a particular object.
		 * Bundled here is also a contains method that checks if an object
		 * exists in any of the nodes on the list, returning a boolean.
		 * 
		 * @param index		Index of the node whose value is to be retrieved. Throws if out of range.
		 * @param obj		Container of the first/last node whose index is to be found.
		 * @return obj		Object that the indexed node contains.
		 * @return index	Index at which the first/last node with given object is found. -1 if not found.
		 * @return contains	Whether or not there is anode with a given object in the list.
		 */
		@Override
		public E get(int index) {
			if (index < 0 || index >= size) throw new IndexOutOfBoundsException("Inputted index does not fit the range of 0 to " + (size - 1));
			Node<E> refNode = head.getNext();
			for (int i = 0; i < size; i++) {
				if (i == index) {
					return refNode.getElm();
				}
				refNode = refNode.getNext();
			}
			return null;
		}
		@Override
		public int firstIndex(E obj) {
			Node<E> refNode = head.getNext();
			for (int i = 0; i < size; i++) {
				if (refNode.getElm().equals(obj)) {
					return i;
				}
				refNode.getNext();
			}
			return -1;
		}
		@Override
		public int lastIndex(E obj) {
			Node<E> refNode = tail.getPrev();
			for (int i = (size - 1); i > -1; i--) {
				if (refNode.getElm().equals(obj)) {
					return i;
				}
				refNode.getPrev();
			}
			return -1;
		}
		@Override
		public boolean contains(E obj) {
			Node<E> refNode = head.getNext();
			for (int i = 0; i < size; i++) {
				if (refNode.getElm().equals(obj)) {
					return true;
				}
				refNode.getNext();
			}
			return false;
		}
		
		/**
		 * Standard clear method. Removes every item until it is empty.
		 */
		@Override
		public void clear() {
			while (!isEmpty()) {
				remove(0);
			}
			size = 0;	//redundant, but a precaution.
		}
		
		/**
		 * Iterator interface that's just here
		 * 
		 * @return Iterator	The doubly linked list iterator implemented below this method.
		 */
		@Override
		public Iterator<E> iterator() {
			return new DoublyLinkedListIterator();
		}
		
		/**
		 * The actual iterator class.
		 * 
		 * @param <E>	The container of the original Iterator interface.
		 */
		private class DoublyLinkedListIterator implements Iterator<E>{
			
			/**
			 * A variable identifying the selected node of reference.
			 * 
			 * @var refNode	The node the Iterator is currently on.
			 */
			private Node<E> refNode;
			
			/**
			 * Basic constructor for the iterator.
			 */
			public DoublyLinkedListIterator(){
				refNode = head.getNext();
			}

			/**
			 * Basic iterator methods. hasNext just checks if the node after
			 * the current one is not the tail and next just makes the
			 * reference node the next node, while returning the element of
			 * the original reference node.
			 * 
			 * @return hasNext	If the very next node is not the tail.
			 * @return elm		The value that the original refNode had.
			 */
			@Override
			public boolean hasNext() {
				return refNode != tail;
			}
			@Override
			public E next() {
				E elm = refNode.getElm();
				refNode = refNode.getNext();
				return elm;
			}
			
		}
		
}