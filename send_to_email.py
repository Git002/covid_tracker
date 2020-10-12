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
    s.login("andrew.whiteman77@gmail.com", "avinashy77")

    # message to be sent
    message = df

    try:
        # sending the mail
        s.sendmail("andrew.whiteman77@gmail.com",
                   mail, str(message))
    except:
        Intr.Warnings(cmd=Intr.WRONG_EMAIL)
    finally:
        s.quit()
