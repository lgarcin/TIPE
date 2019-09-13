from dataclasses import dataclass

from astropy import units as u
from astropy.coordinates import Angle, Longitude, Latitude
from astropy.time import Time
from numpy import cos, sin, concatenate, array
from scipy.optimize import root


@dataclass
class Astre:
    ascension_droite: Longitude
    declinaison: Latitude
    azimut: Longitude
    hauteur: Latitude


@dataclass
class Position:
    longitude: Longitude
    latitude: Latitude


def relations(h, Z, d, Ah, lat):
    return [
        sin(d) - sin(lat) * sin(h) - cos(lat) * cos(h) * cos(Z),
        -cos(d) * sin(Ah) - cos(h) * sin(Z),
        -cos(d) * cos(Ah) + cos(lat) * sin(h) - sin(lat) * cos(h) * cos(Z)
    ]


def localisation(heure, astres):
    hs = heure.sidereal_time('mean', longitude='greenwich')

    def fun(x):
        longitude = x[0]
        latitude = x[1]
        return concatenate([relations(astre.hauteur.radian,
                                      astre.azimut.radian,
                                      astre.declinaison.radian,
                                      longitude + hs.radian - astre.ascension_droite.radian,
                                      latitude)
                            for i, astre in enumerate(astres)])

    sol = root(fun, array([0., 0.]), method='lm').x
    return Position(longitude=Longitude(sol[0] * u.rad), latitude=Latitude(sol[1] * u.rad))


pos = localisation(Time('2019-05-18 16:50:00', scale='utc'),
                   [
                       Astre(
                           Angle('7h39m18s'),
                           Angle('5d13m38s'),
                           Angle('202d45m52s'),
                           Angle('44d25m41s')),
                       Astre(
                           Angle('8h59m12s'),
                           Angle('48d2m32s'),
                           Angle('102d12m30s'),
                           Angle('87d16m8s')),
                       Astre(
                           Angle('23h39m21s'),
                           Angle('77d37m55s'),
                           Angle('348d54m46s'),
                           Angle('39d12m29s')
                       )
                   ])
print(pos.latitude.degree, pos.longitude.degree)
