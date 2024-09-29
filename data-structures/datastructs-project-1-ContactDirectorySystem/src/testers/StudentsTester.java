package testers;

import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;

import DataStructures.List.DoublyLinkedList;
import DataStructures.List.List;
import Main.ContactCard;
import Main.Directory;

public class StudentsTester {
	private Directory dir;
	
	@Before
	public void setup() {
		this.dir = new Directory();
		dir.createDirectory("inputFiles/directory.csv");
	}
	/*
	 * TESTING THE DIRECTORY CLASS
	 */
	/*
	 * Testing sharedBirthday()
	 */
	@Test
	public void testBirthdayShared() {
		// She shares birthday with Elizabeth Briggs (3647)
		ContactCard caroleSkidmore = findContact(9639);
		
		
		List<ContactCard> sharedbday = dir.shareBirthdays(caroleSkidmore);
		assertTrue("Failed to return a list with contact Elizabeth Briggs (id=3647) "
				+ "when calling sharedBirthdays() for contact with ID 9639.", 
				sharedbday.size() == 1 && sharedbday.get(0).getID() == 3647);
	}
	@Test
	public void testBirthdayNotShared() {
		// Doesn't share birthday with anyone
		ContactCard howardCardenas = findContact(7486);
		
		List<ContactCard> sharedbday = dir.shareBirthdays(howardCardenas);
		assertTrue("Failed to return empty list for sharedBirthdays() for contact with ID 7486.", 
				sharedbday.isEmpty());
	}
	/*
	 * Testing recommendedFriends()
	 */
	@Test
	public void testFriendsOfFriends() {
		// She has 3 friends Lorenzo Cunningham (66), Brenda Golding (2267), and Carole Skidmore (9639)
		ContactCard gertrudeHansen = findContact(6376);
		/*
		 * Should suggest: 914,4903,3647 (not necessarily in that order)
		 */
		int[] suggIds = new int[] {914, 4903, 3647};
		List<ContactCard> FoFs = dir.recommendedFriends(gertrudeHansen);
		assertTrue("Failed to return a list with the contacts of IDs {914, 4903, 3647} when calling "
				+ "recommendedFriends(6376).", checkContent(suggIds, FoFs));
	}
	@Test
	public void testFriendsOfFriendsClosedCircle() {
		// She has 4 friends Diana Woodward (914), Brenda Golding (2267), Bonny Mongelli (4903) and Gertrude Hansen(6376)
		ContactCard lorenzoCunningham = findContact(66);
		/*
		 * Should suggest: 9639
		 */
		int[] suggIds = new int[] {9639};
		List<ContactCard> FoFs = dir.recommendedFriends(lorenzoCunningham);
		assertTrue("Failed to return a list with the contacts of IDs {9639} when calling "
				+ "recommendedFriends(66).", checkContent(suggIds, FoFs));
	}
	/*
	 * Testing commonFriends()
	 */
	@Test
	public void testCommonFriendsLevel0() {
		// Total strangers
		ContactCard annaWilliams = findContact(1521);
		ContactCard dianaWoodward = findContact(914);
		/*
		 * They should have 0 friends in common
		 * Should return: {}
		 */
		List<ContactCard> CFs = dir.commonFriends(annaWilliams, dianaWoodward);
		assertTrue("Failed to return a list with the contacts of IDs { } when calling "
				+ "commonFriends(1521, 914).", CFs.isEmpty());
	}
	@Test
	public void testCommonFriendsLevel2() {
		// They're mutual friend
		ContactCard brendaGolding = findContact(2267);
		ContactCard lorenzoCunningham = findContact(66);
		/*
		 * They should have 2 friends in common
		 * Should return: Bonny Mongelli (4903) and Gertrude Hansen (6376)
		 */
		int[] suggIds = new int[] {4903, 6376};
		List<ContactCard> CFs = dir.commonFriends(brendaGolding, lorenzoCunningham);
		assertTrue("Failed to return a list with the contacts of IDs {4903, 6376} when calling "
				+ "commonFriends(2267, 66).", checkContent(suggIds, CFs));
	}

	/*
	 * Testing ContactCard
	 */
	@Test
	public void testContactCard() {
		// Pick a random contact
		ContactCard johnDoe = dir.getContacts().get(0);
		johnDoe.setID(0);
		johnDoe.setName("John Doe");
		johnDoe.setEmail("john.doe@mail.com");
		johnDoe.setPhone("1234567890");
		johnDoe.setJobTitle("Worker");
		johnDoe.setFriends(new DoublyLinkedList<>());
		// Check each field
		boolean checkID = johnDoe.getID() == 0;
		boolean checkName = johnDoe.getName().equals("John Doe");
		boolean checkJobTitle = johnDoe.getJobTitle().equals("Worker");
		boolean checkPhone = johnDoe.getPhone().equals("1234567890");
		boolean checkEmail = johnDoe.getEmail().equals("john.doe@mail.com");
		boolean checkFriends = johnDoe.getFriends().isEmpty();
		assertTrue("There's incorrect data in the contact card.", checkID && checkName && 
				checkJobTitle && checkPhone && checkEmail && checkFriends);
		
	}
	/*
	 * AUXILIARY METHODS
	 * 
	 * ***** DO NOT ALTER! ******
	 */
	/**
	 * Returns the contact of the given ID from the directory.
	 * @param id - (int) Id of the contact we wish to find.
	 * @return (ContactCard) The contact with ID id
	 */
	private ContactCard findContact(int id) {
		for(ContactCard c: dir.getContacts()) {
			if(c.getID() == id)
				return c;
		}
		return null;
	}
	/**
	 * Returns whether all the IDs given are present in the List and it contains exclusively those IDs.
	 * @param ids - (int[]) IDs of the contacts expected to be in the list
	 * @param contacts - (List<ContactCard>) List of contacts that we will compare to the IDs given
	 * @return (boolean) True if all the IDs are present in the List and both are the same size, false otherwise
	 */
	private boolean checkContent(int[] ids, List<ContactCard> contacts) {
		// By default they cannot be the same
		if(ids.length != contacts.size())
			return false;
		// Check if the ids are present
		for(int id: ids) {
			boolean found = false;
			for(ContactCard c: contacts) {
				if(c.getID() == id) {
					found = true;
					break;
				}
			}
			if(!found)
				return false;
		}
		return true;
	}
}
