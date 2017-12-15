# Pacman

This coursework exercise asks you to write code to create an MDP-solver to work in the Pacman
environment that we used for the practical exercises.(non-deterministic, 0.8 correct way, 0.1 go righr, 0.1go left)

This coursework requires you to write code to control Pacman and win games using an MDP-
solver. There is a (rather familiar) skeleton piece of code to take as your starting point in the file
mdpAgents.py. This code defines the class MDPAgent.
There are two main aims for your code:
(a) Be able to win at least four games in ten in smallGrid
(b) Be able to win at least two games in ten in mediumClassic
To win games, Pacman has to be able to eat all the food.

Your code must be in Python 2.7.

command:
(a) We will evaluate whether your code can win games in smallGrid by running:
python pacman.py -n 10 -p MDPAgent -l smallGrid
-l is shorthand for -layout. -p is shorthand for -pacman.
(b) We will evaluate whether your code can win games in mediumClassic by running:
python pacman.py -n 10 -p MDPAgent -l mediumClassic
The -n 10 runs ten games in a row.
(c) When using the -n option to run multiple games, the same agent (the same instance of
MDPAgent.py) is run in all the games.
