import notenberechnen as nb

# Menü-Anzeige
def menu():
    # Zeigt das Hauptmenü mit aktuellen Infos
    # nc        Alle veralteten Termine entfernen
    geloeschte_termine = nb.alte_termine_loeschen()
    if geloeschte_termine > 0:
        print(f"[INFO] {geloeschte_termine} veraltete Termine automatisch gelöscht.")
    
    # Aktuelle Daten für Menü-Header laden
    termine = nb.naechste_termine(5)  # Nächste 5 Termine anzeigen
    heute = nb.heutiges_datum()       # Heutiges Datum formatiert
    
    # Kopfzeile mit schöner Formatierung ausgeben
    print("\n" * 3)
    print("+" + "-" * 58 + "+")
    print(f"|                NOTENVERWALTUNG - {heute}                |")
    print("+" + "-" * 58 + "+")
    
    # Statistiken berechnen und anzeigen
    gesamt_ung, _ = nb.gesamt_durchschnitt()  # Gesamtdurchschnitt aller Noten
    fach_anzahl = len(nb.faecher_auflisten()) # Anzahl verschiedener Fächer
    
    # Status-Zeile: Durchschnitt oder Info falls keine Noten vorhanden
    if gesamt_ung:
        print(f"| Gesamtschnitt: {gesamt_ung:.2f}     Anzahl Faecher: {fach_anzahl:<12} |")
    else:
        print(f"| Noch keine Noten eingegeben  Anzahl Faecher: {fach_anzahl:<12} |")
    print("+" + "-" * 58 + "+")
    
    # Nächste Termine anzeigen (falls vorhanden)
    if termine:
        print("\nNAECHSTE PRUEFUNGEN:")
        print("+" + "-" * 38 + "+")
        # Jeden Termin einzeln mit Datum und Fach auflisten
        for termin in termine:
            datum_text = f"| * {termin['datum']}: {termin['fach']}"
            print(f"{datum_text:<38}|")
        print("+" + "-" * 38 + "+")
    
    # Hauptmenü mit allen verfügbaren Optionen anzeigen
    # Strukturiert in 4 Kategorien: Noten, Auswertungen, Wunschnoten, Termine
    print("\n" + "=" * 60)
    print("                         HAUPTMENU")
    print("=" * 60)
    print("\n+-- NOTEN VERWALTEN ---------+    +-- AUSWERTUNGEN -----------+")
    print("|                           |    |                          |")
    print("|  [1] Note hinzufuegen     |    |  [5] Fach-Durchschnitt   |")
    print("|  [2] Note bearbeiten      |    |  [6] Alle Faecher        |")
    print("|  [3] Note loeschen        |    |                          |")
    print("|                           |    |                          |")
    print("|                           |    +--------------------------+")
    print("+---------------------------+")
    print()
    print("+-- WUNSCHNOTEN -------------+    +-- TERMINE ----------------+")
    print("|                           |    |                          |")
    print("|  [7] Wunschnote hinzu     |    | [10] Termin hinzufuegen  |")
    print("|  [8] Wunschnote aendern   |    | [11] Termin aendern      |")
    print("|  [9] Wunschnote loeschen  |    | [12] Termin loeschen     |")
    print("|                           |    |                          |")
    print("+---------------------------+    +--------------------------+")
    print("\n" + "-" * 60)
    print("                      [0] Programm beenden")
    print("-" * 60)

# Eingabe-Funktionen
def wähle_fach():
    # Lässt Benutzer ein Fach aus der Liste wählen
    # Verfügbare Fächer aus Datenbank (JSON Datei)laden
    fächer = nb.faecher_auflisten()
    if not fächer: 
        print("[X] Keine Faecher vorhanden.")
        return None  
    
    print("\nVerfuegbare Faecher:")
    # Fach-Kürzel 
    fach_kuerzel = {
        "Deutsch": "[D]",
        "Französisch": "[F]", 
        "Geschichte": "[G]",
        "Maturaarbeit": "[M]",
        "Physik": "[P]",
        "Mathematik": "[Ma]",
        "Biologie": "[B]",
        "Chemie": "[C]",
        "Geographie": "[Ge]",
        "Musik": "[Mu]",
        "Physik und Anwendungen der Mathematik": "[PAM]",
        "Informatik": "[I]",
        "Englisch": "[E]"
    }
    
    # Fächer mit Nummern auflisten für einfache Auswahl
    for i, fach in enumerate(fächer, 1):
        kuerzel = fach_kuerzel.get(fach, "[F]")  # Standard-Kürzel falls nicht definiert
        print(f"   {i}. {kuerzel} {fach}")
    print("   0. <-- Zurueck zum Hauptmenu")
    
    # Eingabe verarbeiten
    try:
        auswahl = int(input("\n> Fach waehlen: "))
        if auswahl == 0:
            return "ZURUECK"  # Spezialwert für Rückkehr zum Hauptmenü
        elif 1 <= auswahl <= len(fächer):
            return fächer[auswahl - 1]  # Gewähltes Fach zurückgeben
        else:
            print("[X] Ungueltige Auswahl!")
            return None
    except ValueError:
        print("[X] Ungueltige Eingabe!")
        return None

