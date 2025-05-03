## This service allows you to insert data into database tables.

### Service working flow
## 1. Connect to the database
## 2. Fetch all available tables
## 3. Let the user choose a table to insert data into
## 4. Retrieve all column names from the selected table
## 5. Prompt the user to input the values and execute an INSERT operation

import psycopg2

def ConnectDB() :
    connect = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="483949",
        host="localhost",
        port="5432"
    )
    return connect

def GetTables(cursor) :
    cursor.execute("""SELECT table_name 
                     FROM information_schema.tables 
                     WHERE table_schema='public'""")
    
    return [row[0] for row in cursor.fetchall()]
def GetColumns(cursor, table_name) :
    cursor.execute(f"""SELECT column_name 
                      FROM information_schema.columns
                      WHERE table_name = %s""", (table_name,))
    return [row[0] for row in cursor.fetchall()]

def InsertData(cursor, connect, table_name, columns) :
    print("\nEnter values for the following columns : ")
    values = []

    cursor.execute("""SELECT LPAD((MAX(emp_id)::int + 1)::text, 5, '0') AS next_emp_id
                            FROM bm_tbm_emp;""")
    emp_id = cursor.fetchall()[0][0]

    for column in columns :
        if column == 'emp_id' :
            values.append(emp_id)
            continue

        value = input(f"{column} : ")
        
        values.append(value if value != '' else None)

    pleace_holders = ','.join(['%s']*len(columns))
    insert_query = f"INSERT INTO {table_name} VALUES ({pleace_holders})"

    try :
        cursor.execute(insert_query, values)
        connect.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e : 
        print("Deteched Error : ", e)

def main () :
    
    print('{:^40}'.format('★★★★★★★★★ Insert Data ★★★★★★★★★'))
    connect = ConnectDB()
    cursor = connect.cursor()
    tables = GetTables(cursor)
    print("The number of available tables ", str(len(tables)),"\n")

    print('{:^40}'.format('★★★★★★★★★ Table List ★★★★★★★★★'))
    for i, table in enumerate(tables, start=1) :
        print("[",i,"]",table, end="\n" )
    
    
    print('{:^40}'.format('★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★'))
    while True :
        table_choice = int(input("Select a table number to insert data into: "))
        if table_choice <= len(tables) :
            break
        print("You chose wrong number {}")
    
    table = tables[table_choice-1]
   
    if table_choice : 
        print("You chose [", table_choice, "]",tables[table_choice-1] )

    columns = GetColumns(cursor, table)
    InsertData(cursor, connect, table, columns)
    connect.close()
    


if __name__ == "__main__":
    main()
