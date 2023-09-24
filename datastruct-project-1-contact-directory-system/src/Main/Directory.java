package Main;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Date;

import DataStructures.List.DoublyLinkedList;
import DataStructures.List.List;

/**
 * My implementation of Directory that imports the BaseDirectory interface.
 * 
 * @author DanielFebles
 */
public class Directory implements BaseDirectory {
	
	/**
	 * A simple variable for storing the output of createDirectory.
	 * 
	 * @var output	Resulting list of ContactCards obtained from createDirectory function.
	 */
	List<ContactCard> output = new DoublyLinkedList<ContactCard>();

	/**
	 * A very complicated function that will try to analyze an appropriately formatted
	 * text file containing contact information. After initializing various variables,
	 * It begins by starting the analysis of each line of the text file, which will
	 * be split up into arrays. The last part of these array is then added into a list
	 * of arrays, as these will be the friends to add to each contact later. After
	 * creating the appropriate birthday for a contact, a ContactCard is then created
	 * with the appropriate information, barring a null friend list that will be updated
	 * later, and added onto the output variable. It will do this with every line until
	 * it reaches the end of the document. It is at this point a for-loop is created,
	 * in which each friend ID array is then utilized to add the corresponding friend
	 * contact from the now complete output list, by comparing teh ID of each card to
	 * the String-casted-to-Integer ID. This sequence is skipped if there are no friends
	 * on the corresponding ContactCard. The file is then properly closed.
	 * 
	 * @param path		File to be analyzed by the buffered reader.
	 */
	@SuppressWarnings("deprecation")
	@Override
	public void createDirectory(String path) {
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new FileReader(path));
			String refLine = reader.readLine();
			String[] vals;
			String[] dates;
			String[] friend;
			Date bday;
			DoublyLinkedList<String[]> friendids = new DoublyLinkedList<String[]>();
			DoublyLinkedList<ContactCard> friends;
			while(refLine != null) {
				vals = refLine.split(",",7);
				dates = vals[5].split("-");
				friend = vals[6].split(",");
				bday = new Date(Integer.parseInt(dates[0]), Integer.parseInt(dates[2]), Integer.parseInt(dates[1]));
				output.add(new ContactCard(Integer.parseInt(vals[0]), vals[1], vals[2], vals[3], vals[4], bday, null));
				friendids.add(friend);
				refLine = reader.readLine();
			}
			for (int i = 0; i < output.size(); i++) {
				friends = new DoublyLinkedList<ContactCard>();
				if (friendids.get(i)[0].compareTo("") != 0) {
					for (int j = 0; j < friendids.size(); j++) {
						for (int k = 0; k < friendids.get(i).length; k++) {
							if (output.get(j).getID() == Integer.valueOf(friendids.get(i)[k])) {
								friends.add(output.get(j));
							}
						}
					}
				}
				output.get(i).setFriends(friends);
			}
			reader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

	/**
	 * A double (or triple?) nested for-each-loop that returns a list of
	 * contactss that the inputted contact's friends are associated with but are
	 * not friends of the inputted contact themself. With each friend, each
	 * contact on their friend list is compared to the other friends of the main
	 * contact. If a contact from the friend's friend list and the main contact's
	 * friend list share an ID, then a boolean is triggered, preventing them from
	 * being added to the output. After the test, if the currently tested friend
	 * of friend did not trigger the boolean, is not the main contact itself, and
	 * has not already been added to the output, then it is added to a recommend
	 * list, whihc is utlimately outputted once it iterates through every friend's
	 * friend list.
	 * 
	 * @param contact		Contact whose friends will be inspected.
	 * @return recommend	List of contacts that are friends of friends of the contact.
	 */
	@Override
	public List<ContactCard> recommendedFriends(ContactCard contact) {
		List<ContactCard> recommend = new DoublyLinkedList<ContactCard>();
		List<ContactCard> friends = contact.getFriends();
		boolean shared = false;
		for (ContactCard friend : friends) {
			for (ContactCard fof : friend.getFriends()) {
				for (ContactCard tester : friends) {
					if (fof.getID() == tester.getID()) {
						shared = true;
					}
				}
				if (!shared && (fof != contact) && (!recommend.contains(fof))) {
					recommend.add(fof);
				}
				shared = false;
			}	
		}
		return recommend;
	}

	/**
	 * A simple nested for-loop that compares two different friends lists from
	 * contact c1 and c2 respectively. If there exists a ContactCard with the
	 * same ID, it is added to a third list that is returned upon completion.
	 * 
	 * @param c1		First contact to check friends in common with.
	 * @param c2		Second contact to check friends in common with.
	 * @return list3	List of contacts that both the first and second contact have as friends.
	 */
	@Override
	public List<ContactCard> commonFriends(ContactCard c1, ContactCard c2) {
		List<ContactCard> list1 = c1.getFriends();
		List<ContactCard> list2 = c2.getFriends();
		List<ContactCard> list3 = new DoublyLinkedList<ContactCard>();
		for (int i = 0; i < list1.size(); i++) {
			for (int j = 0; j < list2.size(); j++) {
				if(list1.get(i).getID() == list2.get(j).getID()) {
					list3.add(list1.get(i));
				}
			}
		}
		return list3;
	}

	/**
	 * A simple for-loop that compares the birth dates between the contact
	 * and the friends on his friend list. If both they and a friend share
	 * the same day and month of birth, then the friend is added to a list
	 * called shares which is then returned once the for-loop is complete.
	 * 
	 * @param contact	The contact to be compared with their friend list.
	 * @return shares	List of friends that share a birthday with the contact.
	 */
	@SuppressWarnings("deprecation")
	@Override
	public List<ContactCard> shareBirthdays(ContactCard contact) {
		Date bday = contact.getBirthday();
		List<ContactCard> friends = contact.getFriends();
		List<ContactCard> shares = new DoublyLinkedList<ContactCard>();
		for (int i = 0; i < friends.size(); i++) {
			if (bday.getMonth() == friends.get(i).getBirthday().getMonth() && bday.getDate() == friends.get(i).getBirthday().getDate()) {
				shares.add(friends.get(i));
			}
		}
		return shares;
	}

	/**
	 * A simple return function that returns the list of ContactCards as made by createDirectory.
	 * 
	 * @return output	The list of ContactCards outputted from createDirectory function.
	 */
	public List<ContactCard> getContacts() {
		return output;
	}

}
