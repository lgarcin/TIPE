from pde import FieldCollection, PDEBase, ScalarField, UnitGrid, plot_kymographs, MemoryStorage


class SIRPDE(PDEBase):
    """SIR-model with diffusive mobility"""

    def __init__(self,
                 direct_transmission=0.3,
                 recovery=0.9,
                 indirect_transmission=.2,
                 shedding=10.,
                 death=0.1,
                 speed=.01,
                 diffusivity=0.1,
                 bc="auto_periodic_neumann"
                 ):
        self.direct_transmission = direct_transmission
        self.recovery = recovery
        self.indirect_transmission = indirect_transmission
        self.shedding = shedding
        self.death = death
        self.speed = speed
        self.diffusivity = diffusivity
        self.bc = bc

    def get_state(self, s, i, b):
        norm = (s + i).data.max()
        if norm > 1:
            s /= norm
            i /= norm
        s.label = "Susceptible"
        i.label = "Infected"
        b.label = "Bacteria"

        r = ScalarField(s.grid, data=1 - s - i, label="Recovered")
        return FieldCollection([s, i, r, b])

    def evolution_rate(self, state, t=0):
        s, i, r, b = state
        diff = self.diffusivity
        ds_dt = diff * s.laplace(self.bc) - self.direct_transmission * i * s - self.indirect_transmission * b * s
        di_dt = diff * i.laplace(
            self.bc) + self.direct_transmission * i * s - self.recovery * i + self.indirect_transmission * b * s
        dr_dt = diff * r.laplace(self.bc) + self.recovery * i
        db_dt = diff * b.laplace(self.bc) + self.shedding * i - self.speed * b.gradient(self.bc) - self.death * b
        return FieldCollection([ds_dt, di_dt, dr_dt, db_dt])


direct_transmission = .5
recovery = .1
indirect_transmission = .1
shedding = 1.
death = .5
speed = 1.
diffusivity = .1
eq = SIRPDE(direct_transmission=direct_transmission, recovery=recovery, indirect_transmission=indirect_transmission,
            shedding=shedding, death=death, speed=speed, diffusivity=diffusivity)

size = 128
grid = UnitGrid([size])
s = ScalarField(grid, 1)
i = ScalarField(grid, 0)
b = ScalarField(grid, 0)
b.data[size // 2] = 1
state = eq.get_state(s, i, b)

storage = MemoryStorage()
sol = eq.solve(state, t_range=100, dt=1e-2, tracker=["progress", storage.tracker(1)])
plot_kymographs(storage, vmin=0, vmax=1, filename="sirb.png")
