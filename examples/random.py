cauchy_generators = [CauchyDistribution() for i in range(2)]
levy_generators = [LevyDistribution() for i in range(2)]
norm_generators = [NormalDistribution01() for i in range(2)]
cauchy = NDimGenerator(cauchy_generators)
levy = NDimGenerator(levy_generators)
norm = NDimGenerator(norm_generators)

points = []
for i in range(1000):
	points.append(cauchy.get())
self.add_result("cauchy", [points])

points = []
for i in range(1000):
	points.append(levy.get())
self.add_result("levy", [points])

points = []
for i in range(1000):
	points.append(norm.get())
self.add_result("norm", [points])
