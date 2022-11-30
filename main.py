from mymodules import dbc
con = dbc.conn()
keuze = 10
tables = ['cameras', 'licenses', 'flashes', 'fines']

##### Uitleg tabellen #####
# camera's = flitscamera's met hun locatie
# licenses = kentekens van autos en hun gegevens van de eigenaar
# flashes = registratie van kentekens van auto's die te hard hebben en de flitspaal die ze heeft geflitst
# fines = overzicht van de boetes (bedrag) bij een overtreding.

##### Opdrachten 1 t/m 12 ######
# 1. Zorg ervoor dat je in de module dbc.py de juiste gegevens instelt voor de database-connectie
# 2. Gebruik een mysql-client om een database aan te maken.
# 3. Gebruik een mysql-client om tabellen aan te maken. Gebruik het bijgeleverde sql-bestand ('flits.sql')
# 4. Plaats de csv-bestanden in dezelfde map als opdracht.py.
# 5. Zorg ervoor dat het keuzescherm wordt getoond op het scherm
# 6. Maak de code die er voor zorgt dat een keuze wordt uitgevoerd.


##### Hier komt de code om een keuzescherm weer te geven #####

# print("Maak een keuze: ") etc....


##### Hier komt de code om user-input te verwerken #####

# keuze = ....

print("===============================================================")
print("Maak een keuze")
print("0. Maak csv-files vanuit database")
print("1. Laadt csv-files in mysql")
print("2. Overzicht van top 10 meest geflitste auto's")
print("3. Overzicht van top 10 hoogste boetes")
print("4. Stoppen")
print("===============================================================")

try:
    keuze = int(input("Maak een keuze: "))
    if keuze < 0 or keuze > 4:
        raise Exception()

    if keuze == 0:
        dbc.setup_csv_files(tables)

    if keuze == 1:
        dbc.setup_database(con, tables)

    if keuze == 2:
        query = 'select license, count(license) as aantal_keer_geflitst from flashes group by license order by aantal_keer_geflitst desc';
        dbc.select_query(con, query)

    if keuze == 3:
        query = "select license,  count(license) as aantal_keer_geflitst, sum(fine) as totaal_boetes from flashes f join cameras c on f.camera_id = c.id join fines fi on fi.speed_excess = (f.speed-c.max_speed) group by license order by totaal_boetes desc;"
        dbc.select_query(con, query)

    if keuze == 4:
        print("We stoppen ermee!")

except ValueError as e:
    print("Voer een nummer in tussen 1 en 5")
except:
    print("Voer een nummer in tussen 1 en 5")