
edge_values = [("dist", None), 
				  ("pheromone", None)]
node_values = [("pos", PositionGenerator(region=branin_region))]
gg = RandomGraphGenerator(edge_chance=1.0, # generate complete graph
								edge_values = edge_values, # fill values
								node_values = node_values # fill node values
								)

graph = gg.get()
aa = ArtificalAnts_TS(graph)
aa.set_time_limit(3)
graphs = aa.start(save=10)

best_ever = float('inf')
for iteration in graphs:
	if best_ever > graph["best"]:
		best_ever = graph["best"]
	graph = iteration[0]
	print("Best value:", graph["best"])
print("Best ever", best_ever)
self.add_result("graph", graphs)