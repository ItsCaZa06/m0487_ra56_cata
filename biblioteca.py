import sqlite3
from datetime import datetime

class Usuari:
    def __init__(self, nom: str = "None", cognoms: str = "None", dni: str = "None"):
        self.nom = nom
        self.cognoms = cognoms
        self.dni = dni
    
    def imprimir_dades(self) -> str:
        return f"Nom: {self.nom}, Cognoms: {self.cognoms}, DNI: {self.dni}"
    
    def introduir_dades(self) -> str:
        self.nom = input("Introdueix el nom: ")
        self.cognoms = input("Introdueix els cognoms: ")
        self.dni = input("Introdueix el DNI: ")
        return "Dades introduïdes correctament"

class Llibre:
    def __init__(self, titol: str = "None", autor: str = "None", dni_prestec: str = "None"):
        self.titol = titol
        self.autor = autor
        self.dni_prestec = dni_prestec
    
    def imprimir_dades(self) -> str:
        estat = "Disponible" if self.dni_prestec == "None" else f"Prestat a DNI: {self.dni_prestec}"
        return f"Títol: {self.titol}, Autor: {self.autor}, Estat: {estat}"
    
    def introduir_dades(self) -> str:
        self.titol = input("Introdueix el títol: ")
        self.autor = input("Introdueix l'autor: ")
        self.dni_prestec = "None"
        return "Dades introduïdes correctament"

