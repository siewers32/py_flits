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
print("2. Overzicht van de flitscameras en hun locatie")
print("3. Overzicht van de hoogte van boetes op 50-kilometer wegen")
print("4. Overzicht van auto's met een kenteken volgens sidecode 11 (= X-999-XX")
print("5. Overzicht van overtredingen voor een bepaald kenteken")
print("6. De gemiddelde snelheidsoverschrijding per wegtype")
print("7. De top 10 van auto's die het meest geflitst zijn")
print("8. De top 10 van camera's die het meeste geflitst hebben")
print("9. De top 10 met hoogst uitgedeelde boetes")
print("10. Gemiddeld aantal flitsen per dag van de week. (zondag = 0)")
print("===============================================================")

try:
    keuze = int(input("Maak een keuze: "))
    if keuze < 0 or keuze > 10:
        raise Exception()

    if keuze == 0:
        setup_csv_files(tables)

    if keuze == 1:
        setup_database(tables)

    if keuze == 2:
        query = "select id, address, city from cameras;"
        dbc.select_query(con, query)

    if keuze == 3:
        query = "select speed_excess, fine from fines where speed_limit = 50 limit 30"
        dbc.select_query(con, query)

    if keuze == 4:
        query = "select * from licenses where license like '_-___-__';"
        dbc.select_query(con, query)

    if keuze == 5:
        kenteken = input("Geef een kenteken op: ")
        try:
            query = "select l.first_name, l.last_name, l.address, l.postal_code, l.city, l.license, max_speed, speed, fi.fine from licenses l " \
                    "join flashes f on l.license = f.license " \
                    "join cameras c on f.camera_id = c.id " \
                    "join fines fi on concat(fi.speed_limit, (speed_limit + speed_excess)) = concat(c.max_speed, speed)" \
                    "where l.license like \'%" + kenteken + "%\' "
            dbc.select_query(con, query)
        except:
            print("Het ingevoerde kenteken is niet geldig")

    if keuze == 6:
        query = "select c.max_speed, avg(f.speed - c.max_speed) as gemiddelde_overschrijding " \
                "from cameras c " \
                "join flashes f on c.id = f.camera_id " \
                "group by c.max_speed " \
                "order by c.max_speed;"
        dbc.select_query(con, query)


    if keuze == 7:
        query = "select license, count(license) as aantal_keer_geflitst from flashes " \
                "group by license order by aantal_keer_geflitst desc limit 0,10";
        dbc.select_query(con, query)

    if keuze == 8:
        query = "select c.id, c.address, c.city, count(c.id) as aantal_keer_geflitst from flashes f " \
                "join cameras c on f.camera_id = c.id " \
                "group by c.id " \
                "order by aantal_keer_geflitst desc;"
        dbc.select_query(con, query)

    if keuze == 9:
        query = "select l.license,  count(l.license) as aantal_keer_geflitst, " \
                "sum(fine) as totaal_boetes from licenses l " \
                "join flashes f on l.license = f.license " \
                "join cameras c on f.camera_id = c.id " \
                "join fines fi on concat(fi.speed_limit, (speed_limit + speed_excess)) = concat(c.max_speed, speed)" \
                "group by l.license order by totaal_boetes desc limit 0,10;"
        dbc.select_query(con, query)

    if keuze == 10:
        query = "select DATE_FORMAT(expdate, '%w'), avg(speed - max_speed) from licenses l " \
                "join flashes f on l.license = f.license " \
                "join cameras c on c.id = f.camera_id group by DATE_FORMAT(expdate, '%w');"
        dbc.select_query(con, query)

except ValueError as e:
    print("Voer een nummer in tussen 1 en 10")
except:
    print("Voer een nummer in tussen 1 en 10")