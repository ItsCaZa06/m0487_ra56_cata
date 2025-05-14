# Biblioteca

Aquest projecte és una aplicació de gestió d'una biblioteca que permet administrar usuaris, llibres i préstecs. Inclou funcionalitats per afegir, llistar i eliminar usuaris i llibres, així com gestionar els préstecs de llibres entre usuaris.

## Característiques principals

- **Gestió d'usuaris**:
  - Afegir nous usuaris.
  - Llistar usuaris registrats.
  - Eliminar usuaris (només si no tenen llibres en préstec).
  - Suport per a usuaris registrats amb contrasenya encriptada i tipus d'usuari (lector/admin).

- **Gestió de llibres**:
  - Afegir nous llibres.
  - Llistar llibres disponibles, en préstec o tots.
  - Eliminar llibres.

- **Gestió de préstecs**:
  - Assignar llibres a usuaris mitjançant el DNI.
  - Retornar llibres.

- **Base de dades SQLite**:
  - Les dades dels usuaris i llibres es guarden en una base de dades SQLite (`biblioteca.db`).

## Requisits

- Python 3.8 o superior.
- Llibreries requerides (es poden instal·lar amb `pip`):
  - `sqlite3` (inclosa per defecte en Python).
  - `hashlib` (inclosa per defecte en Python).


m0487_ra56_cognomalumne/
├── [biblioteca.py](http://_vscodecontentref_/0)       # Fitxer principal amb la lògica de l'aplicació.
├── [README.md](http://_vscodecontentref_/1)           # Documentació del projecte.
├── [biblioteca.db](http://_vscodecontentref_/2)       # Base de dades SQLite (es crea automàticament).

## Classes principals
**Usuari**
Representa un usuari bàsic de la biblioteca.

**Atributs:**

nom: Nom de l'usuari.
cognoms: Cognoms de l'usuari.
dni: DNI de l'usuari.
Mètodes:

imprimir_dades(): Retorna les dades de l'usuari.
introduir_dades(): Permet introduir les dades de l'usuari.
UsuariRegistrat (herència de Usuari)
Extensió de la classe Usuari amb funcionalitats addicionals.

**Atributs:**

_contrasenya: Contrasenya encriptada (atribut protegit).
tipus_usuari: Tipus d'usuari (lector o admin).
Mètodes:

_encripta_contrasenya(): Encripta la contrasenya amb SHA-256.
introduir_contrasenya(): Permet introduir i encriptar la contrasenya.
verificar_contrasenya(): Verifica si una contrasenya coincideix amb la contrasenya encriptada.
imprimir_dades(): Inclou el tipus d'usuari en les dades.
Llibre
Representa un llibre de la biblioteca.

**Atributs:**

titol: Títol del llibre.
autor: Autor del llibre.
dni_prestec: DNI de l'usuari que té el llibre en préstec (o "None" si està disponible).
Mètodes:

imprimir_dades(): Retorna les dades del llibre.
introduir_dades(): Permet introduir les dades del llibre.
Biblioteca
Gestió centralitzada de la biblioteca.

## Mètodes:
afegir_usuari(), afegir_llibre(): Afegir usuaris o llibres.
imprimir_usuari5(), imprimir_llibres(): Llistar usuaris o llibres.
eliminar_usuari(), eliminar_llibre(): Eliminar usuaris o llibres.
prestar_llibre(), tornar_llibre(): Gestionar préstecs.

Executa el programa:

Segueix les opcions del menú principal:

Gestió d'usuaris.
Gestió de llibres.
Gestió de préstecs.
Sortir.
Contribució
Si vols contribuir al projecte, fes un fork del repositori, crea una branca amb els teus canvis i envia un pull request.

Llicència
Aquest projecte està sota la llicència MIT. Consulta el fitxer LICENSE per a més informació. ```