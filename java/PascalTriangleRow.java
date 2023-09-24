public class PascalTriangleRow {
	public static int[] getRowPascalTriangle(int rowIndex) {
		int[] ary = new int[rowIndex + 1];
		for (int i = 0; i <= rowIndex; i++) {
			ary[i] = 1;
			for (int j = (i - 1); j > 0; j--) {
				ary[j] = (ary[j] + ary[j-1]);
			}
		}
		return ary;
	}
}
