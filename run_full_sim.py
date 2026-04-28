"""
This file will allows the user to run the full simulation to test which philosophical worldview is more "economical" (efficient) in terms of 
the amount of "things" represented by nodes, and the amount of "causes" represented by edges. 
"""


# Here are the local file imports.
from config import Config
from idealism_world import run_isim
from materialism_world import run_msim
from run_analysis import analysis


# Here are the constants for each config list indexing.
WORLD_X = 0
WORLD_Y = 1
STEPS = 2
ITERS = 3
MINDS = 4
OBJECTS = 5
MIND_MOB = 6
MIND_SPD = 7
PERCEP = 8
IMAG = 9
MEM = 10
OBJ_MOB = 11
OBJ_SPD = 12
S_INF = 13
T_INF = 14
R_INF = 15
REQ_CONFIG_LEN = 16


# Here are the constants for each menu option.
GUIDE = 1
CONFIG = 2
SIM = 3
ANALYZE = 4
EXIT = 5


# Here are the constants for input variable bounding.
LOWER_BOUND_1 = 0
LOWER_BOUND_2 = 1
LOWER_BOUND_3 = 10
UPPER_BOUND_0 = 10
UPPER_BOUND_1 = 100
UPPER_BOUND_2 = 1000
UPPER_BOUND_3 = 10000


"""
The main function in this file acts as the user interface loop and its respective logic.
"""
def main():

    # Here is the welcome message.
    print("Welcome to a simulator comparing the worldviews of Berkeley's Idealism and Materialism with a touch of Hume!")

    # This initializes booleans for loop logic.
    menu = True
    setup = False
    simed = False
    data_dict = {}

    # This is the menu loop itself.
    while menu:

        # Here is the option selection.
        print("\nPlease choose an option to proceed.\n1. A Guide to the Simulation\n2. Configure Simulation Settings\
              \n3. Run the Configured Simulation\n4. Analyze Ran Simulation\n5. Exit\n")
        option = input()

        # The first option simply prints a long, informational message.
        if option == str(GUIDE):
            guide_msg()

        # The second requires a single line of valid input for config parameters.
        elif option == str(CONFIG):
            curr_config = config()
            print("\nConfiguration complete!")
            setup = True

        # The third runs the actual simulation, requiring at least one config stored in memory.
        elif option == str(SIM):
            if setup:
                print("\nPlease name this dataset:\n")
                set_name = naming(data_dict)
                print("\nSimulating...\n")
                simulate(curr_config, data_dict, set_name)
                print("Simulation complete!")
                simed = True
            else:
                print("\nCannot run yet, you haven't set up a configuration yet!")

        # The fourth runs and obtains an analysis query, requiring at least one simulation stored in memory.
        elif option == str(ANALYZE): 
            if simed:
                print("\nPick a set to analyze:\n\n")
                chosen = query(data_dict)
                print("\nAnalyzing...\n")
                analyze(chosen, data_dict)
                print("\nAnalysis complete!")
            else:
                print("\nCannot analyze yet, there is no simulation to analyze!")

        # The final option terminates the whole program.
        elif option == str(EXIT):
            print("\nThank you for trying this out. Bye!")
            menu = False

        # This is for the case of an invalid input outside of the given options.
        else:
            print("\nNot a valid option, please type in a number from 1-5 for one.")


