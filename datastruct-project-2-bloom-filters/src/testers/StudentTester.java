package testers;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import org.junit.Before;
import org.junit.Test;

import dataStructures.List;
import main.BloomFilter;

public class StudentTester {
	
	BloomFilter bf;
	
	/**
	 * Creates an empty bloom filter
	 */
	@Before
	public void setup() {
		bf= new BloomFilter();
	}
	/**
	 * Tests if the database is created with the expected content.
	 */
	@Test
	public void testCreateDatabase() {
		List<String> db = bf.createDatabase("inputFiles/database.csv");
		
		String[] expected = {
				"victor.stone", 
				"diana.prince", 
				"wanda.maximoff", 
				"bruce.wayne", 
				"clark.kent", 
				"natasha.romanoff", 
				"billy.batson", 
				"harleen.quinzel", 
				"bruce.banner", 
				"thor.odinson"};
		compareList(db, expected);
		assertTrue("Database has more values that expected.", db.size() == 10);
	}
	/**
	 * Tests if the check is created with the expected content.
	 */
	@Test
	public void testCreateCheck() {
		List<String> check = bf.createCheck("inputFiles/db_check.csv");
		
		String[] expected = {
				"wanda.maximoff", 
				"steven.strange", 
				"eddie.brock", 
				"bruce.banner",
				"timothy.drake",
				"billy.batson" 
				};
		compareList(check, expected);
		assertTrue("Check has more values than expected.", check.size() == 6);
	}
	/**
	 * Tests if the bloom filter is created correctly.
	 */
	@Test
	public void testBloomFilter() {
		bf.createDatabase("inputFiles/database.csv");
		List<Boolean> filter = bf.bloomFilter();
		for(Boolean b: filter) {
			if(b)
				fail("Initial bloom filter isn't initially 0 (false)");
		}
		assertTrue(filter.size() == 335);
	}
	/**
	 * Checks that hashing function.
	 */
	@Test
	public void testHashing() {
		int hash1 = bf.hashing("Help", 1);
		int hash2 = bf.hashing("Help", 2);
		int hash3 = bf.hashing("Help", 3);
		int hash4 = bf.hashing("Help", 4);
		
		assertTrue("Hashing didn't generate the expectd indexes.", hash1 == 98 && hash2 == 196 && hash3 == 294 && hash4 == 393);
		
	}
	
	/*
	 * PRIVATE METHOD 
	 * 
	 * DO NOT EDIT!!!
	 */
	private void compareList(List<String> list, String[] expected) {
		for(String word: expected) {
			if(!list.contains(word))
				fail("The list created doesn't have all the expected content. "
						+ "Missing " + word +".");
		}
	}

}
