"""
This file contains all the setup information for the simulation in a class object.
"""

"""
The class here sets up user-input parameters.
"""
class Config:

    # The variables for a complete-running world are found here.
    def __init__(self, 

                 # There are three variables for determining simulation space and time.
                 world_size, time_steps, sim_runs, 

                 # Here are the two amounts for limtied minds (God is +1) and objects in the simulation.
                 minds, objects,

                 # Here are the four variables for mind behavior.
                 mind_mob, mind_spd, percep_rad, imaginability, memory,

                 # Here are the two variables for mind behavior.
                 obj_mob, obj_spd,

                 # There are three Humean imagination influence variables.
                 spat_inf, temp_inf, resem_inf):

        # The world size is a tuple (x, y), time steps an integer, and sim runs an integer.
        # There will be upper limits of a 10,000 x 10,000 world, 10,000 time steps, and 10,000 runs,
        # and lower limits of a 10 x 10 world, 1 time step, and 1 run. These cannot be a tuple range.
        self.world_size = world_size
        self.time_steps = time_steps
        self.sim_runs = sim_runs

        # These set the total quantity of minds and objects as integers (of objects or minds, God is always assumed to be one).
        # The limits here are up to 1000 minds or objects, and at least 1 mind or object. These amounts can be a tuple range.
        self.minds = minds
        self.objects = objects

        # These set the general traits of the minds.
        # The limits allowed for movement based-variables are 1 to 10% of the total world size, perception from 1 tp 10% world size,
        # imagination from 0 to 100, and memory from 1 to 10. These can be tuple ranges.
        self.mind_mob = mind_mob
        self.mind_spd = mind_spd
        self.percep_rad = percep_rad
        self.imaginability = imaginability
        self.memory = memory

        # These set the general traits of the objects. The miniumum for both is 1, and a maximum will be 10% of the total world size.
        # Both of these traits can vary with a tuple.
        self.obj_mob = obj_mob
        self.obj_spd = obj_spd

        # These set the "Humean" factors that influence imagination in the minds.
        # Each of the three here must add up to 100 exactly and cannot vary with tuples.
        self.spat_inf = spat_inf
        self.temp_inf = temp_inf
        self.resem_inf = resem_inf