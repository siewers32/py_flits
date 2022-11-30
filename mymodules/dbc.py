import pymysql
import csv

def conn():
    return pymysql.connect(host='localhost',
                          user='root',
                          password='root',
<<<<<<< HEAD
                          database='rdw2',
=======
                          database='flits',
>>>>>>> b293568e2aadf22a8e14c9aac760ace252b03881
                          port=8889,
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

def cleardb(con, table):
    try:
        with con.cursor() as cur:
            sql = "DELETE FROM " + table
            cur.execute(sql)
            con.commit()
            print(f"MySQL tabel { table } is leeggemaakt")
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        return False
    except:
        print("Tabel leemaken is mislukt!")

def readfromdb(con, table):
    sql = "select * from " + table
    try:
        with con.cursor() as cur:
            cur.execute(sql)
            con.commit()
            lines = []
            line = {}
            for rows in cur:
                for row in rows:
                    # print(row)
                    line[row] = str(rows[row])
                lines.append(line)
                line = {}
        return lines
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        return False


def create_csv(lines):
    try:
        content = ", ".join([str(i) for i in lines[0]]) + "\n"

        for line in lines:
            keys, values = zip(*line.items())
            content = content + ', '.join([str(i) for i in values]) + "\n"
        return content
    except IndexError as e:
        print(f"Error in create_csv: {e}")
    except:
        print("Error in create_csv")



def write_to_file(file, content):
    f = open(file, 'wt')
    f.write(content)
    f.close

def csv_to_dict(file):
    with open(file, mode='r') as infile:
        lines = csv.reader(infile)
        print(lines[0])

def csv_to_mysql(con, table, file):
    try:
        fields = ""
        cursor = con.cursor()
        csv_data = csv.reader(open(file))
        for row in csv_data:
            if row[0] == 'id':
                fields = ', '.join([str(i) for i in row])
                placeholders = ', '.join(['%s' for i in range(len(row))])
            else:
                sanitized = []
                for r in row:
                    sanitized.append(r.strip())
                sql = 'INSERT INTO ' + table + ' (' + fields + ')' + ' VALUES (' + placeholders + ')'
                cursor.execute(sql, sanitized)
        con.commit()
        print(f"Gegevens uit { file } zijn succesvol overgezet naar tabel { table }")
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        return False
    except:
        print("records toevoegen is mislukt")
        # cursor.close()

def select_query(con, sql):
    try:
         with con.cursor() as cur:
            cur.execute(sql)
            con.commit()
            for rows in cur:
                for row in rows:
                    print(rows[row], end="\t")
                print("")
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        return False
    finally:
        con.close()

def setup_database(con, tables):
    for table in tables:
        filename = table + ".csv"
        cleardb(con, table)
        csv_to_mysql(con, table, filename)

def setup_csv_files(con, tables):
    for table in tables:
        filename = table + ".csv"
        lines = readfromdb(con, table)
        content = create_csv(lines)
        write_to_file(filename, content)