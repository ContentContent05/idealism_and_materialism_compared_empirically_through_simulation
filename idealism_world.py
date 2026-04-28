"""
The file that runs the simulation for Berkeley's Idealism worldview, creating nodes for God's mind and limited minds,
and edges for the perception relationships between them.
"""


# Here are the library imports.
import secrets


# Here are the local file imports.
from nodes_edges import Node, Edge
from config import Config


"""
This is the overall algorithm for running Berkeley's worldview, 
complete by making God and mind nodes, while objects are just ideas as edges.
"""
class IdealistWorld():

    # This takes in the configuration class and its information for initalization and updating during simulation.
    def __init__(self, config):
        self.config = config

        # This initializes the lists for both nodes and edges.
        self.nodes = []
        self.edges = []

        # This preserves position for every object edge.
        self.obj_edges = []

    # Here are where the nodes are initalized, from God to the last mind.
    def init_nodes(self):

        # These lines initalize God in the first place of the list.
        god = Node()
        god.name = "God"
        god.position = [
            self.config.world_size[0] // 2,
            self.config.world_size[1] // 2
        ]
        god.speed = 0
        self.nodes.append(god)

        # These lines intialize all other minds in the remaining places of the list.
        for mind in range(self.resolve(self.config.minds)):
            mind_node = Node()
            mind_node.name = f"Mind {mind}"
            mind_node.position = [
                secrets.randbelow(self.config.world_size[0]),
                secrets.randbelow(self.config.world_size[1])
            ]
            mind_node.mobility = self.resolve(self.config.mind_mob)
            mind_node.speed = self.resolve(self.config.mind_spd)
            mind_node.percep_rad = self.resolve(self.config.percep_rad)
            mind_node.imaginability = self.resolve(self.config.imaginability)
            self.nodes.append(mind_node)

    # Here are where the edges are initalized, form the first object to the last.
    def init_edges(self):

        # These lines intialize all objects in a certain pseudo-position, preseving them in a list to later "move".
        for obj in range(self.resolve(self.config.objects)):
            edge = Edge()
            edge.name = f"Object {obj}"
            edge.pseudo_pos = [
                secrets.randbelow(self.config.world_size[0]),
                secrets.randbelow(self.config.world_size[1])
            ]
            edge.pseudo_mob = self.resolve(self.config.obj_mob)
            edge.pseudo_spd = self.resolve(self.config.obj_spd)

            # By default, God imagines/generates and then perceives all objects.
            edge.provider_node = self.nodes[0]
            edge.receiver_node = self.nodes[0]
            self.obj_edges.append(edge)

        # This will add an additional edge if an object is perceived by a mind, and then add on all of God's self-directed edges.
        self.imagination(self.nodes)
        self.edges.extend(self.obj_edges)
        self.god_to_mind()

    # Every time a time tick passes, this manages any updatable node variables.
    def update_nodes(self, mind_nodes):

        # Here is the mind index incrementer and the start of the loop.
        mind_i = -1
        for mind in mind_nodes:

            # This decides if the mind node should move at all.
            move = secrets.randbelow(100)
            if mind.name != "God" and move < mind.mobility:

                # These lines move the mind node in a certain direction.
                dir = secrets.randbelow(4)
                if dir == 3:
                    mind.position[0] += 1 * mind.speed
                elif dir == 2:
                    mind.position[1] += 1 * mind.speed
                elif dir == 1:
                    mind.position[0] -= 1 * mind.speed
                else:
                    mind.position[1] -= 1 * mind.speed

            # These lines assure the mind node is in bounds.
            if mind.position[0] > self.config.world_size[0]:
                mind.position[0] = self.config.world_size[0]
            if mind.position[1] > self.config.world_size[1]:
                mind.position[1] = self.config.world_size[1]
            if mind.position[0] < 0:
                mind.position[0] = 0
            if mind.position[1] < 0:
                mind.position[1] = 0

            # This is to increment the index.
            mind_i += 1

    # This function updates the edges each time tick.
    def update_edges(self):

        # Every time the edge list is wiped, the preserved objects are added to be updated.
        self.edges = []
        self.imagination(self.nodes)
        self.edges.extend(self.obj_edges)

        # These "move" the objects.
        for obj in self.obj_edges:
            move = secrets.randbelow(100)
            if move < obj.pseudo_mob:
                dir = secrets.randbelow(4)
                if dir == 3:
                    obj.pseudo_pos[0] += obj.pseudo_spd
                elif dir == 2:
                    obj.pseudo_pos[1] += obj.pseudo_spd
                elif dir == 1:
                    obj.pseudo_pos[0] -= obj.pseudo_spd
                else:
                    obj.pseudo_pos[1] -= obj.pseudo_spd

            # This bounds the objects to the world boundaries.
            if obj.pseudo_pos[0] > self.config.world_size[0]:
                obj.pseudo_pos[0] = self.config.world_size[0]
            if obj.pseudo_pos[1] > self.config.world_size[1]:
                obj.pseudo_pos[1] = self.config.world_size[1]
            if obj.pseudo_pos[0] < 0:
                obj.pseudo_pos[0] = 0
            if obj.pseudo_pos[1] < 0:
                obj.pseudo_pos[1] = 0

        # The line here matches God -> Mind perception edges.
        self.god_to_mind()

    # This is used to get the distance between all objects and minds, checking any perception radius overlaps.
    def calc_dist(self, obj, mind):
        dist = ((obj.pseudo_pos[0] - mind.position[0]) ** 2 +
                (obj.pseudo_pos[1] - mind.position[1]) ** 2) ** 0.5
        return dist < mind.percep_rad

    # The function here connects all perceived object edges from God to mind.
    def god_to_mind(self):
        for obj in self.obj_edges:
            for mind in self.nodes[1:]:
                if self.calc_dist(obj, mind):
                    add_edge = Edge()
                    add_edge.name = obj.name
                    add_edge.pseudo_pos = obj.pseudo_pos
                    add_edge.provider_node = self.nodes[0]
                    add_edge.receiver_node = mind
                    self.edges.append(add_edge)

    # These lines probablistically connect a self-directed edge as an imagination.
    def imagination(self, mind_nodes):
        mind_i = -1
        for mind in mind_nodes:
            imag = secrets.randbelow(100)
            if mind.name != "God" and imag < mind.imaginability:
                imag_edge = Edge()
                imag_edge.name = f"Imagination {mind_i}"
                imag_edge.pseudo_pos = mind.position
                imag_edge.provider_node = mind
                imag_edge.receiver_node = mind
                self.edges.append(imag_edge)
            mind_i += 1

    # This function selects a value from a tuple to resolve it.
    def resolve(self, param):
        if isinstance(param, tuple):
            lo, hi = param
            return lo + secrets.randbelow(hi - lo + 1)
        return param


