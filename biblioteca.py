import sqlite3
from datetime import datetime
import hashlib
from getpass import getpass

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

class UsuariRegistrat(Usuari):
    """
    Classe que hereda de Usuari i afegeix funcionalitats per gestionar usuaris registrats.

    Atributs:
        contrasenya (str): Contrasenya encriptada de l'usuari (atribut protegit).
        tipus_usuari (str): Tipus d'usuari, pot ser "lector" o "admin".
    """
    def __init__(self, tipus_usuari: str = "lector", **kwargs):
        """
        Constructor de la classe UsuariRegistrat.

        Args:
            tipus_usuari (str): Tipus d'usuari, per defecte "lector".
            **kwargs: Atributs addicionals per inicialitzar la classe base Usuari.
        """
        super().__init__(**kwargs)
        self._contrasenya = None
        self.tipus_usuari = tipus_usuari if tipus_usuari in ["lector", "admin"] else "lector"

    def _encripta_contrasenya(self, contrasenya_clara: str) -> str:
        """
        Encripta la contrasenya utilitzant hashlib.

        Args:
            contrasenya_clara (str): Contrasenya en text pla.

        Returns:
            str: Contrasenya encriptada.
        """
        return hashlib.sha256(contrasenya_clara.encode()).hexdigest()

    def introduir_contrasenya(self):
        """
        Permet introduir i encriptar la contrasenya de l'usuari.
        """
        contrasenya_clara = getpass("Introdueix la contrasenya: ")
        self._contrasenya = self._encripta_contrasenya(contrasenya_clara)
        print("Contrasenya configurada correctament.")

    def verificar_contrasenya(self, contrasenya_a_verificar: str) -> bool:
        """
        Verifica si una contrasenya coincideix amb la contrasenya encriptada.

        Args:
            contrasenya_a_verificar (str): Contrasenya a verificar.

        Returns:
            bool: True si coincideix, False en cas contrari.
        """
        return self._contrasenya == self._encripta_contrasenya(contrasenya_a_verificar)

    def imprimir_dades(self) -> str:
        """
        Sobreescriu el mètode imprimir_dades per incloure el tipus d'usuari.

        Returns:
            str: Dades de l'usuari registrat.
        """
        dades_base = super().imprimir_dades()
        return f"{dades_base}, Tipus d'usuari: {self.tipus_usuari}"

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

