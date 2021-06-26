import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import  decimal

def get_links(page):
    response = requests.get(f'https://tribesigns.com/collections/clearance?page={page}')
    soup = BeautifulSoup(response.content, 'html.parser')
    main_div = soup.find('ul' , attrs={"class": "products-per-row-4"})
    print(f'Get Page {page}')
    f = open("links.txt", "a")
    for link in main_div.find_all('a' , attrs={"class": "productitem--link"}):

        f.write('https://tribesigns.com' + link.get('href') + '\n')
    f.close()

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1' ,attrs={"class": "product-title"}).text.lstrip().rstrip()
    Category = soup.find('nav', attrs={"class": "breadcrumbs-container"}).find_all('a')[1].text
    path = f'products/{Category}/{title}'
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True)
        price = soup.find('div' ,attrs={"class": "price--main"}).find('span' ,attrs={"class": "money"}).text.lstrip().rstrip()
        description = soup.find('div' ,attrs={"class": "product-description rte"}).text.lstrip().rstrip().replace(' ' , '')
        if re.search("size:.\d" , description):
            size = re.findall("size:.*\"", description)[0]
            size_in_cm_raw = re.findall(r"[-+]?\d*\.\d+|\d+", size)
            size_in_cm = []
            for size_float in size_in_cm_raw:
                final_val7 = decimal.Decimal(float(size_float) * 2.5).quantize(decimal.Decimal('0'),rounding=decimal.ROUND_UP)
                size_in_cm.append(str(final_val7) + ' cm')
        images_div = soup.find('div' , attrs={"class": "gallery-navigation--scroller"})
        counter = 1
        for image in images_div.find_all('img' , attrs={"class" : "product-gallery--media-thumbnail-img"}):
            image_url = image.get('src').replace('75x75' , '1266x1266').replace('//cdn' , 'https://cdn')
            image_file = requests.get(image_url)
            file = open(f"{path}/{counter}.png", "wb")
            file.write(image_file.content)
            file.close()
            counter += 1
        file = open(f"{path}/info.txt", "a")
        file.write(f'Product Title : {title} \n \n \n \n' )
        file.write(f'Product description : {description} \n \n \n \n' )
        file.write(f'Product price : {price} \n \n \n \n' )
        file.write(f'Product Category : {Category} \n \n \n \n' )
        if re.search("size:.\d", description):
            file.write(f'Product Size : {size} \n \n \n \n' )
            file.write(f'Product Size in CM : {size_in_cm} \n \n \n \n' )
        file.write(f'Product Link : {url} \n \n \n \n' )
        file.close()
