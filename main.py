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
print("0. Maak csv-files van database")
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
        setup_csv_files(tables)

    if keuze == 1:
        setup_database(tables)

    if keuze == 2:
        query = 'select license, count(license) as aantal_keer_geflitst from flashes group by license order by aantal_keer_geflitst desc';
        dbc.select_query(con, query)

    if keuze == 3:
        query = "select license,  count(license) as aantal_keer_geflitst, sum(fine) as totaal_boetes from flashes f join cameras c on f.camera_id = c.id join fines fi on fi.speed_excess = (f.speed-c.max_speed) group by license order by aantal_keer_geflitst desc;"
        dbc.select_query(con, query)

    if keuze == 4:
        print("We stoppen ermee!")

except ValueError as e:
    print("Voer een nummer in tussen 1 en 5")
except:
    print("Voer een nummer in tussen 1 en 5")