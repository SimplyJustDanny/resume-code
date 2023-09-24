package main;

import dataStructures.List;

/**
 * Class where the Bloom Filter logic will be implemented.
 * This is NOT where you will implement the BloomFilter methods.
 * 
 * @author Gretchen Bonilla
 *
 */
public class BloomFilterMain {

	
	public static void main(String[] args) {
		/*
		 * BLOOM FILTER LOGIC DESCRIBED IN THE DOCUMENT GOES HERE
		 * 
		 * When the main finishes executing it should produce results.csv 
		 * and the output should be the same as the one shown in expected_output.csv
		 */
		
		/**
		 * A simple main function that creates an object and calls all the necessary methods.
		 * 
		 * @author Daniel Febles
		 */
		BloomFilter bf = new BloomFilter();
		bf.createDatabase("inputFiles/database.csv");
		bf.createCheck("inputFiles/db_check.csv");
		bf.bloomFilter();
		bf.fillingBloomFilter();
		bf.generateResults();
	}

}
