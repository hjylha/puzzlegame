# Puzzlegame

![puzzlegame window](game.PNG)

A cute little children's puzzle as a Python program with GUI via tkinter. However, this one does not have candy as a reward for solving it, since one can simply press the *find a solution* button.

Launch the game by typing

`python play.py`

You can select a piece by clicking or pressing the key corresponding to its "name". Once selected, the piece can be moved with arrow keys or by clicking on an empty spot. Alternatively, you can just drag the pieces around.


This is the real life puzzle which inspired this project.

![puzzle in real life](rl_puzzle.PNG)


### Currently working on
- Database and file checks should be updated



### Possible issues
- Solver does not distinguish between mirrored positions, which might cause problems.
- Solver not extensively tested.



<!-- ### Recent changes -->



### Things to add maybe
- classes for pieces?? Could be needlessly complicated?
- does Puzzlegame class need modification?
- exploring weird paths (far from solutions)
- should there be a response to trying to move the big piece out of the puzzle area 
- grid method might not be the best for placing puzzle pieces
- would qt be better than tkinter?
