package Main;

import java.util.Date;
import DataStructures.List.DoublyLinkedList;

/**
 * Contact Card Class to hold all the information 
 * regarding one contact inside the directory
 * 
 * @author bermed28 & DanielFebles
 */
public class ContactCard {
	
	/**
	 * Setting up all the ncessary variables to store data
	 * 
	 * @var ID		Number that identifies the card. .
	 * @var name	Contact associated with the card.
	 * @var title	Job title of the contact.
	 * @var phone	Phone number of the contact.
	 * @var email	E-mail of the contact.
	 * @var bday	Birthdate of the contact.
	 * @var friends	Other contacts that this contact is friends with.
	 */
	private int ID;
	private String name;
	private String title;
	private String phone;
	private String email;
	private Date bday;
	private DoublyLinkedList<ContactCard> friends;
	
	/**
	 * Two primary constructors: a generic one (in the event I need it)
	 * and a fully-parametered one
	 * 
	 * @param ID						Assigns an ID integer.
	 * @param name, title, phone, email	Assigns the respective string.
	 * @param date						Assign the respective date.
	 * @param friends					Assign the respective DoublyLinkedList<E>
	 */
	public ContactCard() {
		ID = -1;
		name = null;
		title = null;
		phone = null;
		email = null;
		bday = null;
		friends = new DoublyLinkedList<ContactCard>();
	}
	public ContactCard(int ID, String name, String title, String phone, String email, Date bday, DoublyLinkedList<ContactCard> friends) {
		this.ID = ID;
		this.name = name;
		this.title = title;
		this.phone = phone;
		this.email = email;
		this.bday = bday;
		this.friends = friends;
	}
	
	/**
	 * Getters and setters for each variable respectively
	 * 
	 * @param ID, name, title, phone, email, bday, friends	Value to update on the ContactCard.
	 * @return ID, name, title, phone, email, bday, friends	Current value on the ContactCard.
	 */
	public int getID() { return ID;}
	public String getName() { return name;}
	public String getJobTitle() { return title;}
	public String getPhone() { return phone;}
	public String getEmail() { return email;}
	public Date getBirthday() { return bday;}
	public DoublyLinkedList<ContactCard> getFriends() { return friends;}
	public void setID(int ID) { this.ID = ID;}
	public void setName(String name) { this.name = name;}
	public void setJobTitle(String title) { this.title = title;}
	public void setPhone(String phone) { this.phone = phone;}
	public void setEmail(String email) { this.email = email;}
	public void setBirthday(Date bday) { this.bday = bday;}
	public void setFriends(DoublyLinkedList<ContactCard> friends) { this.friends = friends;}
}
