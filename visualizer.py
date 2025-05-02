
import psycopg2
import json

def get_query_plan(sql):
    connect = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="483949",
        host="localhost",
        port="5432"
    )

    cursor = connect.cursor()
    try :
        cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
    except psycopg2.OperationalError as e :
        print(f"Database conection failed : {e}")
    except psycopg2.ProgrammingError as e :
        if e.pgcode == '42P01' :
            print(f"Table not found error : {e}")
        else :
            print(f"SQL error : {e}")
    except psycopg2.Error as e :
        print(f"Unexpected error is deteched : {e}")
    else :
        result = cursor.fetchone()
        print(result, end="\n=====================\n")
        print(result[0], end="\n=====================\n")
        print(result[0][0], end="\n=====================\n")
        plan = result[0][0]['Plan']
        return plan
    finally :
        cursor.close()
        connect.close()



def print_plan_tree(plan, indent=0):
    print('  ' * indent + f"-> {plan['Node Type']}")
    if 'Plans' in plan:
        for subplan in plan['Plans']:
            print_plan_tree(subplan, indent + 1)



 
query = input ("🤔INPUT YOUR QUERY : ")
print(query, end="\n")
plan = get_query_plan(query)
if query :
    if plan : 
        ##print(json.dumps(plan,indent=2 ))
        print_plan_tree(plan)
    else :
        print("There is no plan for Query.")
else :
    print("Input proper Query.")


