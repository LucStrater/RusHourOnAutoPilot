# RusHourOnAutoPilot

Rush Hour is a simple, but surprisingly challenging game. In a board of length 6 and width 6 you get a red car which you have to move to the exit. The only problem is that there are also other cars (2 units long) and trucks (3 units long) blocking the way. To solve the game the user (or our algorithm) has to move the other vehicles in such a way that the red car can move to the exit. All vehicles can only move in one direction, that is vertical or horizontal. The goal of the game is to move the car to the exit in the least amount of steps.

## Explanation

The code is written following the environment-model-agent approach. Python was chosen as these type of problems are best solved using an object-oriented language and all of the authors mastered the syntax of this language.

### Requirements

This codebase is written in Python 3.7. To run the code you will need to install the packages in requirements.txt. This can be doen by running the following command in your terminal:

```
pip install -r requirements.txt
```

### Usage

Run the following command in your terminal:

```
python3 main.py
```

Next follow the steps printed in the terminal. First you will be asked which board you want to solve. Subsequently, you can pick the algorithm to solve it with. **It is strongly advised to solely use the hill climber algorithm on boards 5, 6 and 7** as the other algorithms are very slow and might in some case crash due to a lack of memory.

#### Hill Climber usage

With regards to the Hill Climber the user is prompted to input several values. These are as follows:

<ol>
<li>[random_nr] Number of random algorithm runs: the number of times you want the random algorithm to find a solution for the chosen board. The best solution will be used in the Hill Climber. It is important to find a good random solution (i.e. a solution with relatively few steps), as this means the A* will reach the end board quicker. </li>
<li>[max_score] Maximum allowed heuristic score: this value influences the types of "end" boards the A* algorithm chooses. That is, the A* finds the best path between a start and end board. If the maximum allowed heuristic is higher, it will try to find a path between a start and end board that are further apart. This takes more time and requires an increasing amount of memory. </li>
<li>[max_val] Maximum number of states A* is allowed to search: to prevent the A* from running for out of memory, this variable limits the amount of states the A* is allowed to evaluate. This is useful as for very large boards, the amount of states to evaluate between two boards (where the start board is given and the end board is based on the heuristic), can be enormous. As such, you may run out of memory when running this without this cap. </li>
<li>[low_max_score] Maximum allowed heuristic score after failed A* search: in case the A* reaches the maximum number of states it is allowed to search, the heuristic value that is used to evaluate the end board is lowered with this variable. As such, it will choose a board that is closer to the start board, and thus the A* will need to evaluate relatively few states to get to this board (and will probably not reach the maximum state evaluation limiter).</li>
<li>[max_plus] Incrementation of the maximum heuristic score after an A* iteration over the whole move set: this variable increases the heuristic value that is used to cap the type of end boards that are chosen from a given start board. This happens after the A* has already successfully reduced the moveset once, and uses this variable to increment the maximum heuristic score at each consecutive run. </li>
<li>[max_val_plus] Incrementation of the maximum number of states to be searched after an A* iteration over the whole move set: this increases the maximum number of states the A* algorithm is allowed to evaluate.  This happens after the A* has already successfully reduced the moveset once, and increments at each consecutive run of the A*. This value should increment in tandem with the [max_plus] value, such that larger heuristics are coupled with more states to evaluate. </li>
</ol>

### Structure

The following list describes the structure of the files and folders in this project and where you could find them:

- **/code**: Contains all code written for this project (excluding main).
  - **/code/algorithms**: Contains the code for the agents applied on the model.
    - **/code/algorithms/a_star_io.py**: An A\* algorithm that finds the shortest path between two given rush hour boards.
    - **/code/algorithms/a_star.py**: An A\* algorithm that finds the optimal solution of a rush hour game.
    - **/code/algorithms/breadth_first.py**: A breadth first algorithm for solving a rush hour game.
    - **/code/algorithms/depth_first.py**: A depth first algorithm for solving a rush hour game.
    - **/code/algorithms/hillclimber.py**: A hill climbing approach to solving a rush hour game. This approach commences with a random board. In turn, it trims the found random solution following the "back-forward" principle. Subsequently, the algorithm runs state tracing over the moveset. It then uses the resulting board from the previous steps, and applies A* shortening. The A* shortening is applied iteratively, taking the resulting moveset of the previous A* as input (and runs until A* cannot improve the solution. Lastly the algorithm cleans the solution using a greedy.
    - **/code/algorithms/iterative_deepening.py**: Iterative deepening algorithm for solving a rush hour game.
    - **/code/algorithms/randomise.py**: An algorithm that makes random moves until a solution is found.
  - **/code/classes**: Contains the classes for the model and the environment.
    - **/code/classes/board.py**: The board class is part of the environment of the rush hour game and its attributes are static for a particular game.
    - **/code/classes/car.py**: The car class represents a car on the board class and is thereby also part of the environment. Its attributes are static.
    - **/code/classes/model.py**: This contains the model that represents a rush hour game. The attributes of the Model class are dynamic.
  - **/code/output**: Contains code to generate the output.
    - **/code/output/output.py**: A file that saves the steps to a csv file.
    - **/code/output/pygame_viz.py**: A pygame implementation that shows the steps to solve the rush hour game that one of the algorithms has found.
- **/data**: Contains all data files for this project.
  - **/data/input**: Contains csv files for the starting boards of 7 rush hour games.
  - **/data/output**: Contains the output file.

## Authors

- Mees Wortelboer
- Nils Breeman
- Luc Sträter

## Acknowledgements

For the pygame visualisation, our code is based on the python script written by Noah-Giustini. This can be accessed [here](https://github.com/Noah-Giustini/RushHour).
