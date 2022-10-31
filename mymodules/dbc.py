import pymysql
import csv

def conn():
    return pymysql.connect(host='localhost',
                          user='root',
                          password='root',
                          database='flits',
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
                sql = 'INSERT INTO ' + table + ' (' + fields + ')' + ' VALUES (' + placeholders + ')'
                cursor.execute(sql, row)
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