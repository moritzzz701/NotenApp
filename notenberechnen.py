import json
import math
from datetime import datetime, timedelta

# Datei-Operationen
def daten_laden():
    # Lädt Daten aus JSON-Datei
    # Wenn Datei nicht existiert wird leere Struktur zurückgegeben
    try:
        with open('daten.json', 'r', encoding='utf-8') as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {"faecher": {}}

def daten_speichern(daten):
    # Speichert Daten in JSON-Datei 
    # Mit schöner Formatierung und UTF-8 Encoding
    with open('daten.json', 'w', encoding='utf-8') as datei:
        json.dump(daten, datei, indent=2, ensure_ascii=False)

# Noten-Operationen
def note_hinzufuegen(fach, note, gewichtung=1.0):
    # Fügt Note zu einem Fach hinzu
    # Prüft zuerst ob Note im gültigen Bereich liegt
    if not (1.0 <= note <= 6.9):
        return False, "Note muss zwischen 1.0 und 6.9 liegen"
    
    daten = daten_laden()
    # Prüft ob Fach existiert
    if fach not in daten["faecher"]:    
        return False, f"Fach '{fach}' existiert nicht"
    
    # Gewichtungs-Struktur erstellen falls nicht vorhanden
    if "gewichtungen" not in daten:
        daten["gewichtungen"] = {}
    if fach not in daten["gewichtungen"]:
        daten["gewichtungen"][fach] = []
    
    # Note und Gewichtung hinzufügen
    daten["faecher"][fach].append(note)
    daten["gewichtungen"][fach].append(gewichtung)
    daten_speichern(daten)
    return True, f"Note {note} (Gewichtung {gewichtung}) zu {fach} hinzugefügt"

def note_loeschen(fach, index):
    # Löscht eine Note aus einem Fach
    # Überprüft zuerst ob Fach und Index gültig sind
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return False, f"Fach '{fach}' existiert nicht"
    if index < 0 or index >= len(daten["faecher"][fach]):
        return False, "Ungültiger Index"
    
    # Note entfernen
    geloeschte_note = daten["faecher"][fach].pop(index)
    # Auch Gewichtung löschen falls vorhanden
    if "gewichtungen" in daten and fach in daten["gewichtungen"] and index < len(daten["gewichtungen"][fach]):
        daten["gewichtungen"][fach].pop(index)
    
    daten_speichern(daten)
    return True, f"Note {geloeschte_note} aus {fach} gelöscht"

def note_bearbeiten(fach, index, neue_note, neue_gewichtung=1.0):
    # Bearbeitet eine existierende Note
    # Validiert neue Note und prüft Fach/Index
    if not (1.0 <= neue_note <= 6.9):
        return False, "Note muss zwischen 1.0 und 6.9 liegen"
    
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return False, f"Fach '{fach}' existiert nicht"
    if index < 0 or index >= len(daten["faecher"][fach]):
        return False, "Ungültiger Index"
    
    # Gewichtungsstruktur vorbereiten
    if "gewichtungen" not in daten:
        daten["gewichtungen"] = {}
    if fach not in daten["gewichtungen"]:
        daten["gewichtungen"][fach] = [1.0] * len(daten["faecher"][fach])
    
    # Note und Gewichtung aktualisieren
    alte_note = daten["faecher"][fach][index]
    daten["faecher"][fach][index] = neue_note
    
    if index < len(daten["gewichtungen"][fach]):
        daten["gewichtungen"][fach][index] = neue_gewichtung
    else:
        daten["gewichtungen"][fach].append(neue_gewichtung)
    
    daten_speichern(daten)
    return True, f"Note von {alte_note} auf {neue_note} (Gewichtung {neue_gewichtung}) geändert"

# Berechnungs-Funktionen
def durchschnitt_berechnen(noten, gewichtungen=None):
    # Berechnet gewichteten Durchschnitt

    if not noten:
        return 0.0
    
    # 1. Jede Note wird mit ihrer Gewichtung multipliziert und alle Produkte addiert
    gewichtete_summe = sum(note * gewichtung for note, gewichtung in zip(noten, gewichtungen))
    # 2. Die Summe aller verwendeten Gewichtungen berechnen (nur so viele wie Noten vorhanden)
    gesamt_gewichtung = sum(gewichtungen[:len(noten)])
    # 3. Gewichtete Summe durch Gesamtgewichtung teilen = gewichteter Durchschnitt
    return gewichtete_summe / gesamt_gewichtung

def note_runden(note):
    # Rundet Note auf halbe Noten
    return round(note * 2) / 2

