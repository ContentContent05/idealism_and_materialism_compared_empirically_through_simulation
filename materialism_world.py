"""
The file that runs the simulation for the Materialist worldview with a bit of Humean factors,
creating nodes for minds and objects and edges for the perception relationships between them.
"""


# Here are the library imports.
import secrets
import math


# Here are the local file imports.
from nodes_edges import Node, Edge
from config import Config


# Here are the constants for imagination functionality.
BIG_EXP = 64


"""
This is the overall algorithm for running the Materialist, slightly Humean worldview, 
complete by making mind and object nodes, with edges as perception and other imagination factors.
"""
class MaterialistWorld():

    # This takes in the configuration class and its information for initalization and updating during simulation.
    def __init__(self, config):
        self.config = config

        # This initializes the lists for both nodes and edges.
        self.mind_nodes = []
        self.obj_nodes = []
        self.edges = []

    # Here are where the nodes are initalized, from God to the last mind.
    def init_nodes(self):

        # These lines intialize all minds in the respective list.
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
            mind_node.memory = []
            self.mind_nodes.append(mind_node)

        # These lines intialize all other minds in the remaining places of the list.
        for obj in range(self.resolve(self.config.objects)):
            obj_node = Node()
            obj_node.name = f"Object {obj}"
            obj_node.position = [
                secrets.randbelow(self.config.world_size[0]),
                secrets.randbelow(self.config.world_size[1])
            ]
            obj_node.mobility = self.resolve(self.config.obj_mob)
            obj_node.speed = self.resolve(self.config.obj_spd)
            obj_node.quality = int.from_bytes(secrets.token_bytes(8), 'big') / (2**BIG_EXP - 1)
            self.obj_nodes.append(obj_node)

    # Every time a time tick passes, this manages any updatable node variables.
    def update_nodes(self, mind_nodes, obj_nodes):

        # Here is the loop for the minds.
        for mind in mind_nodes:

            # This decides if the mind node should move at all.
            move = secrets.randbelow(100)
            if move < mind.mobility:

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

        # Here is the loop for the objects.
        for obj in obj_nodes:

            # This decides if the mind node should move at all.
            move = secrets.randbelow(100)
            if move < obj.mobility:

                # These lines move the object node in a certain direction.
                dir = secrets.randbelow(4)
                if dir == 3:
                    obj.position[0] += 1 * obj.speed
                elif dir == 2:
                    obj.position[1] += 1 * obj.speed
                elif dir == 1:
                    obj.position[0] -= 1 * obj.speed
                else:
                    obj.position[1] -= 1 * obj.speed

            # These lines assure the object node is in bounds.
            if obj.position[0] > self.config.world_size[0]:
                obj.position[0] = self.config.world_size[0]
            if obj.position[1] > self.config.world_size[1]:
                obj.position[1] = self.config.world_size[1]
            if obj.position[0] < 0:
                obj.position[0] = 0
            if obj.position[1] < 0:
                obj.position[1] = 0

    # Here are where the edges are initalized, forming the first mind-object pair to the last.
    def update_edges(self):

        # This is to reset the already recorded edges.
        self.edges = []

        # These lines make the connects of all perceived objects to minds.
        perceived_by = {mind: [] for mind in self.mind_nodes}
        for mind in self.mind_nodes:
            for obj in self.obj_nodes:
                if self.calc_dist(obj, mind) < mind.percep_rad:
                    edge = Edge()
                    edge.provider_node = obj
                    edge.receiver_node = mind
                    self.edges.append(edge)
                    perceived_by[mind].append(obj)

        # This updates memory banks with this step's perceptions.
        for mind in self.mind_nodes:
            self.update_memory(mind, perceived_by[mind])

        # This runs the imagination collapse for each mind.
        for mind in self.mind_nodes:
            self.imagination(mind, self.obj_nodes)


    # This is used to get the distance between all objects and minds, checking any perception radius overlaps.
    def calc_dist(self, obj, mind):

        # The calculation for intersection is simply the square root formula.
        dist = ((obj.position[0] - mind.position[0]) ** 2 +
                (obj.position[1] - mind.position[1]) ** 2) ** 0.5
        return dist

    # This method updates the memory banks of each mind node.
    def update_memory(self, mind, perceived_objects):
        
        # The perceived_objects is a list of object nodes perceived this step by this mind,
        # and this removes this step's objects from wherever they already sit in memory
        # (if re-perceived, they return to front rather than duplicating).
        cleaned_bank = [
            [obj for obj in slot if obj not in perceived_objects]
            for slot in mind.memory
        ]

        # This drops any empty slots.
        cleaned_bank = [slot for slot in cleaned_bank if slot]

        # This inserts current perceptions as the new front slot.
        if perceived_objects:
            mind.memory = [perceived_objects] + cleaned_bank
        else:
            mind.memory = cleaned_bank

        # Here trims to the maximum configured length for an object's memory.
        mind.memory = mind.memory[:self.resolve(self.config.memory)]

    # These lines probablistically connect a self-directed edge as an imagination.
    def imagination(self, mind, all_objects):
        if not all_objects:
            return

        # Here calls all weights of the Humean factors.
        s_w = self.spatial_weights(mind, all_objects)
        t_w = self.temporal_weights(mind, all_objects)
        r_w = self.resemblance_weights(mind, all_objects)

        # This combines each influence, scaled by its parameter.
        combined = {}
        for obj in all_objects:
            combined[obj] = (self.config.spat_inf * s_w[obj] +
                             self.config.temp_inf * t_w[obj] +
                             self.config.resem_inf * r_w[obj])

        # Add base imaginability as a flat floor so imagination
        # can still fire even when all influences are zero.
        total = sum(combined.values())
        if total == 0:
            # Flat uniform distribution — any object equally likely
            chosen = secrets.choice(all_objects)
        else:
            # Normalize into a probability distribution
            norm = {obj: w / total for obj, w in combined.items()}

            # Here, secrets builds the cumulative distribution.
            roll = int.from_bytes(secrets.token_bytes(8), 'big') / (2**BIG_EXP - 1)
            cumulative = 0.0
            chosen = all_objects[-1]    # fallback
            for obj, prob in norm.items():
                cumulative += prob
                if roll < cumulative:
                    chosen = obj
                    break

        # Check base imaginability before committing the edge
        imag_roll = secrets.randbelow(100)
        if imag_roll < mind.imaginability:
            imag_edge = Edge()
            imag_edge.name = f"Imagination of {chosen.name} by {mind.name}"
            imag_edge.provider_node = chosen
            imag_edge.receiver_node = mind
            self.edges.append(imag_edge)

    # This function runs the algorithm for imagination with the Humean variables in mind.
    def imagination(self, mind, all_objects):
        if not all_objects:
            return

        # This scores every object on each of the three Humean influences.
        s_w = self.spatial_weights(mind, all_objects)
        t_w = self.temporal_weights(mind, all_objects)
        r_w = self.resemblance_weights(mind, all_objects)

        # These lines merge the three scores into one weighted score per object,
        # using the influence proportions from config as the weights.
        combined = {}
        s_prop = self.config.spat_inf / 100
        t_prop = self.config.temp_inf / 100
        r_prop = self.config.resem_inf / 100
        for obj in all_objects:
            combined[obj] = (s_prop * s_w[obj] +
                             t_prop * t_w[obj] +
                             r_prop * r_w[obj])

        # If every object scored zero on all influences, this falls back to uniform random.
        total = sum(combined.values())
        if total == 0:
            chosen = secrets.choice(all_objects)
        else:

            # This normalizes the combined scores into a probability distribution summing to 1.
            norm = {obj: w / total for obj, w in combined.items()}

            # This samples a random point on the distribution to select the imagined object, where
            # higher-weighted objects occupy more of the 0-1 range and are more likely to be chosen.
            roll = int.from_bytes(secrets.token_bytes(8), 'big') / (2**BIG_EXP - 1)
            cumulative = 0.0
            chosen = all_objects[-1]
            for obj, prob in norm.items():
                cumulative += prob
                if roll < cumulative:
                    chosen = obj
                    break

        # The imaginability here is the "gate" that decides whether imagination fires at all, and
        # the object selection above only matters if this check passes.
        imag_roll = secrets.randbelow(100)
        if imag_roll < mind.imaginability:
            imag_edge = Edge()
            imag_edge.name = f"Imagination of {chosen.name} by {mind.name}"
            imag_edge.provider_node = chosen
            imag_edge.receiver_node = mind
            self.edges.append(imag_edge)

    # Here are where the spatial weights are determined.
    def spatial_weights(self, mind, all_objects):
        weights = {obj: 0.0 for obj in all_objects}
        for obj in all_objects:
            dist = self.calc_dist(obj, mind)
            if dist < mind.percep_rad:
                weights[obj] = 1.0 - (dist / mind.percep_rad)
        return weights
    
    # Here are where the temporal weights are determined.
    def temporal_weights(self, mind, all_objects):
        
        # This returns a dictionary, and handles the case of an empty memory
        weights = {obj: 0.0 for obj in all_objects}
        L = len(mind.memory)
        if L == 0:
            return weights

        # These lines perform the logarithmic algorithm for diminishing influence when less recent.
        for k, slot in enumerate(mind.memory):
            slot_weight = math.log(L - k + 1)
            per_obj = slot_weight / len(slot)
            for obj in slot:
                weights[obj] += per_obj
        return weights
    
    # Here are where the resemblance weights are determined.
    def resemblance_weights(self, mind, all_objects):
        weights = {obj: 0.0 for obj in all_objects}
        if not mind.memory:
            return weights

        # Here is where the objects from the last step are used.
        recent = mind.memory[0]
        if not recent:
            return weights

        # This averages the qualities of the most recently perceived objects.
        ref_quality = sum(obj.quality for obj in recent) / len(recent)

        # This is where the weights are returned based on similarity, and then returned.
        for obj in all_objects:
            similarity = 1.0 - abs(obj.quality - ref_quality)
            weights[obj] = similarity
        return weights
    
    # This function selects a value from a tuple to resolve it.
    def resolve(self, param):
        if isinstance(param, tuple):
            lo, hi = param
            return lo + secrets.randbelow(hi - lo + 1)
        return param


