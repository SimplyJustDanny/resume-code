package main;

import dataStructures.List;

public interface BaseBloomFilter {
	
	/**
	 * Method that parses the csv in a given path and creates
	 * the first of the two initial lists. List must have the
	 * user names within the database.csv file
	 * 
	 * @param path - Path to the database.csv
	 * @return list of user names 
	 */
	public List<String> createDatabase(String path);
	
	/**
	 * Method that parses the csv in a given path and creates
	 * the second of the two initial lists. List must have
	 * the user names within the db_check.csv file
	 * 
	 * @param path - Path to the db_check.csv
	 * @return list of user names to be checked
	 */
	public List<String> createCheck(String path);
	
	/**
	 * Method that creates the empty bloom filter dynamically
	 * using the formula of SIZE.
	 * 
	 * @return boolean list filled with 0s (false)
	 */
	public List<Boolean> bloomFilter();

	/**
	 * Method that receives a word and seed. Applying the formula of 
	 * HASHING it returns an integer.
	 * 
	 * @param word - Word 
	 * @param seed - seed for the hashing
	 * @return word turned into an integer
	 */
	public int hashing(String word, int seed);
	
	/**
	 * Method that fills the bloom filter after using the 
	 * hashing function the number of times found with the TIME TO
	 * REPEAT HASHING for each of the elements within the 
	 * List created off the database file
	 * 
	 * @return boolean list filled with the appropriate 1s
	 */
	public List<Boolean> fillingBloomFilter();
	
	/**
	 * Method that creates the results file based on the
	 * hashing done for each of the words within the List
	 * created off the db_check file. The results file should go
	 * into the outputFiles folder.
	 */
	public void generateResults();

}
