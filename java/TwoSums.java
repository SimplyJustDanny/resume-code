import java.util.Arrays;

public class TwoSums {
	public static int[] twoSum(int[] array, int targetSum) {			            					//Documentation:
		Arrays.sort(array); 																                              //O(nlogn) function (dominant).
		int ofs = 1;													                                  					//Declares offset var.
		int[] ary = new int[2];																                            //Initialize return array.
		for (int i = 0; i < (int) array.length; i++) {                 										//O(n) for loop.
			while (array[i] + array[array.length-ofs] > targetSum && array.length != ofs) {	//If sum larger than target,
				ofs += 1;															                                    		//then increase offset unless
			}														                                        						//it is equal to array length.
			if (array.length == ofs) {						                           								//If length does equal offset,
				break;															                                    			//break.
			}
			if (array[i] + array[array.length-ofs] == targetSum && i != array.length-ofs) {	//If sum equals target and they
				ary[0] = array[i];															                              //are not same value, assign
				ary[1] = array[array.length-ofs];									                        		//values to return array and
				break;												                                    						//break.
			}
		}
		if (ary[0] + ary[1] != targetSum) {										                      			//If array is still shit,
			int[] na = {};																	                                //initialize and return
			return na;																	                                  	//empty array.
		}
		return ary;																	                                  		//Otherwise return array.
	}
}
