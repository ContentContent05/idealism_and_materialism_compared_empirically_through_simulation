"""
This file sets up the respective objects for the nodes and edges used in graphs.
"""


"""
This will initiate the node objects for God, limited minds, or objects.
"""
class Node():

    # This class is for God, a finite mind, or an object, so all respective variable requirements are here.
    def __init__(self):

        # These are for all three.
        self.name = None
        self.position = None

        # These are for both finite minds and objects.
        self.mobility = None
        self.speed = None

        # These are only for finite minds.
        self.percep_rad = None
        self.imaginability = None
        self.memory = None

        # This is only for objects.
        self.quality = None


"""
# This initiates the edges for the directed relationship edges from provider nodes (God/objects) to receiver nodes (limited minds).
"""
class Edge():

    # This class is for either sensory perceptions or imaginations, so all respective variable requirements are here.
    def __init__(self):
        self.name = None
        self.provider_node = None
        self.receiver_node = None
        self.pseudo_pos = None
        self.pseudo_mob = None
        self.pseudo_spd = None