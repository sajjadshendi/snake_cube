import random
from time import time
from sim import *
from Interface import *
import json


# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        self.predicted_actions = []

    # the act function takes a json string as input
    # and outputs an action string
    # action example: [1,2,-2]
    # the first number is the joint number (1: the first joint)
    # the second number is the axis number (0: x-axis, 1: y-axis, 2: z-axis)
    # the third number is the degree (1: -90 degree, -2: 180 degree, -1: 90 degree). angles are counterclockwise
    def act(self, percept):
        # ^^^ DO NOT change the act function above ***

        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***

        alg = self.BFS_SAMPLE_CODE
    
        if self.predicted_actions == []:
            t0=time()
            initial_state = WorldModel(sensor_data['Coordinates'], sensor_data['sticky_cubes'])
            self.predicted_actions = alg(initial_state)
            print("run time:", time()-t0)

        action_info = self.predicted_actions.pop()
        action = [action_info[0], action_info[2], action_info[4]]
        return action

    def BFS_SAMPLE_CODE(self, root_game):
        interface=Interface()

        q = []
        visited = []
        # append the first state as (state, action_history)
        q.append([root_game, []])

        while q:
            # pop first element from queue
            node = q.pop(0)
            visited.append(node)
            
            # get the list of legal actions
            actions_list = interface.valid_actions(node)
            
            # randomizing the order of child generation
            random.shuffle(actions_list)
            
            for action_info in actions_list:
                # copy the current state
                child_state = interface.copy_state(node[0])
                
                # take action and change the copied node
                #print("action is begin")
                #print(child_state.Coordinates, action_info[0], action_info[1], action_info[3])
                output = interface.evolve(child_state, action_info[0], action_info[1], action_info[3])
                #print(action_info[0], action_info[1], action_info[3], child_state.Coordinates)
                #print("action is end")
                

                #for item in visited:
                    #if(interface.compare_two_state(item[0], child_state)):
                        #flag = False
                        #break
                #print([action_info] + node[1])
                flag = True
                # add children to queue
                if(output == 1 and flag):
                    q.append([child_state, [action_info] + node[1]])

                # return if goal test is true
                if interface.goal_state(child_state):
                    return [action_info] + node[1]
