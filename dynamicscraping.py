import requests
from bs4 import BeautifulSoup
import lxml
import xlwt
logindata = {
    'request_uri': 'Lw',
    'frm_username': 'ravishmart',
    'frm_password': 'UmerFarooq2021@',
    'frm_action': 'Login'
}
wb = xlwt.Workbook()
sheet1 = wb.add_sheet('HITTrade Scraping')
sheet1.write(0,0,"Product Category")
sheet1.write(0,1,"Product Title")
sheet1.write(0,2,"Product Price")
sheet1.write(0,3, "Product Barcode")
count = 1
loginurl='https://www.htitrade.co.uk/trade/login.php'
with requests.Session() as s:
    url = "https://www.htitrade.co.uk/shop_by_product"
    s.post(loginurl, data=logindata)
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    allcategories = soup.find_all(class_="is3-productgroup-thumbnail-title")
    for category in allcategories:
        updtdurl = category.get('href')
        r2 = s.get(updtdurl)
        psoup = BeautifulSoup(r2.content, 'lxml')
        allsubcategories = psoup.find_all(class_="is3-productgroup-thumbnail-title")
        for subcategory in allsubcategories:
            spcfcurl = subcategory.get('href')
            r3 = s.get(spcfcurl)
            s_soup = BeautifulSoup(r3.content, 'lxml')
            titles = s_soup.find_all(class_ ="is3-product-thumbnail-img product-link")
            for title in titles:
                prdcturl = title.get('href')
                r4 = s.get(prdcturl)
                prdct_soup = BeautifulSoup(r4.content, 'html.parser')
                rows = prdct_soup.find('table', class_='table')
                sheet1.write(count,0,category.get_text())
                sheet1.write(count,1,prdct_soup.find(class_="is3-main-title").get_text())
                sheet1.write(count,2,prdct_soup.find(class_="pull-left price-value").get_text())
                sheet1.write(count,3,rows.find_all('td')[1].get_text())
                count = count + 1
                print(category.get_text())
                print(prdct_soup.find(class_="is3-main-title").get_text())
                print(prdct_soup.find(class_="pull-left price-value").get_text())
                print(rows.find_all('td')[1].get_text())

wb.save('dynamicscraping.xls')
print("Scrape Successful")