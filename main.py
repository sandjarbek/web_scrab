import requests
import selectorlib
import smtplib, ssl
import os
import time


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
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()




if __name__=="__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        content = read(extracted)

        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey new event was found")

        time.sleep(2 )
