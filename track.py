import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import sys
def generate_html(submits):
    with open('index.html', 'wb') as file:
        file.write(b"<!DOCTYPE html>")
        file.write(b"<html lang=\"en\">")
        file.write(b"    <head>")
        file.write(b"        <meta charset=\"UTF-8\">")
        file.write(b"        <meta name=\"viewport\" content=\"width=device-width initial-scale=1.0\">")
        file.write(b"        <title>Sleeping Cup Submission Count</title>")
        file.write(b"        <style>")
        file.write(b"            html, body")
        file.write(b"            {")
        file.write(b"                height: 100%;")
        file.write(b"                margin: 0;")
        file.write(b"            }")
        file.write(b"            .upper_center")
        file.write(b"            {")
        file.write(b"                position: absolute;")
        file.write(b"                top: 50%;")
        file.write(b"                left: 50%;")
        file.write(b"                transform: translate(-50%, -50%);")
        file.write(b"                margin-top: -200px;")
        file.write(b"                margin-left: -25px;")
        file.write(b"            }")
        file.write(b"            .lower_center")
        file.write(b"            {")
        file.write(b"                position: absolute;")
        file.write(b"                top: 50%;")
        file.write(b"                left: 50%;")
        file.write(b"                transform: translate(-50%, -50%);")
        file.write(b"                margin-top: 100px;")
        file.write(b"            }")
        file.write(b"        </style>")
        file.write(b"    </head>")
        file.write(b"    <body style=\"background-color: black;\">")
        file.write(b"        <center>")
        file.write(b"            <h1 style=\"white-space: nowrap; color: #0f0; font-family: Segoe UI; font-size: 150px;\" class=\"upper_center\">Submission Count</h1>")
        file.write(bytes("            <h1 style=\"white-space: nowrap; color: #fff; font-family: Consolas; font-size: 300px; letter-spacing: 50px;\" class=\"lower_center\"><span style=\"color: #777;\">00</span>{}</h1>".format(submits), encoding="utf-8"))
        file.write(b"        </center>")
        file.write(b"    </body>")
        file.write(b"</html>")
def extract_numbers(text):
    pattern = r'(\d+)\s*/\s*(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        return None, None
login_url = 'http://8.136.99.126/login'
username = '035966_L3'
password = sys.argv[1]
session = requests.Session()
payload = {'uname': username, 'password': password, 'rememberme': True}
response = session.post(login_url, data = payload)
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
