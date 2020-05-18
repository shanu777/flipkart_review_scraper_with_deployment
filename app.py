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

        product_url = []
        for url in urls:
            product_url.append(base_url + url.get('href'))

        product_review_url = []
        try:
            for x in range(len(product_url)):
                source = requests.get(product_url[x]).content
                soup = BeautifulSoup(source, 'lxml')
                list = ['swINJg _3nrCtb', 'swINJg _3cycCZ']
                for x in list:
                    if (soup.find('div', class_=x)) is not None:
                        product_review_url.append(base_url + soup.find('div', class_=x).parent.get('href'))
                    else:
                        continue
        except:
            print('error1')

        Reviews = []
        for x in range(len(product_review_url)):
            source = requests.get(product_review_url[x]).content
            soup = BeautifulSoup(source, 'lxml')
            reviews = soup.find_all('div', class_='_1PBCrt')
            for review in reviews:

                try:
                    names = ['_3LYOAd _3sxSiS _2675cp', '_3LYOAd _3sxSiS']
                    name = 'not available'
                    for x in names:
                        if (review.find('p', class_=x)) is not None:
                            name = review.find('p', class_=x).text
                        else:
                            continue
                    # Name.append(name)
                except:
                    name = 'not available'

                try:
                    ratings = ['hGSR34 E_uFuv', 'hGSR34 E_uFuv _3-6Xp-']
                    rating = 'not available'
                    for x in ratings:
                        if (review.find('div', class_=x)) is not None:
                            rating = review.find('div', class_=x).text
                        else:
                            continue
                    # Rating.append(rating)
                except:
                    rating = 'not available'

                try:
                    comments = ['_2t8wE0', 'qwjRop']
                    for x in comments:
                        if (review.find('div', class_=comments[0])) is not None:
                            comment = review.find('div', class_=comments[0]).text
                        if (review.find('div', class_=comments[1])) is not None:
                            comment = review.find('div', class_=comments[1]).text
                        else:
                            comment = 'not available'
                        # Review.append(comment)
                except:
                    comment = 'not available'

                try:
                    summar = ['_2t8wE0', '_2xg6Ul']
                    summary = 'not available'
                    for x in summar:
                        if review.find('p', class_=x) is not None:
                            summary = review.find('p', class_=x).text
                        else:
                            continue

                    # Summary.append(summary)
                except:
                    summary = 'not available'

                try:
                    review_dict = {'Name': name, 'Rating': rating, 'Comment': comment, 'Summary': summary}
                except:
                    print('error dict')
                try:
                    Reviews.append(review_dict)
                except:
                    print('error list')

            if (len(Reviews)) > 10:
                break

        return render_template("results.html", Reviews=Reviews)
    else:
        render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)



