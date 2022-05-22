import requests
from bs4 import BeautifulSoup
import smtplib
import time

def send_email(URL,EMAIL,title,flt_price):
    server =  smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('roy.coder.00@gmail.com','xdlsrxrodhhbytsu')

    subject = "PRICE FALLEN!"
    body = f"{title} \n HURRY UP! NOW THE PRICE IS {flt_price} \n check the link below:- \n {URL}"

    msg = f" Subject: {subject} \n\n {body}"
    
    server.sendmail(
        'roy.coder.00@gmail.com',
        EMAIL,
        msg.encode('utf-8')
    )
    print("Email Send")

    server.quit()

def check_price_amazon(URL,EMAIL,PRICE):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text().strip()
    str_price = soup.find(class_="a-price-whole").get_text().strip()

    #print(title)
    new_str_price = ""

    for s in str_price:
        if s.isdigit():
            new_str_price = s + new_str_price

    flt_price = float(new_str_price[::-1])

    #print(flt_price)

    if flt_price < PRICE:
        send_email(URL,EMAIL,title,flt_price)
        return 0

def check_price_flipkart(URL,EMAIL,PRICE):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(class_="B_NuCI").get_text().strip()
    str_price = soup.find(class_="_30jeq3 _16Jk6d").get_text().strip()

    #print(title)
    new_str_price = ""

    for s in str_price:
        if s.isdigit():
            new_str_price = s + new_str_price

    flt_price = float(new_str_price[::-1])

    #print(flt_price)

    if flt_price < PRICE:
        send_email(URL,EMAIL,title,flt_price)  
        return 0      

def take_input():

    URL = str(input("Give the url of the product: "))
    EMAIL =str(input("Give the your email: "))
    PRICE = int(input("Price below which you want alert: "))
    A_or_F = int(input("FOR AMAZON enter 1, FOR FLIPKART enter 0: "))
    run = 1
    while run:
        if A_or_F==1:
            run=check_price_amazon(URL,EMAIL,PRICE)
        elif A_or_F==0:
            run=check_price_flipkart(URL,EMAIL,PRICE)
        else:
            A_or_F = int(input("FOR AMAZON enter 1, FOR FLIPKART enter 0"))
        time.sleep(60)

take_input()