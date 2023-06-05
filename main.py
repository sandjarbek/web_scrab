import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3

connection = sqlite3.connect("data.db")


URL="https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value= extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    password = os.getenv("PASSWORD")
    # user = "securesally@gmail.com"
    user = "sanjarbek.soatov1989@gmail.com"
    receiver = "sanjarbek.89.ss@gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(user, password)
        server.sendmail(user, receiver, message)
    print("Email was send!")

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor= connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events Where band=? and city=? and date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows



if __name__=="__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)



        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey new event was found")

        time.sleep(2 )


# INSERT INTO events VALUES('Monkeys', 'Monkey City', '2088.10.24')
# SELECT * from events WHERE date='2088.10.14'
