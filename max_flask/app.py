from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json

app = Flask(__name__)

data = [{"name": "Товар1", "price": 100, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"},
    {"name": "Товар2", "price": 200, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"},
    {"name": "Товар1", "price": 120, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"},
    {"name": "проверка кассы", "price": 120, "href" :  "https://5ka.ru/product/3614011/syr---s-goluboy-plesenyu--bzmzh-g/", "pic" : "https://photos.okolo.app/product/1166650-main/800x800.jpeg?updated_at=2024-11-15T09:07:39.136Z"}]


@app.route("/<req>", methods=["GET", "POST"])
def search(req):
    #if 'userLogged' not in session or session['userLogged'] != username:
    #    abort(401)
    #session.clear()
    search_res = []
    if request.method == "POST":
        return redirect(url_for('search', req=request.form['product_name']))
    if req:
        search_request = req
        search_res = [item for item in data if item["name"] in search_request]
    return render_template("search.html", products=search_res)
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        return redirect(url_for('search', req=request.form['product_name']))
    else:
        return render_template("index.html")


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
