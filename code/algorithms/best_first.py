from code.algorithms.a_star_io import A_star

class Best_first(A_star):
    """
    this best first algorithm functions as the A* IO only the heuristic is not admissable.
    """
    def heuristic(self, model):
        """   
        Distance to goal: with a given goal board determine the distance of every car to its final position.
        """ 
        score = 0

        for car in self.cars:
            row_model, column_model = model.get_car_pos(car)
            row_goal, column_goal = self.goal.get_car_pos(car)
            score += abs(row_model - row_goal) + abs(column_model - column_goal)

        return score