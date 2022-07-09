from pde import FieldCollection, PDEBase, ScalarField, UnitGrid, plot_kymographs, MemoryStorage


class SIRPDE(PDEBase):
    """SIR-model with diffusive mobility"""

    def __init__(
            self, beta=0.3, gamma=0.9, diffusivity=0.1, bc="auto_periodic_neumann"
    ):
        self.beta = beta  # transmission rate
        self.gamma = gamma  # recovery rate
        self.diffusivity = diffusivity  # spatial mobility
        self.bc = bc  # boundary condition

    def get_state(self, s, i):
        """generate a suitable initial state"""
        norm = (s + i).data.max()  # maximal density
        if norm > 1:
            s /= norm
            i /= norm
        s.label = "Susceptible"
        i.label = "Infected"

        # create recovered field
        r = ScalarField(s.grid, data=1 - s - i, label="Recovered")
        return FieldCollection([s, i, r])

    def evolution_rate(self, state, t=0):
        s, i, r = state
        diff = self.diffusivity
        ds_dt = 0*diff * s.laplace(self.bc) - self.beta * i * s
        di_dt = diff * i.laplace(self.bc) + self.beta * i * s - self.gamma * i
        dr_dt = 0*diff * r.laplace(self.bc) + self.gamma * i
        return FieldCollection([ds_dt, di_dt, dr_dt])


beta, gamma, diffusivity = 2., .1, 1.
eq = SIRPDE(beta=beta, gamma=gamma, diffusivity=diffusivity)

# initialize state
grid = UnitGrid([128])
s = ScalarField(grid, 1)
i = ScalarField(grid, 0)
i.data[0] = 1
state = eq.get_state(s, i)

# simulate the pde
storage = MemoryStorage()
sol = eq.solve(state, t_range=50, dt=1e-2, tracker=["progress", storage.tracker(1)])
plot_kymographs(storage, vmin=0, vmax=1, filename="sir1D.png")
