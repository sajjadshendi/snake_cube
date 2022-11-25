from sim import *
import json
import copy
from sklearn.decomposition import PCA

#a class for indirect communication with simulator
class Interface:

    def __init__(self):
        pass

    #we pass our input json to this method and we get a simulator with specific coordinates and joint_cubes
    def initial_state(self, input):
        input_dict = json.loads(input)
        world_model = WorldModel(input_dict['Coordinates'], input_dict['sticky_cubes'])
        return world_model

    #we pass our simulator to this method and we get a dictionary that have simulator coordinates and joint_cubes
    def cur_state(self, world_model):
        return world_model.cur_state()

    #در این متد ما مکعب با شماره cur_cube را در راستای مکعب با شماره before_cube به اندازه زاویه action در راستای خلاف عقربه های ساعت میچرخانیم. در هر شبیه ساز مکعب ها از یک تا 27 شماره دارند. که بر اساس اندیسشان در آرایه Coordinates این شماره را میگیرند
    def evolve(self, world_model, cur_cube, before_cube, action):
        output = world_model.take_action(cur_cube, before_cube, action)
        return output

    #چک میکند که مختصات های شبیه ساز در حالت مکعب نهایی هستند یا نه
    def goal_state(self, world_model):
        return world_model.goal_state()

    #به ازای یک حالت تمام فعالیت های ممکن را میدهد. هر فعالیت به صورت یک آرایه است که خانه اول آرایه مکعبی را میدهد که باید در راستای مکعب به شماره خانه دوم آرایه بچرخد. خانه سوم آرایه راستای چرخش را میدهد. خانه چهارم درجه چرخش و خانه پنجم کدگذاری مخصوص درجه چرخش را نمایش میدهد.
    def valid_actions(self, node):
        actions = []
        inline = ""
        #تمام حالاتی که یک مکعب میتواند در راستای مکعب قبلی اش بچرخد را میدهد.
        for i in range (2,28):
            if (node[0].Coordinates[i - 1][0] != node[0].Coordinates[i - 2][0]):
                inline = 'x'
            if (node[0].Coordinates[i - 1][1] != node[0].Coordinates[i - 2][1]):
                inline = 'y'
            if (node[0].Coordinates[i - 1][2] != node[0].Coordinates[i - 2][2]):
                inline = 'z'
            actions.append([i,i-1,inline,-90,-1])
            actions.append([i,i-1,inline,90,1])
            actions.append([i,i-1,inline,180,-2])
        return actions

    #یک حالت شبیه ساز را کاملا کپی میکند
    def copy_state(self, world_model):
        new_Coordinates = copy.deepcopy(world_model.Coordinates)
        new_sticky_cubes = copy.deepcopy(world_model.sticky_cubes)
        new_worldmodel = WorldModel(new_Coordinates, new_sticky_cubes)
        return new_worldmodel

    #دو جالت مختلف شبیه ساز را از نظر تشابه مقایسه میکند
    def compare_two_state(self,world_model1, world_model2):
        mat1=[]
        first_cor = world_model1.Coordinates[0]
        for item in world_model1.Coordinates:
            point = [item[0] - first_cor[0], item[1] - first_cor[1], item[2] - first_cor[2]]
            mat1.append(point)
        mat2 = []
        first_cor = world_model2.Coordinates[0]
        for item in world_model2.Coordinates:
            point = [item[0] - first_cor[0], item[1] - first_cor[1], item[2] - first_cor[2]]
            mat2.append(point)
        return (PCA().fit_transform(mat1) == PCA().fit_transform(mat2)).all

