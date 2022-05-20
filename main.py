from flask import Flask, render_template, redirect, request_started, url_for, request
import sqlite3
import smtplib, ssl
import json
import os

app = Flask(__name__)


# if __name__ == "__main__":
#     app.run(debug=True)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect("store.db")
conn.row_factory = dict_factory

conn.execute("""CREATE TABLE if not exists PRODUCTS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              name TEXT NOT NULL,
              price TEXT NOT NULL,
              sale DOUBLE NOT NULL,
              photo TEXT NOT NULL
            );
             """)
# send = os.environ['SEND']
# receive = os.environ['RECIEVE']
# Storedpassword = os.environ['PASSWORD']
send = "no"
recieve = "no"
Storedpassword = "no"


def email(name, query, email):
    message = f"""\
Subject: Query from {name} ({email})
  
{query}
  """
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = send
    if sender_email == "no":
        return None
    receiver_email = recieve
    password = Storedpassword
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


products = conn.execute("SELECT * FROM PRODUCTS").fetchall()

salees = []
for product in products:
    if product["sale"] != 1:
        salees.append(product)
for sale in salees:
    sale["newPrice"] = f"{float(sale['price']) * sale['sale']:.2f}"


@app.route('/')
def mainPage():
    return redirect(url_for('home'))


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        term = request.get_json()
        searchResults = []
        if term.lower() == "avishai":
            return json.dumps("gotoavi")
        if term.lower() == "6969420":
            return json.dumps("pftscout")
        for product in products:
            if term.lower() in product["name"].lower():
                searchResults.append(product)
        return json.dumps(searchResults)
    else:
        return render_template("home.html",
                               title="Home",
                               products=products)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        emailaddress = request.form.get('email', 'not found')
        name = request.form.get('name', 'not found')
        query = request.form.get('query', 'not found')
        email(name, query, emailaddress)
    return render_template("contact.html", title="Contact")

@app.route('/login', methods=["POST"])
def login():
    emailaddress = request.form.get('email', 'not found')
    password = request.form.get('psw', 'not found')
    urlname = request.form.get("address", "not found").split("/")[-1]
    return render_template(f"{urlname}.html", title=f"{urlname.capitalize()}", products=products, salees=salees)


@app.route('/sales')
def sales():
    return render_template("sales.html", title="Sales", salees=salees)


@app.route("/gaming")
def gaming():
    return render_template("gaming.html", title="Gaming")


@app.route("/logic")
def logic():
    return render_template("logic.html", title="Logic")


@app.route("/avishai")
def avishai():
    return render_template("avishai.html", title="avishai")


@app.route("/pft")
def pft():
    return render_template("pft.html", title="Pause for Thought")
app.run(host='0.0.0.0', port=5002)


