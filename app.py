from flask import Flask, render_template, request, jsonify, session, redirect, url_for, request, flash
import json
from parsers.vasko import parse_by_name_vasko
import logging
from collections import Counter
import re

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

data_history = [{'name': 'iphone 15',
  'price': 100,
  'href': 'https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/',
  'pic': 'https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z',
  'set_words': {'15', 'iphone'}},
 {'name': 'чехол iphone 15',
  'price': 200,
  'href': 'https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/',
  'pic': 'https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z',
  'set_words': {'15', 'iphone', 'чехол'}},
 {'name': 'чехол iphone 14',
  'price': 120,
  'href': 'https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/',
  'pic': 'https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z',
  'set_words': {'14', 'iphone', 'чехол'}},
 {'name': 'iphone 14',
  'price': 120,
  'href': 'https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/',
  'pic': 'https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z',
  'set_words': {'14', 'iphone'}}]
data_path = 'parsed_data/technodeus.json'

#with open(data_path, 'r') as file:
#    data_history = json.load(file)

@app.route("/search/<req>", methods=["GET", "POST"])
def search(req):
    search_res = []
    filters = {"include": [], "exclude": []}

    custom_filters = request.form.getlist("custom_filters")  # Получаем пользовательские фильтры
    if request.method == "POST" and 'product_name' in request.form:
        return redirect(url_for('search', req=request.form['product_name']))

    if req != '' and req != 'favicon.ico':
        search_request = req.lower()
        words_set = set(search_request.split())
        search_res = []
        #search_res = parse_by_name_vasko(req)  # Парсит сайт в реальном времени
        #search_added_res = [
        #    item for item in data_history if search_request in item['name'].lower()
        #]
        search_added_res = [
                item for item in data_history if words_set & item["set_words"]
             ]

        search_res = search_res + search_added_res
        search_res = sorted(search_res, key=lambda x: x["price"])

    word_counts = Counter(
        re.findall(r'\b\w+\b', " ".join([item["name"].lower() for item in search_res]))
    )
    top_words = [word for word, _ in word_counts.most_common(10)]

    if request.method == "POST":
        if "add_custom_filter" in request.form and request.form.get("custom_filter"):
            custom_word = request.form.get("custom_filter").strip().lower()
            if custom_word not in top_words and custom_word not in custom_filters:
                custom_filters.append(custom_word)

        all_words = top_words + custom_filters
        for word in all_words:
            action = request.form.get(word)
            if action == "include" and word not in filters["include"]:
                filters["include"].append(word)
            elif action == "exclude" and word not in filters["exclude"]:
                filters["exclude"].append(word)

        search_res = [
            item for item in search_res
            if all(inc in item["name"].lower() for inc in filters["include"]) and
               not any(exc in item["name"].lower() for exc in filters["exclude"])
        ]
        print(req,request.form['product_name'] if 'product_name' in request.form else 1)
    return render_template(
        "search.html",
        products=search_res,
        top_words=top_words,
        filters=filters,
        custom_filters=custom_filters
    )


@app.route('/favicon.ico')  # костыль!
def favicon():
    return '', 204


@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    logging.debug("mda")
    if request.method == "POST" and request.form['product_name'] != '':
        return redirect(url_for('search', req=request.form['product_name']))
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    #
    elif request.method == "POST" and request.form['username'] == "yadayn" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    elif request.method == "POST" and len(request.form['username']) > 2:
        flash('пароль неверен')
    return render_template("login.html")


@app.route("/unaftorize")
def unaftorize():
    return render_template("unaftorize.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    logging.debug(session['userLogged'], username)
    if 'userLogged' not in session or session['userLogged'] != username:
        return redirect(url_for('unaftorize'))  # мб через аборт сделать
    if 'data_history' not in session:
        session['data_history'] = []
    # СДЕЛАТЬ ИСТОРИЮ ПРИВЯЗАННОЙ К ПОЛЬЗОВАТЕЛЮ
    return render_template("user.html", history=session['data_history'])


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
