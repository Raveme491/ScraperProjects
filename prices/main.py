import requests
from bs4 import BeautifulSoup
import smtplib
import dados

books = {
    'Algorimos':'https://www.amazon.com.br/Entendendo-Algoritmos-Ilustrado-Programadores-Curiosos/dp/8575225634/?_encoding=UTF8&pd_rd_w=HYvtK&content-id=amzn1.sym.7e02476f-6b1f-478b-bd90-e9f82ef6fc53&pf_rd_p=7e02476f-6b1f-478b-bd90-e9f82ef6fc53&pf_rd_r=CNTF891N636HSJTN0GKQ&pd_rd_wg=dugyG&pd_rd_r=c2b8e4f1-fac3-4865-8563-c8f8cc542667&ref_=pd_gw_ci_mcx_mr_hp_atf_m',
    'Devoradores de estrelas':'https://www.amazon.com.br/Devoradores-estrelas-Andy-Weir-ebook/dp/B094RCZF5V/ref=sr_1_1?crid=2WIKC76TX0KX8&keywords=devoradores+de+estrelas&qid=1675207425&s=digital-text&sprefix=devorad%2Cdigital-text%2C178&sr=1-1',
    'Assassinato no expresso do oriente':'https://www.amazon.com.br/Assassinato-no-Expresso-do-Oriente/dp/8595086788/ref=sr_1_5?crid=QKSIKJ54RMCW&keywords=agatha+christie&qid=1675208764&sprefix=%2Caps%2C710&sr=8-5'
}

headers = {
    "Accept-Language":"pt-BR,pt;q=0.5",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

prices = []
for book in books.values():
    html = requests.get(book, headers=headers).text

    soup = BeautifulSoup(html,'lxml')

    try:
        result = soup.find(name="span", id="kindle-price").getText()
    except AttributeError:
        result = soup.find(name="span", id="price").getText()
    prices.append(float(result[3:].replace(",",".")))


with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=dados.email, password=dados.password)
    connection.sendmail(
        from_addr=dados.email,
        to_addrs=dados.email_para,
        msg = f"Subject:PRICES DO DIA \n\n \
            {list(books.keys())[0]}: R${prices[0]}\n \
            {list(books.keys())[1]}: R${prices[1]}\n \
            {list(books.keys())[2]}: R${prices[2]}"
    )