def eingabe_note():
    # Fordert Benutzer zur Noteneingabe auf
    try:
        # Note einlesen und auf 2 Dezimalstellen runden für Konsistenz
        return round(float(input("> Note (1.0-6.0): ")), 2)
    except ValueError:  
        print("[X] Ungueltige Note!")
        return None

def eingabe_gewichtung():
    # Fordert Benutzer zur Gewichtungseingabe auf
    try:
        gewichtung = float(input("> Gewichtung: "))
        # Gewichtung muss positiv sein (0 würde die Note bedeutungslos machen)
        if gewichtung <= 0:
            print("[X] Gewichtung muss groesser als 0 sein!")
            return None
        return gewichtung
    except ValueError:
        print("[X] Ungueltige Gewichtung!")
        return None

# Noten-Menüpunkte
def note_hinzufügen():
    # Menüpunkt: Neue Note hinzufügen
    print("\n[+] Note hinzufuegen")
    print("-" * 20)
    # Schritt 1: Fach auswählen
    fach = wähle_fach()
    if fach == "ZURUECK":
        return
    elif fach:
        # Schritt 2: Note eingeben
        note = eingabe_note()
        if note:
            # Schritt 3: Gewichtung eingeben
            gewichtung = eingabe_gewichtung()
            if gewichtung:
                # Schritt 4: Note in Datenbank speichern
                erfolg, nachricht = nb.note_hinzufuegen(fach, note, gewichtung)
                if erfolg:
                    print(f"[OK] {nachricht}")
                else:
                    print(f"[X] {nachricht}")

def noten_anzeigen():
    # Menüpunkt: Noten für ein Fach anzeigen
    print("\n[i] Noten anzeigen")
    print("-" * 20)
    fach = wähle_fach()
    if fach == "ZURUECK":
        return
    elif fach:
        # Alle Noten für das gewählte Fach laden
        noten = nb.noten_anzeigen(fach)
        if noten:
            # Zusätzliche Infos laden: Wunschnote und Durchschnitt
            wunschnote = nb.wunschnote_anzeigen(fach)
            ung, ger = nb.fach_durchschnitt(fach)
            
            # Übersichtliche Anzeige aller Informationen
            print(f"\n{fach}:")
            print(f"   Noten: {noten}")
            print(f"   Durchschnitt: {ung:.3f} (gerundet: {ger:.1f})")
            
            # Falls Wunschnote gesetzt: Berechnung anzeigen, was noch benötigt wird
            if wunschnote:
                print(f"   Wunschnote: {wunschnote}")
                print("\n   Benoetigte Noten fuer Wunschnote:")
                # Für 1-5 weitere Tests berechnen, welche Note benötigt wird
                for i in range(1, 6):
                    benoetigte = nb.benoetigte_noten_berechnen(fach, wunschnote, i)
                    if benoetigte:
                        print(f"      {i} Test(s): {benoetigte[0]}")
                    else:
                        print(f"      {i} Test(s): [X] Nicht erreichbar")
        else:
            print("[X] Keine Noten vorhanden.")

def note_bearbeiten():
    # Menüpunkt: Existierende Note bearbeiten
    fach = wähle_fach()
    if fach == "ZURUECK" or not fach:
        return  
    
    # Alle vorhandenen Noten für das Fach anzeigen
    noten = nb.noten_anzeigen(fach)
    if not noten:
        print("Keine Noten vorhanden.")
        return
    
    # Noten nummeriert auflisten zur Auswahl
    for i, note in enumerate(noten, 1):
        print(f"{i}. {note}")
    
    try:
        # Note auswählen (1-basiert, daher -1 für Array-Index)
        index = int(input("Note wählen: ")) - 1
        if 0 <= index < len(noten):
            # Neue Werte eingeben
            neue_note = eingabe_note()
            if neue_note:
                gewichtung = eingabe_gewichtung()
                if gewichtung:
                    # Änderung in Datenbank speichern
                    print(nb.note_bearbeiten(fach, index, neue_note, gewichtung)[1])
        else:
            print("Ungültige Auswahl!")
    except ValueError:
        print("Ungültige Eingabe!")

