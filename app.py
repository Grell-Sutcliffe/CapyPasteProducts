
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, request, flash
import json
from parsers.vasko import parse_by_name_vasko
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

# data_history = [{"name": "Товар1", "price": 100, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"},
# {"name": "Товар2", "price": 200, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"},
# {"name": "Товар1", "price": 120, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"},
# {"name": "проверка кассы", "price": 120, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"}]
data_path = 'parsed_data/technodeus.json'

with open(data_path, 'r') as file:
    data_history = json.load(file)


@app.route("/search/<req>", methods=["GET", "POST"])
def search(req):
    search_res = []
    try:
        logging.debug(request.form['product_name'], 1111111111,
                      request.method, request.form['product_name'] == '')
    except:
        logging.debug("mda")
    # получаем текст введенный пользователем в поле
    if request.method == "POST" and request.form['product_name'] != '':
        return redirect(url_for('search', req=request.form['product_name']))

    # if req: # тесты со словарем
    #     search_request = req
    #     search_res = [item for item in data if item["name"] in search_request]

    logging.debug(req)
    search_res = None
    # проверяет что ввод не пустой и не рандомно вылезающий везде ввод favion
    if req != '' and req != 'favicon.ico':
        search_request = req
        search_res = parse_by_name_vasko(req)  # парсит сайт в реальном времени
        search_added_res  = [
            item for item in data_history if search_request in item['name']]
        search_res = search_res + search_added_res
        search_res = sorted(search_res, key=lambda x: x["price"])
        logging.debug('app', search_res)
        if 'userLogged' in session:
            session['data_history'] = search_res[:5] if len(search_res) > 6 else search_res
            logging.debug("AAA")
    # перенаправление на страницу с названием товара в пути
        return render_template("search.html", products=search_res)


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
