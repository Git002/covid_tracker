import pymysql
from intro import Intro
import scrape
import time
from get_sql_data import fetch_data
from send_to_email import send_mail

from scrape import scrape_data_from_countries, scrape_data_from_world


Intr = Intro()
Intr.ShowTitle()
gta = fetch_data()

show_total_cmd = ['show', 'countries']
select_cmd = ['select', '*', 'from', 'india']
update_cmd = ['update', 'database']
drop_cmd = ['drop', 'database']
select_graph = ['show', 'graph']
sendmail = ['mail', 'data', 'to', 'email_address']
help_ = ['show', 'help']

db = pymysql.connect("localhost", "abhay", "1234", "covid_db")
cursor = db.cursor()


def update_cmd_handler():
    cursor.execute("""SELECT count(*) from india;""")
    db.commit()
    scrape.scrape_data_from_india()
    cursor.execute("""SELECT count(*) from world;""")
    db.commit()
    scrape.scrape_data_from_world()
    cursor.execute("""SELECT count(*) from countries;""")
    db.commit()
    scrape.scrape_data_from_countries()


while True:
    command = list(map(str, input(">> ").split()))
    command = [new_cmd.lower() for new_cmd in command]
    arr_size = len(command)
    if command == show_total_cmd:
        try:
            print(gta.get_data(cmd="SELECT COUNTRY_NAMES FROM COUNTRIES;"))
            Intr.Success()
        except:
            Intr.Warnings(cmd=Intr.NO_DATABASE_ERROR)

    elif command == "":
        Intr.Warnings()

    elif command == " ":
        Intr.Warnings()

    elif len(command) <= 1:
        Intr.Warnings()

    elif command == drop_cmd:
        try:
            cursor.execute("drop table india, world, countries;")
            db.commit()
            Intr.Success()
        except:
            Intr.Warnings(Intr.NO_TABLE_TO_DROP)
            pass

    elif command == update_cmd:
        print('Updating data...')
        time.sleep(1)
        try:
            update_cmd_handler()
            Intr.Success()
        except:
            Intr.Warnings(Intr.NO_DATABASE_ERROR)
            time.sleep(1)
            print("Creating new dataset intead...")
            scrape.scrape_data_from_india()
            scrape_data_from_countries()
            scrape_data_from_world()
            Intr.Success()

    elif command[0] == select_cmd[0] and command[-2] == select_cmd[-2]:
        lst_to_str = ' '.join(map(str, command))
        try:
            print(gta.get_data(cmd=lst_to_str))
            Intr.Success()
        except:
            Intr.Warnings(cmd=Intr.NO_DATABASE_ERROR)

    elif command == select_graph:
        gta.get_graph()
        Intr.Success()

    elif command[:2] == sendmail[:2] and len(command) == 4:
        df = gta.get_data(cmd="SELECT * FROM COUNTRIES limit 25;")
        send_mail(df=df, mail=command[-1])
        df = gta.get_data(cmd="SELECT * FROM india limit 25;")
        send_mail(df=df, mail=command[-1])

    elif command == help_:
        print("""
        1.) Select * from <database name>: india, countries, world
        2.) Show countries
        3.) update database
        4.) drop database
        5.) select graph
        6.) mail data to <email_add>
        """)

    else:
        Intr.Warnings()
