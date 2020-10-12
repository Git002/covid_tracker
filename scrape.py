from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from store_data import Store

import errno
import os
import platform
import subprocess
import warnings

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome import service, webdriver, remote_connection


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
                """/html/body/div/div/div[3]/div[1]/div[4]/div/div[""" + str(z) + """]/div[1]/div""")
            state.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[4]/div/div[""" + str(z) + """]/div[2]/div[2]""")
            confirmed.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[4]/div/div[""" + str(z) + """]/div[3]/div""")
            active.append(element)
            element = driver.find_element_by_xpath(
                """/html/body/div/div/div[3]/div[1]/div[4]/div/div[""" + str(z) + """]/div[4]/div[2]""")
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
