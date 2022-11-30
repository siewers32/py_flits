##### Uitleg tabellen #####
# cameras = flitscamera's met hun locatie
# licenses = kentekens van autos en hun gegevens van de eigenaar
# flashes = registratie van kentekens van auto's die te hard hebben en de flitspaal die ze heeft geflitst
# fines = overzicht van de boetes (bedrag) bij een overtreding.

##### Opdrachten 1 t/m 12 ######
# 1. Zorg ervoor dat je in de module dbc.py de juiste gegevens instelt voor de database-connectie
# 2. Gebruik een mysql-client om een database aan te maken.
# 3. Gebruik een mysql-client om tabellen aan te maken. Gebruik het bijgeleverde sql-bestand ('flits.sql')
# 4. Zorg ervoor dat het keuzescherm wordt getoond op het scherm
# 5. Maak de code die er voor zorgt dat een keuze wordt uitgevoerd.

from flits_modules import dbc

# Maak connectie met de database
con = dbc.conn()
tables = ['cameras', 'licenses', 'flashes', 'fines']
keuze = 0

##### Hier komt de code om een keuzescherm weer te geven #####


##### Hier komt de code om user-input te verwerken #####

keuze = 9

try:
    if keuze < 0 or keuze > 8:
        raise Exception()

    if keuze == 0:
        # Met keuze 0 worden de tabellen in de database leeggemaakt
        # De csv-files worden ingelezen de gegevens worden in de tabellen gezet.
        dbc.setup_database(con, tables)

    #### Opdracht 6  #####
    # Geef een overzicht van de flitscameras en hun locatie
    if keuze == 1:
        query = ""
        dbc.select_query(con, query)

    #### Opdracht 7  #####
    # Geef een overzicht van de boetes op 50-kilometer wegen")
    if keuze == 2:
        query = ""
        dbc.select_query(con, query)

    #### Opdracht 8  #####
    # Geef een overzicht van auto's waarvan het kenteken bestaat uit 1 letter, 3 cijfers en 2 letters (bijv. X-999-XX")
    if keuze == 3:
        query = ""
        dbc.select_query(con, query)

    #### Opdracht 9 #####
    # Geef een overzicht van overtredingen voor een bepaald kenteken
    #
    # Bekijk onderstaande code
    # Zorg ervoor dat de gebruiker een kenteken op kan geven
    # Het gegeven kenteken wordt gebruikt om op te zoeken
    if keuze == 4:
        kenteken = 0
        # == code om kenteken op te vragen == #
        try:
            query = "select l.first_name, l.last_name, l.address, l.postal_code, l.city, l.license, max_speed, speed, fi.fine from licenses l " \
                    "join flashes f on l.license = f.license " \
                    "join cameras c on f.camera_id = c.id " \
                    "join fines fi on concat(fi.speed_limit, (speed_limit + speed_excess)) = concat(c.max_speed, speed)" \
                    "where l.license like \'%" + kenteken + "%\' "
            dbc.select_query(con, query)
        except:
            print("Het ingevoerde kenteken is niet geldig")

    ##### Opdracht 10 #####
    # Geef de top 10 van camera's die de hoogste gemiddelde snelheidsoverschrijding hebben gemeten
    if keuze == 5:
        query = ""
        dbc.select_query(con, query)

    ##### Opdracht 11 ####
    # Geef de top 10 van auto's die het meest geflitst zijn
    if keuze == 6:
        query = ""
        dbc.select_query(con, query)

    ##### Opdracht 12 ####
    # Geef de top 10 van camera's die het meeste geflitst hebben
    if keuze == 7:
        query = ""
        dbc.select_query(con, query)
    # Top 10 van kentekens met het hoogste bedrag aan boetes en het aantal keer dat ze geflitst zijn.

    if keuze == 8:
        query = "select l.license,  count(l.license) as aantal_keer_geflitst, " \
                "sum(fine) as totaal_boetes from licenses l " \
                "join flashes f on l.license = f.license " \
                "join cameras c on f.camera_id = c.id " \
                "join fines fi on concat(fi.speed_limit, (speed_limit + speed_excess)) = concat(c.max_speed, speed)" \
                "group by l.license order by totaal_boetes desc limit 0,10;"
        dbc.select_query(con, query)

except:
    print("Voer een nummer in tussen 0 en 8")