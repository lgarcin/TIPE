vertices = [1,2,3,4]
edges = Dict(
        (1, 2) => (0, 1),
        (2, 4) => (1, 0),
        (1, 3) => (1, 0),
        (3, 4) => (0, 1),
        (3, 2) => (0, 0)
    )
source = 1
sink = 4


using JuMP, Ipopt


# Selfish routing

m = Model(solver=IpoptSolver())

@variable(m, 0 <= flow[keys(edges)] <= 1)

@objective(m, Min, sum([value[1] * flow[key] ^2 / 2 + value[2] * flow[key] for (key, value) in edges]))

for i in vertices
    @constraint(m, (i==sink ? 1 : sum([flow[key] for (key, value) in edges if key[1] == i])) == (i==source ? 1 : sum([flow[key] for (key, value) in edges if key[2] == i])))
end

solve(m)
println(getvalue(flow))

# Social routing

m = Model(solver=IpoptSolver())

@variable(m, 0 <= flow[keys(edges)] <= 1)

@objective(m, Min, sum([value[1] * flow[key] ^2 + value[2] * flow[key] for (key, value) in edges]))

for i in vertices
    @constraint(m, (i==sink ? 1 : sum([flow[key] for (key, value) in edges if key[1] == i])) == (i==source ? 1 : sum([flow[key] for (key, value) in edges if key[2] == i])))
end

solve(m)
println(getvalue(flow))