"""
This will print the message informing the user behind the philosopical worldviews and how the simulation interprets and runs them.
"""
def guide_msg():

    # The message here explains both philosophical worldviews, the interpretation for simulation, and all variables
    print(
"\nAccording to George Berkeley, the Idealist, the only things in existence are minds. Limited minds cause imaginative\n\
\"weak\" ideas, and God's unlimited mind causes and coordinates \"strong\" ideas or sensory experiences. In both cases,\n\
ideas are collected into bundles known as \"objects\". Objects are not \"exsistent\" in a sense, as they are caused by\n\
\"real\" minds. So, to simulate this Idealism, a node for God's mind stems edges to all other nodes representing limited\n\
minds, where these edges represent all strong, perceived ideas. Limited minds may also direct an edge to themselves to\n\
represent weak, imaginative ideas.\n\
\n\
David Hume, on the other hand, a Materialist, claims that only objects made of matter exist and cause impressions.\n\
Material objects exist and cause impressions through their perceptible qualities, which cause ideas in minds. This\n\
worldview will be simulated by having nodes for each object which extend edges to nodes representing minds that \"bundle\"\n\
all ideas received from the relationship edges, which are the impressions or \"causes\" of ideas.\n\
\n\
This file will allows the user to run the full simulation to test which philosophical worldview is more \"economical\"\n\
(efficient) in terms of the amount of \"things\" represented by nodes, and the amount of \"causes\" represented by edges.\n\
\n\
GUIDE TO THE PARAMETERS TO SET:\n\
\n\
WORLD LENGTH (WORLD_X): integer only, 10 to 10,000 — sets the x-axis size of the world\n\
WORLD HEIGHT (WORLD_Y): integer only, 10 to 10,000 — sets the y-axis size of the world\n\
TIME STEPS (STEPS): integer only, 1 to 10,000 — sets how many time ticks each simulation run lasts\n\
ITERATIONS (ITERS): integer only, 1 to 10,000 — sets how many times the simulation repeats for data collection\n\
\n\
TOTAL MINDS (MINDS): integer or range, 1 to 1,000 — sets how many limited minds populate the world\n\
TOTAL OBJECTS (OBJECTS): integer or range, 1 to 1,000 — sets how many objects populate the world\n\
\n\
MIND MOBILITY (MIND_MOB): integer or range, 0 to 100 — percentage chance a mind moves each time tick\n\
MIND SPEED (MIND_SPD): integer or range, 1 to 10% of world size — spatial steps a mind moves when it moves\n\
PERCEPTION RADIUS (PERCEP): integer or range, 1 to 10% of world size — radius in which a mind perceives objects\n\
IMAGINABILITY (IMAG): integer or range, 0 to 100 — percentage chance a mind imagines something each time tick\n\
MEMORY LENGTH (MEM): integer or range, 1 to 10 — how many past time ticks a mind remembers for Humean influences\n\
\n\
OBJECT MOBILITY (OBJ_MOB): integer or range, 0 to 100 — percentage chance an object moves each time tick\n\
OBJECT SPEED (OBJ_SPD): integer or range, 1 to 10% of world size — spatial steps an object moves when it moves\n\
\n\
SPATIAL INFLUENCE (S_INF): integer only, must combine with T_INF and R_INF to sum to exactly 100\n\
                            share of imaginability driven by proximity of objects to the mind\n\
TEMPORAL INFLUENCE (T_INF): integer only, share of imaginability driven by recency of perceived objects\n\
RESEMBLANCE INFLUENCE (R_INF): integer only, share of imaginability driven by quality similarity of objects\n"
    )


"""
This will allow the user to set all variables or parameters on the configuration file before running a simulation.
"""
def config():
    while True:
        print("\nFor any non-world, non-Humean parameter, enter a single integer or a range as MIN-MAX.\n"
              "Example: 5 or 3-7\n"
              "S_INF + T_INF + R_INF must sum to 100.\n"
              "WORLD_X, WORLD_Y, STEPS, ITERS, MINDS, OBJECTS, MIND_MOB, MIND_SPD, PERCEP, IMAG, MEM, OBJ_MOB, OBJ_SPD, S_INF, T_INF, R_INF\n")
        param_string = input()
        param_list = config_logic(param_string)
        if param_list is None:
            print("\nInvalid input.")
            continue
        curr_config = Config(
            (param_list[WORLD_X], param_list[WORLD_Y]),
            param_list[STEPS],
            param_list[ITERS],
            param_list[MINDS],
            param_list[OBJECTS],
            param_list[MIND_MOB],
            param_list[MIND_SPD],
            param_list[PERCEP],
            param_list[IMAG],
            param_list[MEM],
            param_list[OBJ_MOB],
            param_list[OBJ_SPD],
            param_list[S_INF],
            param_list[T_INF],
            param_list[R_INF]
        )
        return curr_config