def fach_durchschnitt(fach):
    # Berechnet Durchschnitt für ein Fach
    # Gibt sowohl ungerundeten als auch gerundeten Wert zurück
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return None, None
    
    noten = daten["faecher"][fach]
    if not noten:
        return None, None
    
    # Gewichtungen laden falls vorhanden
    gewichtungen = None
    if "gewichtungen" in daten and fach in daten["gewichtungen"]:
        gewichtungen = daten["gewichtungen"][fach]
    
    ungerundet = durchschnitt_berechnen(noten, gewichtungen)
    gerundet = note_runden(ungerundet)
    return ungerundet, gerundet

def gesamt_durchschnitt():
    # Berechnet Durchschnitt über alle Fächer
    # Sammelt alle Noten und Gewichtungen aus allen Fächern
    daten = daten_laden()
    alle_noten = []
    alle_gewichtungen = []
    
    for fach, fach_noten in daten["faecher"].items():
        alle_noten.extend(fach_noten)
        
        # Gewichtungen für dieses Fach laden
        if "gewichtungen" in daten and fach in daten["gewichtungen"]:
            fach_gewichtungen = daten["gewichtungen"][fach]
            # Auffüllen falls zu wenige Gewichtungen vorhanden
            while len(fach_gewichtungen) < len(fach_noten):
                fach_gewichtungen.append(1.0)
            alle_gewichtungen.extend(fach_gewichtungen[:len(fach_noten)])
        else:
            # Standard-Gewichtung wenn keine angegeben
            alle_gewichtungen.extend([1.0] * len(fach_noten))
    
    if not alle_noten:
        return None, None
    
    ungerundet = durchschnitt_berechnen(alle_noten, alle_gewichtungen)
    gerundet = note_runden(ungerundet)
    return ungerundet, gerundet

# Fach-Verwaltung
def faecher_auflisten():
    # Gibt sortierte Liste aller Fächer zurück
    # Alphabetisch sortiert
    daten = daten_laden()
    return sorted(list(daten["faecher"].keys()))

def noten_anzeigen(fach):
    # Gibt alle Noten eines Fachs zurück
    # Null wenn Fach nicht existiert
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return None
    return daten["faecher"][fach]

# Wunschnoten-Verwaltung
def wunschnote_hinzufuegen(fach, note):
    # Fügt Wunschnote für ein Fach hinzu
    # Prüft Note im Bereich 1.0-6.0 und ob Fach existiert
    if not (1.0 <= note <= 6.0):
        return False, "Note muss zwischen 1.0 und 6.0 liegen"
    
    daten = daten_laden()
    if fach not in daten["faecher"]:    
        return False, f"Fach '{fach}' existiert nicht"
    
    # Wunschnoten-Struktur erstellen falls nicht vorhanden
    if "wunschnoten" not in daten:
        daten["wunschnoten"] = {}
    if fach in daten["wunschnoten"]:
        return False, f"Wunschnote für {fach} existiert bereits (aktuell: {daten['wunschnoten'][fach]})"
    
    daten["wunschnoten"][fach] = note
    daten_speichern(daten)
    return True, f"Wunschnote {note} für {fach} gesetzt"

def wunschnote_aendern(fach, neue_note):
    # Ändert eine existierende Wunschnote
    # Prüft ob Note gültig und Wunschnote vorhanden ist
    if not (1.0 <= neue_note <= 6.0):
        return False, "Note muss zwischen 1.0 und 6.0 liegen"
    
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return False, f"Fach '{fach}' existiert nicht"
    if "wunschnoten" not in daten or fach not in daten["wunschnoten"]:
        return False, f"Keine Wunschnote für {fach} vorhanden"
    
    # Alte Note speichern und neue setzen
    alte_note = daten["wunschnoten"][fach]
    daten["wunschnoten"][fach] = neue_note
    daten_speichern(daten)
    return True, f"Wunschnote von {alte_note} auf {neue_note} geändert"

def wunschnote_loeschen(fach):
    # Löscht eine Wunschnote
    # Prüft ob Fach und Wunschnote existieren
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return False, f"Fach '{fach}' existiert nicht"
    if "wunschnoten" not in daten or fach not in daten["wunschnoten"]:
        return False, f"Keine Wunschnote für {fach} vorhanden"
    
    # Wunschnote entfernen
    geloeschte_note = daten["wunschnoten"][fach]
    del daten["wunschnoten"][fach]
    daten_speichern(daten)
    return True, f"Wunschnote {geloeschte_note} für {fach} gelöscht"