"""
The actual function for running and returning the graph is here.
"""
def run_msim(config, verbose):
    world = MaterialistWorld(config)

    # These are metrics for edge data over time series, 
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
    world.update_edges()

    # This runs the actual iterations.
    for step in range(config.time_steps):
    
        # The line here runs the actual update of nodes and edges.
        world.update_nodes(world.mind_nodes, world.obj_nodes)
        world.update_edges()

        # The calculations for each of the four metrics for nodes.
        tot_n = len(world.mind_nodes + world.obj_nodes)
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
            for node in world.mind_nodes:
                print(node.name, node.position)
            for node in world.obj_nodes:
                print(node.name, node.position)
            print("\nEDGES:")
            for edge in world.edges:
                if edge.name is None:
                    print(edge.provider_node.name, "- Perceived By ->", edge.receiver_node.name)
                else:
                    print(edge.provider_node.name, "- Imagined By ->", edge.receiver_node.name)
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
                 # The simulation will have five mind nodes and five objects
                 5, 5, 
                 # The minds will have an 80% chance of moving, move five steps at a time if they do,
                 # can see in a twenty-five space radius, have a 2/3 chance of imagining something,
                 # and have a three-long memory bank.
                 80, 5, 25, 67, 3,
                 # The objects will have an 60% chance of moving and move three steps at a time if they do.
                 60, 3,
                 # An object's distance influence 50% of imagination, its recency 30%, and similarity to others 20%.
                 50, 30, 20)
    tot_nodes, tot_edges = run_msim(config, verbose=True)
    print(f"\nIn the main file, only these will be returned:\n{tot_nodes}\n{tot_edges}")


"""
This calls the main function.
"""
if __name__ == '__main__':
    main()