self.set_function_and_region(becker_lago, becker_lago_region, step=0.05)
nd = GlowwormSwarmOptimization(region=becker_lago_region)

nd.set_fitness_function(becker_lago)
nd.init_population(gen_count=20)
nd.set_time_limit(1)
agents = nd.start(save=1)

self.add_result("gso", agents)