def wunschnote_anzeigen(fach):
    # Gibt Wunschnote für ein Fach zurück
    # Null wenn keine Wunschnote gesetzt ist
    daten = daten_laden()
    if "wunschnoten" not in daten or fach not in daten["wunschnoten"]:
        return None
    return daten["wunschnoten"][fach]

def benoetigte_noten_berechnen(fach, wunschnote, zusaetzliche_tests):
    # Berechnet benötigte Noten um Wunschnote zu erreichen
    # Berücksichtigt aktuelle Noten und geplante Tests
    daten = daten_laden()
    if fach not in daten["faecher"]:
        return None
    
    aktuelle_noten = daten["faecher"][fach]
    # Wenn noch keine Noten vorhanden, einfach Wunschnote zurückgeben
    if not aktuelle_noten:
        return [wunschnote] * zusaetzliche_tests
    
    # Berechnung für gewünschten Durchschnitt
    aktueller_durchschnitt = sum(aktuelle_noten)
    gesamt_tests = len(aktuelle_noten) + zusaetzliche_tests
    benoetigte_summe = wunschnote * gesamt_tests
    fehlende_summe = benoetigte_summe - aktueller_durchschnitt
    benoetigte_note = fehlende_summe / zusaetzliche_tests

    # Prüfen ob Wunschnote erreichbar ist
    if benoetigte_note > 6.9:
        return None  # Unmöglich
    if benoetigte_note < 1.0:
        benoetigte_note = 1.0
    
    return [round(benoetigte_note, 2)] * zusaetzliche_tests

# Datum und Termine
def heutiges_datum():
    # Gibt heutiges Datum als String zurück
    # Format: TT.MM.JJJJ
    return datetime.now().strftime("%d.%m.%Y")

def naechste_termine(anzahl):
    # Gibt die nächsten X Termine zurück
    # Begrenzt auf angegebene Anzahl
    daten = daten_laden()
    if "termine" not in daten:
        return []
    return daten["termine"][:anzahl]

def termin_hinzufuegen(datum, fach):
    # Fügt einen neuen Termin hinzu
    # Erstellt Terminliste falls nicht vorhanden
    daten = daten_laden()
    if "termine" not in daten:
        daten["termine"] = []
    
    # Neuen Termin zur Liste hinzufügen
    daten["termine"].append({"datum": datum, "fach": fach})
    daten_speichern(daten)
    return True, f"Termin {datum}: {fach} hinzugefügt"

def termine_anzeigen():
    # Gibt alle Termine zurück
    # Leere Liste wenn keine Termine vorhanden
    daten = daten_laden()
    if "termine" not in daten:
        return []
    return daten["termine"]

def termin_aendern(index, neues_datum, neues_fach):
    # Ändert einen existierenden Termin
    # Prüft ob Index gültig ist
    daten = daten_laden()
    if "termine" not in daten or index < 0 or index >= len(daten["termine"]):
        return False, "Ungültiger Termin"
    
    # Termin mit neuen Daten überschreiben
    daten["termine"][index] = {"datum": neues_datum, "fach": neues_fach}
    daten_speichern(daten)
    return True, f"Termin geändert zu {neues_datum}: {neues_fach}"

def termin_loeschen(index):
    # Löscht einen Termin
    # Prüft ob Index im gültigen Bereich liegt
    daten = daten_laden()
    if "termine" not in daten or index < 0 or index >= len(daten["termine"]):
        return False, "Ungültiger Termin"
    
    # Termin entfernen und Info für Bestätigung speichern
    geloeschter_termin = daten["termine"].pop(index)
    daten_speichern(daten)
    return True, f"Termin {geloeschter_termin['datum']}: {geloeschter_termin['fach']} gelöscht"

def alte_termine_loeschen():
    # Löscht automatisch veraltete Termine
    # Entfernt alle Termine die vor gestern waren
    daten = daten_laden()
    if "termine" not in daten:
        return 0
    
    # Gestern als Letzten Tag setzen
    gestern = datetime.now() - timedelta(days=1)
    gestern_datum = gestern.replace(hour=23, minute=59, second=59)
    
    alte_termine = []
    neue_termine = []
    
    # Termine durchgehen und nach Datum sortieren
    for termin in daten["termine"]:
        try:
            termin_datum = datetime.strptime(termin["datum"], "%d.%m.%Y")
            if termin_datum <= gestern_datum:
                alte_termine.append(termin)  
            else:
                neue_termine.append(termin)  
        except ValueError:
            # Bei ungültigem Datum behalten
            neue_termine.append(termin)
    
    # Nur speichern wenn Termine gelöscht wurden
    if len(alte_termine) > 0:
        daten["termine"] = neue_termine
        daten_speichern(daten)
    
    return len(alte_termine)