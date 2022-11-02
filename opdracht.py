# Stappenplan:
# 1. Leeg tabellen in MySQL
# 2. Converteer regels tekstbestand naar list met dictionaries in python
# 3. Creeer records van gegevens in de list
# 4. Geef menu weer met opties
# 5. Voer queries uit
# 6. Formatteer en presenteer output op het scherm.


from mymodules import dbc
con = dbc.conn()


#setup
tables = ['cameras', 'licenses', 'flashes', 'fines']
def setup_csv_files(tables):
    for table in tables:
        filename = table + ".csv"
        lines = dbc.readfromdb(con, table)
        content = dbc.create_csv(lines)
        dbc.write_to_file(filename, content)

# run
def setup_database(tables):
    for table in tables:
        filename = table + ".csv"
        dbc.cleardb(con, table)

        # lines = dbc.readfromdb(con, table)
        # content = dbc.create_csv(lines)
        # dbc.write_to_file(filename, content)
        dbc.csv_to_mysql(con, table, filename)

# setup_csv_files(tables)


con = dbc.conn()
keuze = 10

print("===============================================================")
print("Maak een keuze")
print("1. Overzicht van de flitscameras en hun locatie")
print("2. Overzicht van de hoogte van boetes op 50-kilometer wegen")
print("3. Overzicht van auto's met een kenteken volgens sidecode 11 (= X-999-XX")
print("4. Overzicht van overtredingen voor een bepaald kenteken")
print("5. De top 10 van camera's die de hoogste gemiddelde snelheidsoverschrijding hebben gemeten")
print("6. De top 10 van auto's die het meest geflitst zijn")
print("7. De top 10 van camera's die het meeste geflitst hebben")
print("8. De top 10 met hoogst uitgedeelde boetes")
print("===============================================================")

try:
    ##### Opdracht ######
    # Zorg ervoor dat de gebruiker een keuze kan maken door 1 van de getoonde regelnummers te kiezen
    # Als de gebruiker iets anders intypt dan een van de regelnummers wordt er een foutmelding getoond

    if keuze == 1:
        query = ""#### OPDRACHT Geef de query die hoort bij de keuze van regel 1 #####
        dbc.select_query(con, query)

    if keuze == 2:
        query = ""#### OPDRACHT Geef de query die hoort bij de keuze van regel 2 #####
        dbc.select_query(con, query)

    if keuze == 3:
        query = ""#### OPDRACHT Geef de query die hoort bij de keuze van regel 3 #####
        dbc.select_query(con, query)

    if keuze == 4:
        #### OPDRACHT ####
        # Zorg ervoor dat de gebruiker een kenteken op kan geven
        # Het gegeven kenteken wordt gebruikt om op te zoeken

        try:
            query = "select l.first_name, l.last_name, l.address, l.postal_code, l.city, l.license, max_speed, speed, fi.fine from licenses l " \
                    "join flashes f on l.license = f.license " \
                    "join cameras c on f.camera_id = c.id " \
                    "join fines fi on concat(fi.speed_limit, (speed_limit + speed_excess)) = concat(c.max_speed, speed)" \
                    "where l.license like \'%" + kenteken + "%\' "
            dbc.select_query(con, query)
        except:
            print("Het ingevoerde kenteken is niet geldig")

    if keuze == 5:
        query = ""#### OPDRACHT Geef de query die hoort bij de keuze van regel 5 #####
        dbc.select_query(con, query)


    if keuze == 6:
        query = ""#### OPDRACHT Geef de query die hoort bij de keuze van regel 6 #####
        dbc.select_query(con, query)

    if keuze == 7:
        query = ""#### OPDRACHT Geef de query die hoort bij de keuze van regel 7 #####
        dbc.select_query(con, query)

    if keuze == 8:
        query = "select l.license,  count(l.license) as aantal_keer_geflitst, " \
                "sum(fine) as totaal_boetes from licenses l " \
                "join flashes f on l.license = f.license " \
                "join cameras c on f.camera_id = c.id " \
                "join fines fi on concat(fi.speed_limit, (speed_limit + speed_excess)) = concat(c.max_speed, speed)" \
                "group by l.license order by totaal_boetes desc limit 0,10;"
        dbc.select_query(con, query)

except:
    print("Voer een nummer in tussen 1 en 8")