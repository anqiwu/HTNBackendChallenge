import sqlite3
import requests
import queries
from argparse import ArgumentParser


def verify(conn, data):

    cur = conn.cursor()
    for index, user in enumerate(data):
        sql_verify = ''' SELECT * FROM users_skills WHERE user_id={}'''.format(index + 1)
        cur.execute(sql_verify)
        row = cur.fetchall()
        if len(row) != len(user["skills"]):
            print("NOT OK, index={}\n", index+1)
            print(user["name"])


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("TABLE CREATED")
    except ConnectionError:
        print("cannot create table")
    except sqlite3.OperationalError:
        print("fml")


def drop_table(conn, drop_table_sql):
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
        print("TABLE DROPPED")
    except ConnectionError:
        print("cannot create table")
    except sqlite3.OperationalError:
        print("fml")


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except ConnectionError:
        print("There is an error connection to the db!")
    return None


def get_data():
    url = "https://htn-interviews.firebaseio.com/users.json"
    resp = requests.get(url)
    data = resp.json()
    return data


def parse_json(list_of_users, conn):
    cur = conn.cursor()
    for user in list_of_users:
        name = user["name"]
        picture = user["picture"]
        company = user["company"]
        email = user["email"]
        phone = user["phone"]
        latitude = float(user["latitude"])
        longitude = float(user["longitude"])
        all_skills = user["skills"]
        user_info = (email, name, picture, company, phone, latitude, longitude)
        cur.execute(queries.sql_insert_user, user_info)
        cur.execute(queries.sql_insert_company, (company,))
        for skill in all_skills:
            skill_name = skill["name"]
            rating = skill["rating"]
            cur.execute(queries.sql_insert_skill, (skill_name,))
            val = cur.execute(""" SELECT skills.skill_id FROM skills WHERE skills.skill_name='{}'""".format(skill_name)).fetchone()
            cur.execute(queries.sql_insert_skill_with_rating, (skill_name, rating, val[0]))

    conn.commit()


def update_junction_table(conn, users):
    for index, user in enumerate(users):
        sql_junc_tb = '''INSERT INTO users_skills (user_id, skill_with_rating_id)
                                SELECT users.user_id AS user_id,
                                        skills_with_rating.skill_with_rating_id AS skill_with_rating_id
                                        FROM users CROSS JOIN skills_with_rating WHERE'''
        skills = user["skills"]
        cur = conn.cursor()
        for skill in skills[:-1]:
            sql_junc_tb += " (user_id={}".format(index + 1)
            sql_junc_tb += " AND skill_name='{}' AND rating={})".format(skill["name"], skill["rating"])
            sql_junc_tb += " OR"
        sql_junc_tb += " (user_id={}".format(index + 1)
        sql_junc_tb += " AND skill_name='{}' AND rating={});".format(skills[-1]["name"], skills[-1]["rating"])
        print(sql_junc_tb)
        print("\n")
        cur.execute(sql_junc_tb)

    conn.commit()


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--drop_all", default=True,
                        help="drop all tables in db if set to True")
    args = parser.parse_args()

    db_path = "./db/data.db"

    # create a database connection
    conn = create_connection(db_path)

    if args.drop_all and conn:
        print("Dropping all tables from db")
        drop_table(conn, queries.sql_drop_users_skills_table)
        drop_table(conn, queries.sql_drop_skills_table)
        drop_table(conn, queries.sql_drop_skills_with_rating_table)
        drop_table(conn, queries.sql_drop_users_table)
        drop_table(conn, queries.sql_drop_companies_table)

    if conn:
        create_table(conn, queries.sql_create_companies_table)
        create_table(conn, queries.sql_create_users_table)
        create_table(conn, queries.sql_create_skills_table)
        create_table(conn, queries.sql_create_skills_with_rating_table)
        create_table(conn, queries.sql_create_users_skills_table)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")

    data = get_data()
    parse_json(data, conn)
    update_junction_table(conn, data)

    counter = 0
    for user in data:
        counter += len(user["skills"])

    print(counter)

    verify(conn, data)


if __name__ == "__main__":
    main()