"""
This helps check validity of the user input, as well as actually inputting them into the Config class object.
"""
def config_logic(param_string):
    cleaned = param_string.replace(" ", "")
    tokens = cleaned.split(",")
    param_list = [parse_token(t) for t in tokens]
    if any(p is None for p in param_list):
        return None
    if len(param_list) < REQ_CONFIG_LEN:
        return None

    # These variables must be plain integers.
    must_be_int = [WORLD_X, WORLD_Y, STEPS, ITERS, S_INF, T_INF, R_INF]
    if any(not isinstance(param_list[i], int) for i in must_be_int):
        return None

    # The world size bounds must be 10 to 10,000.
    x = param_list[WORLD_X]
    y = param_list[WORLD_Y]
    if not (LOWER_BOUND_3 <= x <= UPPER_BOUND_3 and LOWER_BOUND_3 <= y <= UPPER_BOUND_3):
        return None

    # The time steps and iterations bounds are 1 to 10,000.
    if not (LOWER_BOUND_2 <= param_list[STEPS] <= UPPER_BOUND_3):
        return None
    if not (LOWER_BOUND_2 <= param_list[ITERS] <= UPPER_BOUND_3):
        return None

    # The sum of Humean influences must be 100.
    if param_list[S_INF] + param_list[T_INF] + param_list[R_INF] != UPPER_BOUND_1:
        return None

    # This does the 10% calculation.
    max_spd = max(x, y) // LOWER_BOUND_3

    # The limits for the amounts of minds and objects are 1 to 1000.
    if not in_bounds(param_list[MINDS], LOWER_BOUND_2, UPPER_BOUND_2):
        return None
    if not in_bounds(param_list[OBJECTS], LOWER_BOUND_2, UPPER_BOUND_2):
        return None

    # These lines bound all the mind traits.
    if not in_bounds(param_list[MIND_MOB], LOWER_BOUND_1, UPPER_BOUND_1):
        return None
    if not in_bounds(param_list[MIND_SPD], LOWER_BOUND_2, max_spd):
        return None
    if not in_bounds(param_list[PERCEP], LOWER_BOUND_2, max_spd):
        return None
    if not in_bounds(param_list[IMAG], LOWER_BOUND_1, UPPER_BOUND_1):
        return None
    if not in_bounds(param_list[MEM], LOWER_BOUND_2, UPPER_BOUND_0):
        return None

    # These lines bound all the object traits.
    if not in_bounds(param_list[OBJ_MOB], LOWER_BOUND_1, UPPER_BOUND_1):
        return None
    if not in_bounds(param_list[OBJ_SPD], LOWER_BOUND_2, max_spd):
        return None

    # This finally returns the whole list.
    return param_list


"""
Here is a helper to check a if parameter (int or tuple) is within [lo, hi].
"""
def in_bounds(p, lo, hi):
    if isinstance(p, tuple):
        return lo <= p[0] <= hi and lo <= p[1] <= hi and p[0] <= p[1]
    return lo <= p <= hi


"""
The function here parses each token as int or (int, int).
"""
def parse_token(token):
    if '-' in token:
        parts = token.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            lo, hi = int(parts[0]), int(parts[1])
            if lo <= hi:
                return (lo, hi)
        return None
    elif token.isdigit():
        return int(token)
    return None


"""
The function here checks if a name is valid or not.
"""
def naming(data_dict):
    while True:
        name = input().strip()
        if name == "":
            print("\nName cannot be empty.")
            continue
        if name in data_dict:
            print("\nName already exists, choose another.")
            continue
        return name


"""
This runs the the simulations with inputs from the configuration, and then input the sim ouputs to the data dictionary.
"""
def simulate(curr_config, data_dict, set_name):
    inode_array = []
    iedge_array = []
    mnode_array = []
    medge_array = []
    for run in range(curr_config.sim_runs):
        inode_list, iedge_list = run_isim(curr_config, verbose=False)
        mnode_list, medge_list = run_msim(curr_config, verbose=False)
        inode_array.append(inode_list)
        iedge_array.append(iedge_list)
        mnode_array.append(mnode_list)
        medge_array.append(medge_list)
    data_dict[set_name] = {
        "config": curr_config,
        "idealism": {
            "nodes": inode_array,
            "edges": iedge_array
        },
        "materialism": {
            "nodes": mnode_array,
            "edges": medge_array
        }
    }


"""
This checks if the user inputted a valid query option.
"""
def query(data_dict):
    querying = True
    while querying:
        print("\nAvailable datasets:")
        for key in data_dict:
            print(f" - {key}")
        print("\nPick a set to analyze:\n")
        chosen = input().strip()
        if chosen not in data_dict:
            print("\nDataset not found.\n")
        else:
            querying = False
    return chosen


"""
This will allow the user to query for tables and graphs once the simulation is completed and data is input.
"""
def analyze(chosen, data_dict):
    analysis(data_dict[chosen], chosen)


"""
The main function that runs once play is clicked.
"""
if __name__ == '__main__':
    main()