# Covid Tracker
>This is a school project made by me for my `IP Practicals` of 2021 for my `12th Board exams`. For those who want to _quickly_ make the project and have _no time_ to make their own and want to _shine on_ then feel free to copy ;)

# Requirements:
- [x] Windows 7 SP1
- [X] Python 3.8.3
- [x] Selenium 3.141.0
- [x] Pandas
- [X] smtplib
- [x] sqlalchemy
- [x] pymysql
- [x] matplotlib
- [x] MySql version 8.0 command line

# Explaining the project
The project has basically many modules the one to start off is the `main.py`
Just open it, and it will show you the screen like this:

![Main.py](https://i.postimg.cc/5NCsw5ss/Capture.png)

The code behind this screen is based on two modules: `main.py`, `intro.py`
Here's `main.py`:
```
import pymysql
import time

# my own modules...
import scrape
from intro import Intro
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

```
Now the `intro.py`
It is responsible for the "Covid Tracker" text art in the front. Here's what it looks like:
```
import click
import os


class Intro():
    def __init__(self):
        self.NO_DATABASE_ERROR = "NO_DATABASE_ERROR"
        self.NO_TABLE_TO_DROP = "NO_TABLE_TO_DROP"
        self.WRONG_EMAIL = "WRONG_EMAIL"

    def ShowTitle(self):
        os.system("cls")
        click.secho(""" _______  _______          _________ ______              __     _____  
(  ____ \(  ___  )|\     /|\__   __/(  __  \            /  \   / ___ \ 
| (    \/| (   ) || )   ( |   ) (   | (  \  )           \/) ) ( (   ) )
| |      | |   | || |   | |   | |   | |   ) |   _____     | | ( (___) |
| |      | |   | |( (   ) )   | |   | |   | |  (_____)    | |  \____  |
| |      | |   | | \ \_/ /    | |   | |   ) |             | |       ) |
| (____/\| (___) |  \   /  ___) (___| (__/  )           __) (_/\____) )
(_______/(_______)   \_/   \_______/(______/            \____/\______/                                                                                                                           
      """, fg='yellow')

        click.secho("""_________ _______  _______  _______  _        _______  _______ 
\__   __/(  ____ )(  ___  )(  ____ \| \    /\(  ____ \(  ____ )
   ) (   | (    )|| (   ) || (    \/|  \  / /| (    \/| (    )|
   | |   | (____)|| (___) || |      |  (_/ / | (__    | (____)|
   | |   |     __)|  ___  || |      |   _ (  |  __)   |     __)
   | |   | (\ (   | (   ) || |      |  ( \ \ | (      | (\ (   
   | |   | ) \ \__| )   ( || (____/\|  /  \ \| (____/\| ) \ \__
   )_(   |/   \__/|/     \|(_______/|_/    \/(_______/|/   \__/
      """, fg='cyan')

        print("""\n\n\nThis is a open-source software which is free to distribute and can be edited by 
anyone. Link to the source github in Readme file. Feel free to conribute.

Author: Abhay Salvi
Version: 1.0.0
      """)

    def Warnings(self, cmd=""):
        if cmd == "":
            click.secho(
                "Error (01): You have a Syntax error in your query. Check -h command for help", fg='red')
        elif cmd == self.NO_DATABASE_ERROR:
            click.secho(
                "Error (02): Can't perform operation because No such Database Exists", fg='red')
        elif cmd == self.NO_TABLE_TO_DROP:
            click.secho(
                "Error (03): Can't Drop data because No Database Exists", fg='red')
        elif cmd == self.WRONG_EMAIL:
            click.secho(
                "Error (04): Wrong email entered", fg='red')

    def Success(self):
        click.secho("Query OK, Exit Code: 0", fg='green')

```

-----
Now what the `main.py` does is to scrape the data on the the update command. To do that, here's another file named `scrape.py` It hides the ChromeWebDriver and scrapes behind the scenes. Here's what it looks like:
```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

import errno
import os
import platform
import subprocess
import warnings

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome import service, webdriver, remote_connection

# my own module...
from store_data import Store

# Hiding Chrome browser to avoid popping it up


class HiddenChromeService(service.Service):
    def start(self):
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())

            if platform.system() == 'Windows':
                info = subprocess.STARTUPINFO()
                info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = 0  # SW_HIDE (6 == SW_MINIMIZE)
            else:
                info = None

            self.process = subprocess.Popen(
                cmd, env=self.env,
                close_fds=platform.system() != 'Windows',
                startupinfo=info,
                stdout=self.log_file,
                stderr=self.log_file,
                stdin=subprocess.PIPE)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "Executable %s must be in path. %s\n%s" % (
                    os.path.basename(self.path), self.start_error_message,
                    str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can't connect to the Service %s" % (
                    self.path,))


class HiddenChromeWebDriver(webdriver.WebDriver):
    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):
        if chrome_options:
            warnings.warn('use options instead of chrome_options',
                          DeprecationWarning, stacklevel=2)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = self.create_options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = HiddenChromeService(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=remote_connection.ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url,
                    keep_alive=keep_alive),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
options = Options()
options.add_argument("--headless")
options.add_argument(f'user-agent={user_agent}')
csv_file_location_c = r"C:\Users\intel\Desktop\countries.csv"
csv_file_location_w = r"C:\Users\intel\Desktop\world.csv"
csv_file_location_i = r"C:\Users\intel\Desktop\india.csv"

s_data = Store()


def scrape_data_from_countries():
    time.sleep(1)
    driver = HiddenChromeWebDriver(
        executable_path=r"C:\Users\intel\Downloads\setups\chromedriver.exe", options=options)
    driver.get('https://www.worldometers.info/coronavirus/#countries')

    country_name = []
    total_cases = []
    deaths = []
    recovered = []

    for z in range(5, 225):
        try:
            element = driver.find_element_by_xpath(
                """/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[""" + str(z) + """]/td[2]/a""")
            country_name.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[""" + str(z) + """]/td[3]""")
            total_cases.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[""" + str(z) + """]/td[5]""")
            deaths.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[""" + str(z) + """]/td[7]""")
            recovered.append(element)
        except:
            pass

    country_name_text = [ele.text.strip() for ele in country_name]
    total_cases_text = [ele.text.strip() for ele in total_cases]
    deaths_text = [ele.text.strip() for ele in deaths]
    recovered_text = [ele.text.strip() for ele in recovered]

    df = pd.DataFrame(
        {
            "COUNTRY_NAMES": country_name_text,
            "TOTAL_CASES": total_cases_text,
            "CONFIRMED_CASES": deaths_text,
            "RECOVERED_CASES": recovered_text,
        }
    )
    driver.close()

    # print(df)
    s_data.store_to_csv(loc=csv_file_location_c, df=df)
    s_data.store_to_sql(df=df, name="countries")


def scrape_data_from_world():
    driver = HiddenChromeWebDriver(
        executable_path=r"C:\Users\intel\Downloads\setups\chromedriver.exe", options=options)
    driver.get('https://www.worldometers.info/coronavirus/')

    total_cases = []
    deaths = []
    recovered = []

    try:
        element = driver.find_element_by_xpath(
            """/html/body/div[3]/div[2]/div[1]/div/div[4]/div/span""")
        total_cases.append(element)
        element = driver.find_element_by_xpath(
            """/html/body/div[3]/div[2]/div[1]/div/div[6]/div/span""")
        deaths.append(element)
        element = driver.find_element_by_xpath(
            """/html/body/div[3]/div[2]/div[1]/div/div[7]/div/span""")
        recovered.append(element)
    except:
        pass

    total_cases_text = [ele.text.strip() for ele in total_cases]
    deaths_text = [ele.text.strip() for ele in deaths]
    recovered_text = [ele.text.strip() for ele in recovered]

    df = pd.DataFrame(
        {
            "TOTAL_CASES": total_cases_text,
            "CONFIRMED_CASES": deaths_text,
            "RECOVERED_CASES": recovered_text,
        }
    )
    driver.close()

    # print(df)
    s_data.store_to_csv(loc=csv_file_location_w, df=df)
    s_data.store_to_sql(df=df, name="world")


def scrape_data_from_india():
    driver = HiddenChromeWebDriver(
        executable_path=r"C:\Users\intel\Downloads\setups\chromedriver.exe", options=options)
    driver.get('https://www.covid19india.org/')

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'DIV.state-name.fadeInUp'))
    )
    state = []
    confirmed = []
    active = []
    recovered = []

    try:
        for z in range(2, 37):
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[5]/div/div[""" + str(z) + """]/div[1]/div""")
            state.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[5]/div/div[""" + str(z) + """]/div[2]/div[2]""")
            confirmed.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[5]/div/div[""" + str(z) + """]/div[3]/div""")
            active.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[5]/div/div[""" + str(z) + """]/div[4]/div[2]""")
            recovered.append(element)
    except:
        pass

    state_text = [ele.text.strip() for ele in state]
    confirmed_text = [ele.text.strip() for ele in confirmed]
    active_text = [ele.text.strip() for ele in active]
    recovered_text = [ele.text.strip() for ele in recovered]

    df = pd.DataFrame(
        {
            "STATE_NAME": state_text,
            "CONFIRMED_CASES": confirmed_text,
            "ACTIVE_CASES": active_text,
            "RECOVERED_CASES": recovered_text,
        }
    )

    driver.close()

    # print(df)
    s_data.store_to_csv(loc=csv_file_location_i, df=df)
    s_data.store_to_sql(df=df)

```
----
Now we've sucessfully scraped the data, but were to store it?
Well, here's another module that I created named `store_data.py`:
```
from sqlalchemy import create_engine

class Store():
    def store_to_csv(self, loc, df):
        df.to_csv(loc, mode='a', encoding='utf-8')

    def store_to_sql(self, df, name="india"):
        engine = create_engine(f"mysql://abhay:1234@localhost/covid_db")
        con = engine.connect()
        df.to_sql(con=con, name=name,
                  if_exists='replace')

```
Now it stores data to **both** csv as well as SQL. But it can send this to your email too! And to do that, here's an another module named:
```
import smtplib
from intro import Intro

Intr = Intro()


def send_mail(df, mail):
    port = 587  # For starttls

    # Create a secure SSL context
    s = smtplib.SMTP('smtp.gmail.com', port)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("email", "pass")

    # message to be sent
    message = df

    try:
        # sending the mail
        s.sendmail("email",
                   mail, str(message))
    except:
        Intr.Warnings(cmd=Intr.WRONG_EMAIL)
    finally:
        s.quit()

```
Here's how it looks:
![excel](https://i.postimg.cc/DfQ7gNBN/exl.png)
---
Now we've transfered the data to Email, but to show that data visually in both text and graph, we need another module which I created specefically for both the purpose named `get_sql_data.py`:
```
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
        fig.suptitle('India data and countries data horizontally stacked')
        ax1.plot(query, query2)
        ax2.plot(query3, query4)

        ax1.ticklabel_format(style='plain', axis='x')
        ax2.ticklabel_format(style='plain', axis='x')
        plt.show()

```
Here's how it looks:
![cmd](https://i.postimg.cc/3JynhsVS/Capture-2-PNG.png)
![cmd](https://i.postimg.cc/HsQ3jwWX/Figure-1.png)