class Biblioteca:
    def __init__(self):
        self.conn = sqlite3.connect('biblioteca.db')
        self.crear_taules()
    
    def crear_taules(self):
        cursor = self.conn.cursor()
        
        # Crear taula d'usuaris
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuaris (
            dni TEXT PRIMARY KEY,
            nom TEXT,
            cognoms TEXT
        )
        ''')
        
        # Crear taula de llibres
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS llibres (
            titol TEXT PRIMARY KEY,
            autor TEXT,
            dni_prestec TEXT DEFAULT 'None',
            FOREIGN KEY (dni_prestec) REFERENCES usuaris(dni)
        )
        ''')
        
        self.conn.commit()
    
    def cross_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT l.titol, l.autor, u.nom, u.cognoms, u.dni
        FROM llibres l
        LEFT JOIN usuaris u ON l.dni_prestec = u.dni
        ''')
        return cursor.fetchall()
    
    def afegir_usuari(self, usuari: Usuari) -> str:
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO usuaris (dni, nom, cognoms)
            VALUES (?, ?, ?)
            ''', (usuari.dni, usuari.nom, usuari.cognoms))
            self.conn.commit()
            return "Usuari afegit correctament"
        except sqlite3.IntegrityError:
            return "Error: Ja existeix un usuari amb aquest DNI"
    
    def afegir_llibre(self, llibre: Llibre) -> str:
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO llibres (titol, autor, dni_prestec)
            VALUES (?, ?, ?)
            ''', (llibre.titol, llibre.autor, llibre.dni_prestec))
            self.conn.commit()
            return "Llibre afegit correctament"
        except sqlite3.IntegrityError:
            return "Error: Ja existeix un llibre amb aquest títol"
    
    def imprimir_usuari5(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM usuaris LIMIT 5')
        usuaris = cursor.fetchall()
        resultat = ""
        for usuari in usuaris:
            resultat += f"DNI: {usuari[0]}, Nom: {usuari[1]}, Cognoms: {usuari[2]}\n"
        return resultat if resultat else "No hi ha usuaris registrats"
    
    def imprimir_llibres(self, filtre: str = "tots") -> str:
        cursor = self.conn.cursor()
        if filtre == "prestec":
            cursor.execute('SELECT * FROM llibres WHERE dni_prestec != "None"')
        elif filtre == "disponibles":
            cursor.execute('SELECT * FROM llibres WHERE dni_prestec = "None"')
        else:
            cursor.execute('SELECT * FROM llibres')
        
        llibres = cursor.fetchall()
        resultat = ""
        for llibre in llibres:
            estat = "Prestat" if llibre[2] != "None" else "Disponible"
            resultat += f"Títol: {llibre[0]}, Autor: {llibre[1]}, Estat: {estat}\n"
        return resultat if resultat else "No hi ha llibres registrats"
    
    def eliminar_usuari(self, dni: str) -> str:
        cursor = self.conn.cursor()
        # Verificar si l'usuari té llibres en préstec
        cursor.execute('SELECT COUNT(*) FROM llibres WHERE dni_prestec = ?', (dni,))
        if cursor.fetchone()[0] > 0:
            return "Error: L'usuari té llibres en préstec. No es pot eliminar."
        
        cursor.execute('DELETE FROM usuaris WHERE dni = ?', (dni,))
        self.conn.commit()
        return "Usuari eliminat correctament" if cursor.rowcount > 0 else "Usuari no trobat"
    
    def eliminar_llibre(self, titol: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM llibres WHERE titol = ?', (titol,))
        self.conn.commit()
        return "Llibre eliminat correctament" if cursor.rowcount > 0 else "Llibre no trobat"
    
    def prestar_llibre(self, titol: str, dni: str) -> str:
        cursor = self.conn.cursor()
        
        # Verificar si l'usuari existeix
        cursor.execute('SELECT 1 FROM usuaris WHERE dni = ?', (dni,))
        if not cursor.fetchone():
            return "Error: L'usuari no existeix"
        
        # Verificar si el llibre està disponible
        cursor.execute('SELECT dni_prestec FROM llibres WHERE titol = ?', (titol,))
        resultat = cursor.fetchone()
        if not resultat:
            return "Error: El llibre no existeix"
        
        if resultat[0] != "None":
            return "Error: El llibre ja està en préstec"
        
        # Fer el préstec
        cursor.execute('UPDATE llibres SET dni_prestec = ? WHERE titol = ?', (dni, titol))
        self.conn.commit()
        return "Préstec registrat correctament"
    
    def tornar_llibre(self, titol: str) -> str:
        cursor = self.conn.cursor()
        
        # Verificar si el llibre existeix i està en préstec
        cursor.execute('SELECT dni_prestec FROM llibres WHERE titol = ?', (titol,))
        resultat = cursor.fetchone()
        if not resultat:
            return "Error: El llibre no existeix"
        
        if resultat[0] == "None":
            return "Error: El llibre no està en préstec"
        
        # Tornar el llibre
        cursor.execute('UPDATE llibres SET dni_prestec = "None" WHERE titol = ?', (titol,))
        self.conn.commit()
        return "Llibre retornat correctament"

def main():
    biblioteca = Biblioteca()
    
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Gestió d'usuaris")
        print("2. Gestió de llibres")
        print("3. Gestió de préstecs")
        print("4. Sortir")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            menu_usuaris(biblioteca)
        elif opcio == "2":
            menu_llibres(biblioteca)
        elif opcio == "3":
            menu_prestecs(biblioteca)
        elif opcio == "4":
            print("Fins aviat!")
            break
        else:
            print("Opció no vàlida. Torna a intentar.")

def menu_usuaris(biblioteca):
    while True:
        print("\n--- GESTIÓ D'USUARIS ---")
        print("1. Afegir usuari")
        print("2. Llistar usuaris")
        print("3. Eliminar usuari")
        print("4. Tornar al menú principal")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            usuari = Usuari()
            usuari.introduir_dades()
            print(biblioteca.afegir_usuari(usuari))
        elif opcio == "2":
            print("\n--- LLISTA D'USUARIS ---")
            print(biblioteca.imprimir_usuari5())
        elif opcio == "3":
            dni = input("Introdueix el DNI de l'usuari a eliminar: ")
            print(biblioteca.eliminar_usuari(dni))
        elif opcio == "4":
            break
        else:
            print("Opció no vàlida. Torna a intentar.")

def menu_llibres(biblioteca):
    while True:
        print("\n--- GESTIÓ DE LLIBRES ---")
        print("1. Afegir llibre")
        print("2. Llistar tots els llibres")
        print("3. Llistar llibres disponibles")
        print("4. Llistar llibres en préstec")
        print("5. Eliminar llibre")
        print("6. Tornar al menú principal")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            llibre = Llibre()
            llibre.introduir_dades()
            print(biblioteca.afegir_llibre(llibre))
        elif opcio == "2":
            print("\n--- TOTS ELS LLIBRES ---")
            print(biblioteca.imprimir_llibres("tots"))
        elif opcio == "3":
            print("\n--- LLIBRES DISPONIBLES ---")
            print(biblioteca.imprimir_llibres("disponibles"))
        elif opcio == "4":
            print("\n--- LLIBRES EN PRÉSTEC ---")
            print(biblioteca.imprimir_llibres("prestec"))
        elif opcio == "5":
            titol = input("Introdueix el títol del llibre a eliminar: ")
            print(biblioteca.eliminar_llibre(titol))
        elif opcio == "6":
            break
        else:
            print("Opció no vàlida. Torna a intentar.")

def menu_prestecs(biblioteca):
    while True:
        print("\n--- GESTIÓ DE PRÉSTECS ---")
        print("1. Prestar llibre")
        print("2. Tornar llibre")
        print("3. Tornar al menú principal")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            titol = input("Introdueix el títol del llibre: ")
            dni = input("Introdueix el DNI de l'usuari: ")
            print(biblioteca.prestar_llibre(titol, dni))
        elif opcio == "2":
            titol = input("Introdueix el títol del llibre a tornar: ")
            print(biblioteca.tornar_llibre(titol))
        elif opcio == "3":
            break
        else:
            print("Opció no vàlida. Torna a intentar.")

if __name__ == "__main__":
    main()