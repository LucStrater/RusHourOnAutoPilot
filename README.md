# RusHourOnAutoPilot

Rush Hour is a simple, but surprisingly challenging game. In a board of length 6 and width 6 you get a red car which you have to move to the exit. The only problem is that there are also other cars (2 units long) and trucks (3 units long) blocking the way. To solve the game the user (or our algorithm) has to move the other vehicles in such a way that the red car can move to the exit. All vehicles can only move in one direction, that is vertical or horizontal. The goal of the game is to move the car to the exit in the least amount of steps.


## Explenation
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

Next follow the steps printed in the terminal. First you will be asked which board you want to solve. Than you can pick the algorithm to solve it with. It is strongly advised to only use the hill climber algorithm on boards 5, 6 and 7 as the other algorithms are very slow and might in some case crash due to a lack of memory. 


### Structure

The following list describes the structure of the files and folders in this project and where you could find them:

- **/code**: Contains all code written for this project (excluding main).
  - **/code/algorithms**: Contains teh code for the agents applied on the model.
    - **/code/algorithms/a_star_io.py**: An A* algorithm that finds the shortest path between two given rush hour configurations.
    - **/code/algorithms/a_star.py**: An A* algorithm that finds the optimal solution of a rush hour game.
    - **/code/algorithms/breadth_first.py**: A breath first approach to solving a rush hour game.
    - **/code/algorithms/depth_first.py**: A depth first approach to solving a rush hour game. 
    - **/code/algorithms/hillclimber.py**: A hill climbing approach to solving a rush hour game. Starts with a random board, then does back-forward trimming, then state-tracing, then A* shortening and lastly cleans the solution using a greedy. The first 4 steps are done for multiple iterations untill no improvement is found.
    - **/code/algorithms/iterative_deepening.py**: Iterative deepening algorithm for solving rush hour boards.
    - **/code/algorithms/randomise.py**: An algorithm that makes random moves untill a solution is found.
  - **/code/classes**: Contains the classes for the model and the environment.
    - **/code/classes/board.py**: The board class is part of the environment of the rush hour game and its attributes are static for a particular game.
    - **/code/classes/car.py**: The car class represents a car on the board class and is thereby also part of the environment and its attributes are also static.
    - **/code/classes/model.py**: This contains the model that represents a rush hour game. The attributes of the Model class are dynamic.
  - **/code/output**: Contains code to generate the output.
    - **/code/output/output.py**: A file that saves the steps to a csv file.
    - **/code/output/pygame_viz.py**: A pygame implementation that shows the steps to solve the rush hour game.
- **/data**: Contains all data files for this project. 
  - **/data/input**: Contains csv files for the begin position of 7 rush hour games. 
  - **/data/output**: Contains the output file.


## Authors
- Mees Wortelboer
- Nils Breeman
- Luc Sträter







