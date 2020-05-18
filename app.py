from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import bs4
from bs4 import BeautifulSoup

app= Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')



@app.route('/review',methods=['POST'])
@cross_origin()
def index():
    if request.method=="POST":
        try:
            search_string = request.form['content'].replace(" ", "")
            base_url = 'https://www.flipkart.com'
            base_search_url = 'https://www.flipkart.com/search?q='
            search_url = base_search_url + search_string
        except:
            print('error')

        source = requests.get(search_url).content
        soup = BeautifulSoup(source, 'lxml')
        classes = ['Zhf2z-', '_31qSD5', '_3dqZjq', '_2cLu-l']
        for x in classes:
            if len(soup.find_all('a', class_=x)) != 0:
                urls = soup.find_all('a', class_=x)
            else:
                continue

        try:
            product_url = []
            for url in urls:
                product_url.append(base_url + url.get('href'))
        except:
            pass

        try:
            product_review_url = []
            for x in range(len(product_url)):
                source = requests.get(product_url[x]).content
                soup = BeautifulSoup(source, 'lxml')
                product_review_url.append(base_url + soup.find('div', class_='swINJg _3nrCtb').parent.get('href'))
        except:
            pass

        Reviews = []
        for x in range(len(product_review_url)):
            source = requests.get(product_review_url[x]).content
            soup = BeautifulSoup(source, 'lxml')
            reviews = soup.find_all('div', class_='_1PBCrt')
            for review in reviews:
                try:
                    name = review.find('p', class_='_3LYOAd _3sxSiS').text
                    # Name.append(name)
                except:
                    name='no name'

                try:
                    rating = review.find('div', class_='hGSR34 E_uFuv').text
                    # Rating.append(rating)
                except:
                    rating='no rating'
                try:
                    comment = review.find('div', class_='qwjRop').div.div.text
                    # Review.append(comment)
                except:
                    comment='no comment'
                try:
                    summary = review.find('p', class_='_2xg6Ul').text
                    # Summary.append(summary)
                except:
                    summary='no summary'
                review_dict = {'Name': name, 'Rating': rating, 'Comment': comment, 'Summary': summary}
                Reviews.append(review_dict)
                if len(Reviews)>10:
                    break
        return render_template("results.html", Reviews=Reviews)
    else:
        render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)