def note_löschen():
    # Menüpunkt: Note löschen
    fach = wähle_fach()
    if fach == "ZURUECK" or not fach:
        return
    
    # Vorhandene Noten anzeigen
    noten = nb.noten_anzeigen(fach)
    if not noten:
        print("Keine Noten vorhanden.")
        return
    
    # Noten zur Auswahl auflisten
    for i, note in enumerate(noten, 1):
        print(f"{i}. {note}")
    
    try:
        # Note zum Löschen auswählen
        index = int(input("Note löschen: ")) - 1
        if 0 <= index < len(noten):
            # Sicherheitsabfrage vor dem Löschen
            if input(f"Note {noten[index]} löschen? (j/n): ").lower() == 'j':
                print(nb.note_loeschen(fach, index)[1])
        else:
            print("Ungültige Auswahl!")
    except ValueError:
        print("Ungültige Eingabe!")

# Durchschnitts-Menüpunkte
def durchschnitt():
    # Menüpunkt: Durchschnitt eines Fachs anzeigen
    fach = wähle_fach()
    if fach == "ZURUECK":
        return
    elif fach:
        # Durchschnitt berechnen (ungerundet und gerundet)
        ung, ger = nb.fach_durchschnitt(fach)
        if ung:
            print(f"\n{fach}: {ung:.3f} (gerundet: {ger:.1f})")
        else:
            print("Keine Noten vorhanden.")

def alle_fächer():
    # Menüpunkt: Übersicht aller Fächer
    # Fächer alphabetisch sortiert für bessere Übersicht
    fächer = sorted(nb.faecher_auflisten())
    for fach in fächer:
        noten = nb.noten_anzeigen(fach)
        if noten:
            # Durchschnitt und optional Wunschnote anzeigen
            ung, ger = nb.fach_durchschnitt(fach)
            wunschnote = nb.wunschnote_anzeigen(fach)
            if wunschnote:
                print(f"\n{fach}: {noten} → ∅ {ung:.3f} (Wunsch: {wunschnote})")
            else:
                print(f"\n{fach}: {noten} → ∅ {ung:.3f}")
    
    # Gesamtdurchschnitt aller Fächer anzeigen
    gesamt_ung, _ = nb.gesamt_durchschnitt()
    if gesamt_ung:
        print(f"\n--- GESAMTDURCHSCHNITT ---")
        print(f"Alle Faecher: {gesamt_ung:.3f}")
    else:
        print(f"\n--- GESAMTDURCHSCHNITT ---")
        print("Keine Noten vorhanden.")

def gesamtdurchschnitt():
    # Menüpunkt: Gesamtdurchschnitt anzeigen
    # Durchschnitt über alle Fächer berechnen
    ung, _ = nb.gesamt_durchschnitt()
    if ung:
        print(f"\nGesamtdurchschnitt: {ung:.3f}")
    else:
        print("Keine Noten vorhanden.")

# Wunschnoten-Menüpunkte
def wunschnote_hinzufügen():
    # Menüpunkt: Wunschnote festlegen
    fach = wähle_fach()
    if fach == "ZURUECK":
        return
    elif fach:
        # Wunschnote eingeben und speichern
        note = eingabe_note()
        if note:
            erfolg, nachricht = nb.wunschnote_hinzufuegen(fach, note)
            if erfolg:
                print(f"[OK] {nachricht}")
            else:
                print(f"[X] {nachricht}")

def wunschnote_ändern():
    # Menüpunkt: Wunschnote ändern
    fach = wähle_fach()
    if fach == "ZURUECK":
        return
    elif fach:
        # Aktuelle Wunschnote anzeigen falls vorhanden
        aktuelle_wunschnote = nb.wunschnote_anzeigen(fach)
        if aktuelle_wunschnote:
            print(f"Aktuelle Wunschnote: {aktuelle_wunschnote}")
            # Neue Wunschnote eingeben und ändern
            neue_note = eingabe_note()
            if neue_note:
                print(nb.wunschnote_aendern(fach, neue_note)[1])
        else:
            print("Keine Wunschnote vorhanden.")

