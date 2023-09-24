package Main;
import DataStructures.List.List;

/**
 * Base Directory Interface
 * @author bermed28
 */
public interface BaseDirectory {
	
	/**
	 * Method that takes in a string representing 
	 * the path of contactDirectoy.csv and parses said csv. 
	 * Once parsed, the Directory class will have filled up the private directory 
	 * ArrayList<ContactCard> field
	 * 
	 * @param path - Path to contactDirectory.csv
	 * @author bermed28
	 */
	public void createDirectory(String path);

	/**
	 * Method that returns a list of ContactCards that represent all of the cards the contact 
	 * passed as parameter does not have marked as favorite, but his favorites do have marked 
	 * as favorite.
	 * 
	 * Think of it like Facebook’s “People You May Know” feature, 
	 * friends of friends who are not friends with you.
	 * 
	 * If contact does not have any friends, the method returns an empty list.
	 *  
	 * @param contact - The target contact to find the recommendedFriends of.
	 * @return - A list of contact cards that represent all of the cards the contact 
	 * passed as parameter does not have marked as favorite, but his favorites do have marked 
	 * as favorite.
	 * @author bermed28
	 */
	public List<ContactCard> recommendedFriends(ContactCard contact);

	/**
	 * Method that returns a list of common friends between 2 contact cards.
	 * 
	 * If c1 or c2 does not have any friends, the method returns an empty list.
	 * 
	 * @param c1 - Contact 1
	 * @param c2 - Contact 2
	 * @return A list of common friends between c1 and c2
 	 * @author bermed28
	 */
	public List<ContactCard> commonFriends(ContactCard c1, ContactCard c2);
	
	
	/**
	 * Method that returns a list of contacts who share the same birthday as the contact passed as parameter.
	 * A shared birthday are the dates that share the same month and the same day.
	 * 
	 * @param contact - Target contact that contains the birthday to look for in common with other contacts
	 * @return a list of contacts who share the same birthday as contact.
	 * @author bermed28
	 */
	public List<ContactCard> shareBirthdays(ContactCard contact);
	
}
