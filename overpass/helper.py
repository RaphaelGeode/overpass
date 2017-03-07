from enum import Enum

class Country(Enum):
    Belgium = "België - Belgique - Belgien"

class BelgiumAdministrativeBoundary(Enum):
    NationalBorder = 2
    Regions = 4
    Provinces = 6
    AdministrativeArrondissements = 7
    Municipalities = 8
    Boroughs = 9

class FrenchAdministrativeBoundary(Enum):
    NationalBorder = 2
    TerritorialAreas = 3
    Regions = 4
    Circonscription = 5
    Départements = 6
    Arrondissements = 7
    Communes = 8
    Arrondissements = 9
    Quartiers = 10


(proposed / in use)	N/A	National border	(see boundary=political for linguistic communities)	Regions (NUTS1)	N/A	Provinces (NUTS2)	Administrative arrondissements (NUTS3)	Municipalities	Deelgemeenten (sections)	N/A
