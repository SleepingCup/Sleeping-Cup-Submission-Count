import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys
def generate_html(submits):
    with open('index.html', 'wb') as file:
        file.write(b"<!DOCTYPE html>\n")
        file.write(b"<html lang=\"en\">\n")
        file.write(b"    <head>\n")
        file.write(b"        <meta charset=\"UTF-8\">\n")
        file.write(b"        <meta name=\"viewport\" content=\"width=device-width initial-scale=1.0\">\n")
        file.write(b"        <title>Sleeping Cup Submission Count</title>\n")
        file.write(b"        <style>\n")
        file.write(b"            html, body\n")
        file.write(b"            {\n")
        file.write(b"                height: 100%;\n")
        file.write(b"                margin: 0;\n")
        file.write(b"            }\n")
        file.write(b"            .upper_center\n")
        file.write(b"            {\n")
        file.write(b"                position: absolute;\n")
        file.write(b"                top: 50%;\n")
        file.write(b"                left: 50%;\n")
        file.write(b"                transform: translate(-50%, -50%);\n")
        file.write(b"                margin-top: -225px;\n")
        file.write(b"                margin-left: -5px;\n")
        file.write(b"            }\n")
        file.write(b"            .mid_center\n")
        file.write(b"            {\n")
        file.write(b"                position: absolute;\n")
        file.write(b"                top: 50%;\n")
        file.write(b"                left: 50%;\n")
        file.write(b"                transform: translate(-50%, -50%);\n")
        file.write(b"                margin-top: 50px;\n")
        file.write(b"                margin-left: 25px;\n")
        file.write(b"            }\n")
        file.write(b"            .lower_center\n")
        file.write(b"            {\n")
        file.write(b"                position: absolute;\n")
        file.write(b"                top: 50%;\n")
        file.write(b"                left: 50%;\n")
        file.write(b"                transform: translate(-50%, -50%);\n")
        file.write(b"                margin-top: 250px;\n")
        file.write(b"                margin-left: -5px;\n")
        file.write(b"            }\n")
        file.write(b"        </style>\n")
        file.write(b"    </head>\n")
        file.write(b"    <body style=\"background-color: black;\">\n")
        file.write(b"        <center>\n")
        file.write(b"            <h1 style=\"white-space: nowrap; color: #0f0; font-family: Segoe UI; font-size: 150px;\" class=\"upper_center\">Submission Count</h1>\n")
        file.write(bytes("            <h1 style=\"white-space: nowrap; color: #fff; font-family: Consolas; font-size: 300px; letter-spacing: 50px;\" class=\"mid_center\"><span style=\"color: #777;\">00</span>{}</h1>\n".format(submits), encoding="utf-8"))
        file.write(bytes("<h1 style=\"white-space: nowrap; color: #fff; font-family: Segoe UI; font-size: 50px\" class=\"lower_center\"><span style=\"color: #ff0;\">{:.3f} </span><span style=\"color: #0ff;\">submissions per day on average</span></h1>\n".format(submits / (datetime.now() - datetime(2024, 6, 27)).days), encoding="utf-8"))
        file.write(b"        </center>\n")
        file.write(b"    </body>\n")
        file.write(b"</html>\n")
def extract_numbers(text):
    pattern = r'(\d+)\s*/\s*(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        return None, None
login_url = 'https://www.sleepingcup.com/login?uname=035966_L3&password={}&tfa=&authnChallenge='.format(sys.argv[1])
session = requests.Session()
response = session.post(login_url)
if response.ok == False:
    print('Login failed!')
    sys.exit(1)
url = 'http://8.136.99.126/p?page='
page = 0
count = 0
submits = 0
continous = True
while continous:
    continous = False
    page = page + 1
    content = session.get(url + str(page))
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        text = soup.get_text()
        lines = text.splitlines()
        for line in lines:
            num1, num2 = extract_numbers(line)
            if num1 != None:
                continous = True
                count = count + 1
                submits = submits + num2
    else:
        print('Crawling Failed!')
        sys.exit(1)
print('Crawled!')
print('Problem Count:', count)
print('Submission Count:', submits)
generate_html(submits)

