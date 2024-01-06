# PyTetris
A version of Tetris created in Python3 and Pygame. Built in order to create an AI which can play the game more efficiently than a human. Final project for CS20.


# Usage
Requires `pygame` to be installed. Executing `main.py` will run the game.

# Controls
The controls are
| Key  | Action |
| ------------- | ------------- |
| Z  | Rotate Left  |
| X  | Rotate Right  |
| Down  | Hard Drop  |
| Left  | Move Left  |
| Right  | Move Right  |

# Features
- Main menu, with navigation buttons
- AI capable of reaching millions of score
- Leaderboard and score saving
- Classic Tetris gameplay
- 7-bag system for pieces, ensuring that each piece arrives each time
- Pausing
- Seperate levels, achieved by clearing a certain number of lines
- Faster play as levels progress

# Issues
- Levels become too fast for humans to process (pieces fall instantly)
- AI does not realistically drop pieces. Instead, it instantly puts the piece down. It will adhere to tetris rules, however.
- Controls are not adjustable, and may be unnatural for some
- AI can save scores
