package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import dataStructures.*;
import dataStructures.List;

	/**
	 * My implementation of the BloomFilter class, which implements BaseBloomFilter.
	 * 
	 * @author DanielFebles
	 */

public class BloomFilter implements BaseBloomFilter {
	
	/**
	 * A handful of variables to facilitate a lot of processes between methods.
	 * 
	 * @var filterSize	Integer for the filter's size as determined by a formula.
	 * @var database	A list of strings that contain the users in the database file.
	 * @var check		A list of strings that contain the users in the check file.
	 * @var filter		A list of booleans that mimic a bloom filter.
	 */
	int filterSize = 0;
	List<String> database = new DoublyLinkedList<String>();
	List<String> check = new DoublyLinkedList<String>();
	List<Boolean> filter = new ArrayList<Boolean>(filterSize);

	/**
	 * A simple file reading function that takes a given path to a database file then
	 * creates and returns a list of strings from the received data. It initializes a
	 * DoublyLinkedList in order to make sure that additions to the list are as easy
	 * and efficient as possible. A BufferedReader is then initialized, which will
	 * then iterate through the given path, adding the user from each line by splitting
	 * the line into an array via commas and adding the first string, which should be
	 * the name, to the DoublyLinkedList. It then closes the file, internally remembers
	 * the DoublyLinkedList and then returns it.
	 * 
	 * @param path		The directory in which the database file is located.
	 * @return result	A list of strings containing all the users within the file.
	 */
	@Override
	public List<String> createDatabase(String path) {
		List<String> result = new DoublyLinkedList<String>();
		try {
			BufferedReader reader = new BufferedReader(new FileReader(path));
			String refLine = reader.readLine();
			while (refLine != null) {
				result.add(refLine.split(",")[0]);
				refLine = reader.readLine();
			}
			reader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		database = result;
		return result;
	}

	/**
	 * An even simpler file reading function. Receives a path to a check file, and
	 * retuns a list of strings containing the users in that file. It initialies a
	 * DoublyLinkedList for easy and efficient addition, then initiates a
	 * BufferedReader to iterate through the file, adding each line (and thus username)
	 * to the DoublyLinkedList. Close file, interanlly save the DoublyLinkedList, and
	 * finally return it.
	 * 
	 * @param path		The directory in which the check file is located.
	 * @return result	A list of strings containing all the users within the file.
	 */
	@Override
	public List<String> createCheck(String path) {
		List<String> result = new DoublyLinkedList<String>();
		try {
			BufferedReader reader = new BufferedReader(new FileReader(path));
			String refLine = reader.readLine();
			while (refLine != null) {
				result.add(refLine);
				refLine = reader.readLine();
			}
			reader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		check = result;
		return result;
	}

	/**
	 * A simple method that produces and returns a list of booleans meant to imitate a
	 * bloom filter. First it calculates the initial size of the bloom filter via a
	 * formula, then creates a new ArrayList with the calculated size. The ArrayList
	 * was chosen as being able to index efficiently is vital for a bloom filter.
	 * Afterwards, a for loop proceeds to add a number of falses to the ArrayList,
	 * said number being equal to the prior calcuated size. Finally, it returns the
	 * ArrayList.
	 * 
	 * @return filter	A list of booleans meant to imitate a Bloom Filter.
	 */
	@Override
	public List<Boolean> bloomFilter() {
		filterSize = (int) ((-1*database.size()*Math.log(0.0000001))/Math.pow(Math.log(2), 2));
		filter = new ArrayList<Boolean>(filterSize);
		for (int i = 0; i < filterSize; i++) filter.add(false);
		return filter;
	}
	
	/**
	 * A simple hashing method. It takes the inputted word, turns it into an integer
	 * via ASCII characters, and returns said integer multiplied by an inputted seed
	 * amd divided by the word's length.
	 * 
	 * @param word	The string which will be converted into a hash code.
	 * @param seed	A seed to further offset the final hash code.
	 * @return hash	Result of the string going through the hashing formula.
	 */
	@Override
	public int hashing(String word, int seed) {
		int ascii = 0;
		for (int i = 0; i < word.length(); i++) {
			ascii += word.charAt(i);
		}
		int hash = ascii*seed/word.length();
		return hash;
	}

	/**
	 * A method that fills the bloom filter by using the list of users extracted from
	 * the database. First it calculates the number of times to hash via a formula.
	 * Then, after declaring hash variable, it iterates through every user on the
	 * list and hashes it with a range of numbers determined by the prior calculated
	 * number of times. It then sets true at the indexes of each hash produced by the
	 * hashcode, modulo the size of the filter. It then returns the filled filter.
	 * 
	 * @return filter	The filled bloom filter as determined by the database.
	 */
	@Override
	public List<Boolean> fillingBloomFilter() {
		int times = (int) (filterSize*Math.log(2)/database.size());
		int hash = 0;
		for (String user : database) {
			for (int i = 1; i <= times; i++) {
				hash = hashing(user, i);
				filter.set(hash % filterSize, true);
			}
		}
		return filter;
	}

	/**
	 * A method that generates a file containing a list of the users in the check file,
	 * each accompanied by a statement of whether or not they could be in the bloom filter.
	 * It starts by calculating the number of times to hash, alongside initializing an int
	 * hash and a boolean broken. It then creates a File object with path set to outputFiles,
	 * and creates (or replaces) a .csv file called results. A BufferedWriter object is then
	 * initialized in order to write through the list, starting with the header. While it does
	 * so, it iterates through the check list, and checks if the indexes of every hash from
	 * each user is true. If one of the hashes from a user ends up being false, then the user 
	 * is declared to not be in the filter, the broken boolean is set to true, and the loop
	 * breaks. If a user has every single hash tested, and the loop is not broken prematurely,
	 * then the user is written to probably be in the database. If the loop was broken
	 * prematurely, then the broken boolean is set to false again. After iterating through
	 * every single user in the check list, the writer closes the file, adn the results.csv
	 * is completely ouputted. (NOTE: The file might not appear initially when using Eclipse,
	 * which is why it is recommended to refresh the project (by clicking on the project folder
	 * then either hitting F5 or clicking Refresh from the dropdown File tab) after running the
	 * BloomFilterMain. In the event that it still doesn't show, the file can still be accessed
	 * and seen through File Explorer, inside whererever the project directory is located.)
	 * 
	 * @create results.csv	A file showing which checked users could be in the bloom filter.
	 */
	@Override
	public void generateResults() {
		try {
			int times = (int) (filterSize*Math.log(2)/database.size());
			int hash = 0;
			boolean broken = false;
			File output = new File("outputFiles/results.csv");
			if(output.exists()) output.delete();
			output.createNewFile();
			BufferedWriter writer = new BufferedWriter(new FileWriter("outputFiles/results.csv"));
			writer.write("Username,Result");
			for (String user : check) {
				for (int i = 1; i <= times; i++) {
					hash = hashing(user, i);
					if (!filter.get(hash % filterSize)) {
						writer.write("\n" + user + ",Not in the DB");
						broken = true;
						break;
					}
				}
				if (!broken) writer.write("\n" + user + ",Probably in the DB");
				else broken = false;
			}
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}	
	}

}
