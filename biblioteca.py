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

