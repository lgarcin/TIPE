from dataclasses import dataclass

from numpy import cos, sin, concatenate, pi, array
from scipy.optimize import root

from astropy.coordinates import Angle, Longitude, Latitude
from astropy.time import Time
from astropy import units as u


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


pos = localisation(Time('2019-05-09 07:46:00', scale='utc'),
                   [
                       Astre(
                           Angle('1h51m27s'),
                           Angle('-10d20m5s'),
                           Angle('135d17m0s'),
                           Angle('20d19m0s')),
                       Astre(
                           Angle('21h18m34s'),
                           Angle('62d35m7s'),
                           Angle('323d31m57s'),
                           Angle('69d56m50s')),
                       Astre(
                           Angle('17h34m56s'),
                           Angle('12d33m37s'),
                           Angle('272d47m35s'),
                           Angle('14d20m22s')
                       )
                   ])
print(pos.latitude.degree, pos.longitude.degree)
