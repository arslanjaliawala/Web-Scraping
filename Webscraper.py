import requests
from bs4 import BeautifulSoup
import lxml
import xlwt

root = 'https://martslu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Martslu-DataScraping')
count = 0
pricelist = [0 for i in range(2)]

r = requests.get(root,headers = headers)
soup = BeautifulSoup(r.content, 'lxml')
a = soup.find_all(class_= "box-text box-text-products")
sheet1.write(count,0,'Product Category')
sheet1.write(count,1,'Product Title')
sheet1.write(count,2,'Product Price')
sheet1.write(count,3,"Discounted Price")
count = 0
for entry in a:
    count = count +1
    category = entry.find(class_ = "category uppercase is-smaller no-text-overflow product-cat op-7").get_text()
    title = entry.find(class_= "name product-title").get_text()
    price = entry.find(class_="price").get_text()
    sheet1.write(count, 0, category)
    sheet1.write(count, 1, title)
    pricelist = price.split()
    counter = 2
    for price in pricelist:
        sheet1.write(count, counter, price)
        counter += 1
    if (counter == 3):
        sheet1.write(count,counter,price)

wb.save(' filescraping.xls')
print("Writing Successful!!!")