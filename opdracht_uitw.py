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
tables = ['cameras', 'licenses', 'flashes', 'fines']
keuze = 0

# Database connectie
con = dbc.conn()

##### Hier komt de code om een keuzescherm weer te geven #####
print("===============================================================")
print("Maak een keuze")
print("0. Tabellen leegmaken en nieuwe csv-bestanden inlezen")
print("1. Overzicht van de flitscameras en hun locatie")
print("2. Overzicht van de boetes op 50-kilometer wegen")
print("3. Overzicht van auto's waarvan het kenteken bestaat uit 1 letter, 3 cijfers en 2 letters (bijv. X-999-XX)")
print("4. Overzicht van overtredingen voor een bepaald kenteken")
print("5. De top 10 van camera's die de hoogste gemiddelde snelheidsoverschrijding hebben gemeten")
print("6. De top 10 van auto's die het meest geflitst zijn")
print("7. De top 10 van camera's die het meeste geflitst hebben")
print("8. De top 10 van kentekens met het hoogste bedrag aan boetes en het aantal keer dat ze geflitst zijn")
print("9. Stop programma")
print("===============================================================")


try:
    ##### Hier komt de code om user-input te verwerken #####
    keuze = int(input("Maak een keuze: "))
    print(keuze)
    if keuze < 0 or keuze > 9:
        raise Exception()

    if keuze == 0:
        # Met keuze 0 worden de tabellen in de database leeggemaakt
        # De csv-files worden ingelezen de gegevens worden in de tabellen gezet.
        dbc.setup_database(con, tables)

    #### Opdracht 6  #####
    # Geef een overzicht van de flitscameras en hun locatie
    if keuze == 1:
        query = "select * from cameras"
        dbc.select_query(con, query)

    #### Opdracht 7  #####
    # Geef een overzicht van de boetes op 50-kilometer wegen")
    if keuze == 2:
        query = "select speed_excess, fine from fines where speed_limit = 50 limit 30"
        dbc.select_query(con, query)

    #### Opdracht 8  #####
    # Geef een overzicht van auto's waarvan het kenteken bestaat uit 1 letter, 3 cijfers en 2 letters (bijv. X-999-XX")
    if keuze == 3:
        query = "select * from licenses where license like '%_-___-__%';"
        dbc.select_query(con, query)

    #### Opdracht 9 #####
    # Geef een overzicht van overtredingen voor een bepaald kenteken
    #
    # Bekijk onderstaande code
    # Zorg ervoor dat de gebruiker een kenteken op kan geven
    # Het gegeven kenteken wordt gebruikt om op te zoeken
    if keuze == 4:
        kenteken = str(input('Wat is het kenteken? '))
        try:
            query = "select l.first_name, l.last_name, l.address, l.postal_code, l.city, l.license, max_speed, speed from licenses l " \
                    "join flashes f on l.license = f.license " \
                    "join cameras c on f.camera_id = c.id " \
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
        query = "select l.license, c.max_speed, avg(f.speed - c.max_speed) as gemiddelde_overschrijding " \
                "from cameras c " \
                "join flashes f on c.id = f.camera_id " \
                "join licenses l on f.license = l.id " \
                "group by c.max_speed, l.license " \
                "order by gemiddelde_overschrijding desc;"
        dbc.select_query(con, query)

    ##### Opdracht 12 ####
    # Geef de top 10 van camera's die het meeste geflitst hebben
    if keuze == 7:
        query = "select license, count(license) as aantal_keer_geflitst from flashes " \
                "group by license order by aantal_keer_geflitst desc limit 0,10"
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
    print("Voer een nummer in tussen 0 en 9")