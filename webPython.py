# import webbrowser 
# new = 2 # open in a new tab, if possible

# # open a public URL, in this case, the webbrowser docs
# url = "http://docs.python.org/library/webbrowser.html"
# webbrowser.get(using='google-chrome').open(url,new=new)
# print (webbrowser)






import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM stats")
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cur.fetchall()
    # print(type(rows),len(rows),rows[0])

    # with open('out_filename_login.txt', 'w') as out_file:
    #     pass
    #     # out_file.write(rows)
    #     out_file.writelines(str(rows)+'/n')
    #  .. 
    #  .. 
    #  .. parsed_line
    #  out_file.write(parsed_line)
    for row in rows:
        print(row)



# ('meta',)
# ('logins',)
# ('sqlite_sequence',)
# ('sync_entities_metadata',)
# ('sync_model_metadata',)
# ('stats',)
# ('compromised_credentials',)
# ('field_info',)



def main():
    database = r"Login_Data"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by priority:")
        select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        # select_all_tasks(conn)


if __name__ == '__main__':
    main()