"""
The actual function for running and returning the graph is here.
"""
def run_isim(config, verbose):
    world = IdealistWorld(config)

    # These are metrics for node and data over time series, 
    # including total per tick, cumulative per tick, mean per tick, and change per tick.
    tot_nodes = []
    cum_nodes = []
    avg_nodes = []
    dod_nodes = []
    tot_edges = []
    cum_edges = []
    avg_edges = []
    dod_edges = []

    # First nodes and edges are initalized, and then thrown into a for loop dependent on the runs variable.
    world.init_nodes()
    world.init_edges()

    # This runs the actual iterations.
    for step in range(config.time_steps):
    
        # The line here runs the actual update of nodes and edges.
        world.update_nodes(world.nodes)
        world.update_edges()

        # The calculations for each of the four metrics for nodes.
        tot_n = len(world.nodes)
        tot_nodes.append(tot_n)
        if step == 0:
            cum_n = tot_n
        else:
            cum_n += tot_n
        cum_nodes.append(cum_n)
        avg_n = sum(tot_nodes) / len(tot_nodes)
        avg_nodes.append(avg_n)
        if step == 0:
            dod_n = tot_n
        else:
            dod_n = tot_nodes[len(tot_nodes) - 1] - tot_nodes[len(tot_nodes) - 2]
        dod_nodes.append(dod_n)

        # The calculations for each of the four metrics for edges.
        tot_e = len(world.edges)
        tot_edges.append(tot_e)
        if step == 0:
            cum_e = tot_e
        else:
            cum_e += tot_e
        cum_edges.append(cum_e)
        avg_e = sum(tot_edges) / len(tot_edges)
        avg_edges.append(avg_e)
        if step == 0:
            dod_e = tot_e
        else:
            dod_e = tot_edges[len(tot_edges) - 1] - tot_edges[len(tot_edges) - 2]
        dod_edges.append(dod_e)

    # This prints the tallying of the nodes and edges.
        if verbose:
            print("\nNODES:")
            for node in world.nodes:
                print(node.name, node.position)
            print("\nEDGES:")
            for edge in world.edges:
                print(edge.provider_node.name, "-", edge.name, "->", edge.receiver_node.name)
                print(f"Positioned at {edge.pseudo_pos}")
    if verbose:
        print(f"\nNode Totals: {tot_nodes}")
        print(f"Node Cummulations: {cum_nodes}")
        print(f"Node Averages: {avg_nodes}")
        print(f"Node Changes: {dod_nodes}")
        print(f"\nEdge Totals: {tot_edges}")
        print(f"Edge Cummulations: {cum_edges}")
        print(f"Edge Averages: {avg_edges}")
        print(f"Edge Changes: {dod_edges}")

    # Here lies the final return statement for the four data metrics on edges.
    return tot_nodes, tot_edges


"""
The main function here is for testing exaclty one simulation run with preset parameters.
Feel free to mess with the numbers (within the reasonability limits, seen on other files).
"""
def main():
    config = Config(
                 # There will be a 100 x 100 world that lasts ten time steps, the number of runs does not function here.
                 [100, 100], 10, 10, 
                 # The simulation will have five mind nodes and five objects.
                 5, 5, 
                 # The minds will have an 80% chance of moving, move five steps at a time if they do,
                 # can see in a twenty-five space radius, have a 67% chance of imagining something,
                 # and have a three-long memory bank.
                 80, 5, 25, 67, 3,
                 # The objects will have an 60% chance of moving and move three steps at a time if they do.
                 60, 3,
                 # The Humean imagination influence variables do not matter in this version of simulation.
                 50, 30, 20)
    tot_nodes, tot_edges = run_isim(config, verbose=True)
    print(f"\nIn the main file, only these will be returned:\n{tot_nodes}\n{tot_edges}")


"""
This calls the main function.
"""
if __name__ == '__main__':
    main()