def wunschnote_löschen():
    # Menüpunkt: Wunschnote entfernen
    fach = wähle_fach()
    if fach == "ZURUECK":
        return
    elif fach:
        # Aktuelle Wunschnote anzeigen und Löschbestätigung
        aktuelle_wunschnote = nb.wunschnote_anzeigen(fach)
        if aktuelle_wunschnote:
            if input(f"Wunschnote {aktuelle_wunschnote} löschen? (j/n): ").lower() == 'j':
                print(nb.wunschnote_loeschen(fach)[1])
        else:
            print("Keine Wunschnote vorhanden.")

# Termin-Menüpunkte
def termin_hinzufügen():
    # Menüpunkt: Neuen Termin hinzufügen
    # Datum und Fach/Notiz eingeben
    datum = input("Datum (TT.MM.JJJJ) oder 0 fuer Hauptmenu: ")
    if datum == "0":
        return
    fach = input("Fach/Notiz oder 0 fuer Hauptmenu: ")
    if fach == "0":
        return
    # Termin in Datenbank speichern falls beide Eingaben gemacht wurden
    if datum and fach:
        erfolg, nachricht = nb.termin_hinzufuegen(datum, fach)
        if erfolg:
            print(f"[OK] {nachricht}")
        else:
            print(f"[X] {nachricht}")

def termin_ändern():
    # Menüpunkt: Existierenden Termin bearbeiten
    # Alle vorhandenen Termine anzeigen
    termine = nb.termine_anzeigen()
    if not termine:
        print("Keine Termine vorhanden.")
        return
    
    # Termine nummeriert zur Auswahl auflisten
    for i, termin in enumerate(termine, 1):
        print(f"{i}. {termin['datum']}: {termin['fach']}")
    print("0. <-- Zurueck zum Hauptmenu")
    
    try:
        index = int(input("Termin wählen: "))
        if index == 0:
            return
        elif 1 <= index <= len(termine):
            index = index - 1
            alter_termin = termine[index]
            print(f"Aktueller Termin: {alter_termin['datum']}: {alter_termin['fach']}")
            # Neue Werte eingeben (Enter behält alte Werte bei)
            neues_datum = input(f"Neues Datum (aktuell: {alter_termin['datum']}): ") or alter_termin['datum']
            neues_fach = input(f"Neues Fach/Notiz (aktuell: {alter_termin['fach']}): ") or alter_termin['fach']
            # Änderung speichern
            print(nb.termin_aendern(index, neues_datum, neues_fach)[1])
        else:
            print("Ungültige Auswahl!")
    except ValueError:
        print("Ungültige Eingabe!")

def termin_löschen():
    # Menüpunkt: Termin entfernen
    # Vorhandene Termine anzeigen
    termine = nb.termine_anzeigen()
    if not termine:
        print("Keine Termine vorhanden.")
        return
    
    # Termine zur Auswahl auflisten
    for i, termin in enumerate(termine, 1):
        print(f"{i}. {termin['datum']}: {termin['fach']}")
    print("0. <-- Zurueck zum Hauptmenu")
    
    try:
        index = int(input("Termin löschen: "))
        if index == 0:
            return
        elif 1 <= index <= len(termine):
            index = index - 1
            termin = termine[index]
            # Sicherheitsabfrage vor dem Löschen
            if input(f"Termin '{termin['datum']}: {termin['fach']}' löschen? (j/n): ").lower() == 'j':
                print(nb.termin_loeschen(index)[1])
        else:
            print("Ungültige Auswahl!")
    except ValueError:
        print("Ungültige Eingabe!")

# Hauptprogramm
def hauptschleife():
    # Hauptschleife - zeigt Menü und verarbeitet Eingaben
    while True:
        # Menü anzeigen
        menu()
        auswahl = input("\n> Deine Wahl: ")
        
        # Benutzereingabe auswerten und entsprechende Funktion aufrufen
        if auswahl == "1": 
            note_hinzufügen()
        elif auswahl == "2": 
            note_bearbeiten()
        elif auswahl == "3": 
            note_löschen()
        elif auswahl == "5": 
            durchschnitt()
        elif auswahl == "6": 
            alle_fächer()
        elif auswahl == "7": 
            wunschnote_hinzufügen()
        elif auswahl == "8": 
            wunschnote_ändern()
        elif auswahl == "9": 
            wunschnote_löschen()
        elif auswahl == "10": 
            termin_hinzufügen()
        elif auswahl == "11": 
            termin_ändern()
        elif auswahl == "12": 
            termin_löschen()
        elif auswahl == "0": 
            print("\nAuf Wiedersehen!")
            break  # Programm beenden
        else: 
            print("[X] Ungueltige Auswahl!")
        
        # Pause vor dem nächsten Menü-Durchlauf
        input("\n[Enter druecken zum Fortfahren...]")