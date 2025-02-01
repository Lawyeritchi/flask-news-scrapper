from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def class_filter(media_name):
    class_name = ""
    element_name = ""
    
    if media_name == "cnn":
        class_name = "text-2xl inline group-hover:text-cnn_red"
        element_name = "h1"
    elif media_name == "detik":
        class_name = "media__title"
        element_name = "h3"
    elif media_name == "okezone":
        class_name = "jdl-right-headline"
        element_name = "a"
    elif media_name == "kompas":
        class_name = "wSpec-title"
        element_name = "h4"
    elif media_name == "tempo":
        class_name = "lg:text-[22px] lg:font-medium text-neutral-1200 text-base leading-[122%]"
        element_name = "p"
    elif media_name == "liputan6":
        class_name = "headline--main__title"
        element_name = "h2"
        
    return [class_name, element_name]

def news_scrap(name, url):
    detector = class_filter(name)
    class_name, element_name = detector[0], detector[1]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    element = BeautifulSoup(response.content, 'html.parser')
    
    headline = element.find(element_name, class_=class_name)
    
    if headline:
        return headline.text.strip()
    else:
        return f"Tidak dapat menemukan headline untuk {name}"
    
# def product_scrap(url, container_class, title_class, price_class, image_class):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
    
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     products = []
#     containers = soup.find_all('div', class_=container_class)
    
#     for container in containers[:5]:
#         title = container.find(class_=title_class)
#         price = container.find(class_=price_class)
#         image = container.find("img", class_=image_class)
        
#         if title and price and image:
#             products.append({
#                 "title": title.text.strip(),
#                 "price": price.text.strip(),
#                 "image": image["src"]
#             }) 
        
#     return products

@app.route('/')
def main():
    cnn = news_scrap("cnn", "https://www.cnnindonesia.com")
    detik = news_scrap("detik", "https://www.detik.com")
    okezone = news_scrap("okezone", "https://www.okezone.com")
    kompas = news_scrap("kompas", "https://www.kompas.com")
    tempo = news_scrap("tempo", "https://www.tempo.co")
    liputan6 = news_scrap("liputan6", "https://www.liputan6.com")
    
    return render_template('index.html', news1=cnn, news2=detik, news3=okezone, news4=kompas, news5=tempo, news6=liputan6)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)