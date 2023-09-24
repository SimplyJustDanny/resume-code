public class SudokuValidifier {
	public static boolean isValidSudoku(char[][] board) {
        for (int i = 0; i < 9; i++) {
        	for (int j = 0; j < 9; j++) {
        		for (int k = j+1; k < 9; k++) {
        			//Tests Columns
        			if(board[i][j] != '.' || board[i][k] != '.')
        				if (board[i][j] == board[i][k]) {
        				return false;
        			}
        			//Tests Rows
        			if(board[j][i] != '.' || board[k][i] != '.')
        				if (board[j][i] == board[k][i]) {
        				return false;
        			}
        			//Tests Grids
        			if(board[j % 3 + 3*(i % 3)][Math.floorDiv(j,3) + 3*Math.floorDiv(i,3)] != '.' || board[k % 3 + 3*(i % 3)][Math.floorDiv(k,3) + 3*Math.floorDiv(i,3)] != '.')
        				if (board[j % 3 + 3*(i % 3)][Math.floorDiv(j,3) + 3*Math.floorDiv(i,3)] == board[k % 3 + 3*(i % 3)][Math.floorDiv(k,3) + 3*Math.floorDiv(i,3)]) {
        				return false;
        			}
        		}
        	}
        }
		return true;
    }
}
