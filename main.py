from ai import *
from sim import *
from gui import *


input='''{
"Coordinates":[
[-5,2,-6],
[-5,2,-5],
[-5,2,-4],
[-4,2,-4],
[-3,2,-4],
[-3,2,-3],
[-3,2,-2],
[-2,2,-2],
[-1,2,-2],
[-1,2,-1],
[0,2,-1],
[0,2,0],
[0,1,0],
[0,0,0],
[1,0,0],
[2,0,0],
[2,0,1],
[3,0,1],
[3,0,2],
[3,0,3],
[4,0,3],
[4,0,4],
[4,0,5],
[5,0,5],
[5,0,6],
[6,0,6],
[7,0,6]
],
"sticky_cubes":[
[5,6],
[12,13],
[14,15],
[15,16],
[18,19]
]
}'''


if __name__ == "__main__":
    interface=Interface()
    game = interface.initial_state(input)
    agent = Agent()
    gui = GUI()

    action_count=0
    print("initial map")
    gui.draw(game)
    while not (interface.goal_state(game)):
        cur_cube, before_cube, action = agent.act(input)
        
        print("attempting\n","cur_cube:", cur_cube,"\nbefore_cube:", before_cube,"\naction:", action,"\nما مکعب به شماره اول را حول مکعب با شماره دوم به اندازه زاویه مورد نظر میچرخانیم")
        interface.evolve(game,cur_cube,before_cube, action)
        gui.draw(game)
        print("\n")
        action_count+=1

    print(
        "\n\nпобеда!!!",
        "\nyour cost (number of actions):", action_count,
        '\n\ncurrent map state:'
    )
    gui.draw(game)
