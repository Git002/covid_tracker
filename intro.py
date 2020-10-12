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
