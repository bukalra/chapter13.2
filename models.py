import sqlite3
from sqlite3 import Error

create_table_sql = """
   -- projects table
   CREATE TABLE IF NOT EXISTS todos (
      title test,
      description text,
      done text,
      id integer PRIMARY KEY
   );
   """

class Todos:
    def __init__(self, filename):
        self.filename = filename
        
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def execute_sql(self, conn, sql):
        """ Execute sql
        :param conn: Connection object
        :param sql: a SQL script
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def add_todo(self, conn, todo):
        """
        Create a new projekt into the projects table
        :param conn:
        :param projekt:
        :return: projekt id
        """
        sql = '''INSERT INTO todos(title, description, done)
                VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, todo)
        conn.commit()
        return cur.lastrowid

    def all(self, conn, table='todos'):
        """
        Query all rows in the table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows
 
    def get(self, conn, id):

        cur = conn.cursor()
        cur.execute("SELECT * FROM todos WHERE id=?", (id,))

        rows = cur.fetchall()
        return rows

    def update(self, conn, id, table = "todos", **kwargs):
        """
        update status, begin_date, and end date of a task
        :param conn:
        :param table: table name
        :param id: row id
        :return:
        """
        parameters = [f"{k} = ?" for k in kwargs.keys()]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
                    SET {parameters}
                    WHERE id = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

todos = Todos("database.db")