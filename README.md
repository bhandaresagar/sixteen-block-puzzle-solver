# sixteen-block-puzzle-solver

Solves famous 15 block puzzle, with one variation

Consider a variant of the 15-puzzle, but with the following important changes. First, instead of 15
tiles, there are 16, so that there are no empty spaces on the board. Second, instead of moving a single
tile into an open space, a move in this puzzle consists of either (a) sliding an entire row of tiles left or
right, with the left- or right-most tile "wrapping around" to the other side of the board, or (b) sliding
an entire column of the puzzle up or down, with the top- or bottom-most tile "wrapping around" .

The goal of the puzzle is to find a short sequence of moves that restores the canonical configuration
(on the left above) given an initial board configuration.	

The program should run on the command line like:
python solver16.py [input-board-filename]
where input-board-filename is a text file containing a board configuration in a format like: <br />
5 7 8 1 <br />
10 2 4 3 <br />
6 9 11 12 <br />
15 13 14 16 <br />

