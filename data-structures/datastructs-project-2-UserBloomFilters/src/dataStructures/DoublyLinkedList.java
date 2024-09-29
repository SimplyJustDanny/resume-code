package dataStructures;

import java.util.Iterator;


/**
 * List implementation that uses Double nodes as well as dummy header and trailer.
 * @author Gretchen Bonilla
 *
 * @param <E>
 */
public class DoublyLinkedList<E> implements List<E>{

	private class Node<E> {
		// References the node that goes after this one. (This is the previous node of next)
		private Node<E> next;
		// References the node that goes before this one. (This is the next node of prev)
		private Node<E> prev;
		// The data the node holds
		private E element;

		public Node() {
			this.next = null;
			this.prev = null;
			this.element = null;
		}

		public Node(E elm) {
			this.next = null;
			this.prev = null;
			this.element = elm;
		}

		public Node(Node<E> next, Node<E> previous, E elm) {
			this.next = next;
			this.prev = previous;
			this.element = elm;
		}
		
		public Node<E> getNext() {
			return next;
		}
		public void setNext(Node<E> next) {
			this.next = next;
		}
		public Node<E> getPrev() {
			return prev;
		}
		public void setPrev(Node<E> prev) {
			this.prev = prev;
		}
		public E getElement() {
			return element;
		}
		public void setElement(E element) {
			this.element = element;
		}
		/**
		 * Clears the fields of this node. Helps GC.
		 */
		public void clear() {
			this.next = null;
			this.prev = null;
			this.element = null;
		}
	}
	
	
	// Dummy node
	private Node<E> header;
	private Node<E> trailer;
	private int size;
	
	public DoublyLinkedList() {
		// Initialize dummies
		this.header = new Node<E>();
		this.trailer = new Node<E>();
		// Make header trailer point at each other
		this.header.setNext(trailer);
		this.trailer.setPrev(header);
		// Size starts at 0
		this.size = 0;
	}
	

	@Override
	public int size() {
		return this.size;
	}

	private Node<E> getNode(int index) {
		// Check the index is valid
		if(index < 0 || index >size)
			throw new IndexOutOfBoundsException();
		// We start at head
		Node<E> temp = header.getNext();
		// Move through the list until we find the node at position index
		for(int i = 0; i < index; i++)
			temp = temp.getNext();
		// Return the node
		return temp;
	}
	
	@Override
	public boolean isEmpty() {
		return this.size == 0;
	}

	@Override
	public void add(E obj) {
		Node<E> newNode = new Node<E>(trailer, trailer.getPrev(), obj);
		trailer.getPrev().setNext(newNode);
		trailer.setPrev(newNode);
		size++;
	}

	@Override
	public void add(int index, E obj) {
		if(index == size)
			add(obj);
		else {
			Node<E> curr = getNode(index);
			Node<E> newNode = new Node<E>(curr, curr.getPrev(), obj);
			curr.getPrev().setNext(newNode);
			curr.setPrev(newNode);
			size++;
		}
	}

	@Override
	public E get(int index) {
		if(index < 0 || index >=size)
			throw new IndexOutOfBoundsException();
		return getNode(index).getElement();
	}

	@Override
	public E set(int index, E obj) {
		if(index < 0 || index >=size)
			throw new IndexOutOfBoundsException();
		Node<E> curr = getNode(index);
		E old = curr.getElement();
		curr.setElement(obj);
		return old;
	}

	@Override
	public boolean remove(int index) {
		if(index < 0 || index >=size)
			throw new IndexOutOfBoundsException();
		Node<E> curr = getNode(index);
		curr.getPrev().setNext(curr.getNext());
		curr.getNext().setPrev(curr.getPrev());
		curr.clear();
		size--;
		return true;
	}

	@Override
	public boolean remove(E obj) {
		int index =firstIndex(obj); 
		if(index != -1)
			return remove(index);
		return false;
	}

	@Override
	public boolean contains(E obj) {
		return firstIndex(obj)!=-1;
	}

	@Override
	public void clear() {
		while(!isEmpty())
			remove(0);
		
	}

	@Override
	public int removeAll(E obj) {
		// TODO Auto-generated method stub
		int count = 0;
		int index = firstIndex(obj);
		while(index != -1) {
			remove(index);
			index = firstIndex(obj);
			count++;
		}
		return count;
	}

	@Override
	public int firstIndex(E obj) {
		// TODO Auto-generated method stub
		Node<E> temp = header.getNext();
		int index =0;
		while(temp != trailer) {
			if(temp.getElement().equals(obj))
				return index;
			temp = temp.getNext();
			index++;
		}
			
		return -1;
	}

	@Override
	public int lastIndex(E obj) {
		Node<E> temp = trailer.getPrev();
		int index =this.size - 1;
		while(temp != header) {
			if(temp.getElement().equals(obj))
				return index;
			temp = temp.getPrev();
			index--;
		}
			
		return -1;
	}
	
	public String toString() {
		String str = "";
		// This only works because we have the iterator method implemented
		for(E e: this)
			str+= e + " ";
		return str;
	}
	
	@Override
	public Iterator<E> iterator() {
		// TODO Auto-generated method stub
		return new LinkedListIterator<E>();
	}
	
	private class LinkedListIterator<E> implements Iterator<E> {
		// For keeping track of the current node of the list
		private Node<E> currentNode;
		
		@SuppressWarnings("unchecked")
		public LinkedListIterator() {
			// We start at the head node
			currentNode = (Node<E>) header.getNext();
		}

		/**
		 * Checks if we can still move in the list
		 */
		@Override
		public boolean hasNext() {
			// Check if we reached the final node of the list
			return currentNode != trailer;
		}

		/**
		 * Gives the current value and moves us to the next
		 */
		@Override
		public E next() {
			// Get the current value
			E value = currentNode.getElement();
			// Move to next node
			currentNode = currentNode.getNext();
			return value;
		}
		
	}

}