self.set_function_and_region(branin, branin_region, step=0.05)
nd = ChargedSystemSearch(region=branin_region)

nd.set_fitness_function(branin)
nd.init_population(gen_count=10)
nd.set_time_limit(1)
agents = nd.start(save=1)

self.add_result("css", agents)