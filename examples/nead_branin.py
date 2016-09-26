self.set_function_and_region(branin, branin_region, step=0.05)
nd = MeadNelderMethod()
nd.set_fitness_function(branin)
nd.set_time_limit(1)
agents = nd.start(save=1)

self.add_result("MEADNELDERMETHOD", agents)