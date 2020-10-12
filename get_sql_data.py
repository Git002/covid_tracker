from operator import index
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
    host="localhost",
    user="abhay",
    password="1234",
    database="covid_db"
)

mycursor = mydb.cursor()


class fetch_data():
    def __init__(self):
        self.STATE_NAME = "STATE_NAME"
        self.COUNNTRY_NAMES = "COUNTRY_NAMES"
        self.CONFIRMED_CASES = "CONFIRMED_CASES"
        self.TOTAL_CASES = "TOTAL_CASES"
        self.ACTIVE_CASES = "ACTIVE_CASES"
        self.RECOVERED_CASES = "RECOVERED_CASES"

    def get_data(self, cmd):
        db_connection_str = "mysql://abhay:1234@localhost/covid_db"
        db_connection = create_engine(db_connection_str)
        df = pd.read_sql(cmd, con=db_connection)
        return df

    def get_graph(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="abhay",
            password="1234",
            database="covid_db"
        )

        mycursor = mydb.cursor(buffered=True)

        mycursor.execute(
            "select CONFIRMED_CASES from india limit 20;")
        query = mycursor.fetchall()
        query = [int(x[0].replace(',', '')) for x in query]
        # print(query)

        query2 = mycursor.execute(
            "select STATE_NAME from india limit 20;")
        query2 = mycursor.fetchall()
        query2 = [x[0] for x in query2]
        # print(query2)

        mycursor.execute(
            "select TOTAL_CASES from countries limit 20;")
        query3 = mycursor.fetchall()
        query3 = [int(x[0].replace(',', '')) for x in query3]
        # print(query3)

        query4 = mycursor.execute(
            "select COUNTRY_NAMES from countries limit 20;")
        query4 = mycursor.fetchall()
        query4 = [x[0] for x in query4]
        # print(query4)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('India data and countries data horizontally stacked data')
        ax1.plot(query, query2)
        ax2.plot(query3, query4)

        ax1.ticklabel_format(style='plain', axis='x')
        ax2.ticklabel_format(style='plain', axis='x')
        plt.show()
