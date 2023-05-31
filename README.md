# SLOW AI Minesweeper
This is an opensource AI project to solve Minesweeper as fast (slow) as possible

## Intro
This is an opensource project I made when I had some free time.
The goals were to:
 - Have a basic algorithm to solve Minesweeper
 - Use screen capture and mouse-clicks
 - I used https://minesweeperonline.com
 - I worked on it for ~3 days

## Logic
 - Iterative process for:
   - calculate probabilities of bombs
   - flag squares with probability 1
   - expose certainly non-bomb squares
   - if no 100% certainty - mark squares with the highest bomb probability

## How to Run:
 - main.py has 2 run options:
   - main(board_level=<board config>) - run the program on the given config
   - read_board(board_level=BeginnerMinesweeperOnline) - read and print the board on the screen

## TODO:
 - Reading screen pixels isn't ideal, maybe I have offsets here and there and in expert mode the board doesn't 
always match what's on the screen.
 - Improve middle-clicks - only when necessary
 - Completely ignore blank screen - no need to sample them over and over
 - REFACTORING! (make *main* more OO, migrate logic to board.py,... )
 - TESTS!
 - Maybe get pixels from browsers? from DOM? would be more accurate

## Contact me:
 - sagysrael@gmail.com
 - https://www.linkedin.com/in/sagydr/