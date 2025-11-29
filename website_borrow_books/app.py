from flask import Flask, render_template, redirect, url_for, request
import requests
from pandas import Timestamp, Timedelta

app = Flask(__name__)

# ------------------------------------------------------
# 1) DATA MODEL CLASS
# ------------------------------------------------------


class Borrow_Request:
    def __init__(self, name: str, thisbook: str, borrow_date: str, email: str) -> None:
        self.name = name
        self.thisbook = thisbook
        self.borrow_date = borrow_date
        self.email = email
        self.return_date = str(Timestamp('2025-11-25') +
                               Timedelta(7, unit='day'))[:10]

    def to_dict(self):
        return {
            "name": self.name,
            "thisbook": self.thisbook,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "email": self.email
        }

# ------------------------------------------------------
# 2) CLASS send info to make
# ------------------------------------------------------


class MakeWebhookClient:
    def __init__(self, url):
        self.url = url

    def send(self, payload: dict):
        try:
            requests.post(self.url, json=payload)
        except Exception as e:
            print("Error sending to Make:", e)


# Instance ตัวส่ง webhook
make_client = MakeWebhookClient(
    "https://hook.eu1.make.com/2j6pi5o2kvvgg98obrlpoqi9yvcel7cd"
)

# ------------------------------------------------------
# ROUTES
# ------------------------------------------------------


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/books')
def books():
    return render_template('books.html')


@app.route('/labye')
def labye():
    return render_template('labye.html')


@app.route('/the_let_them')
def the_let_them():
    return render_template('the_let_them.html')


@app.route('/manifest1')
def manifest1():
    return render_template('manifest1.html')


@app.route('/manifest2')
def manifest2():
    return render_template('manifest2.html')


@app.route('/fatbook')
def fatbook():
    return render_template('fatbook.html')


@app.route('/do1')
def do1():
    return render_template('do1.html')


@app.route('/fishing')
def fishing():
    return render_template('fishing.html')


@app.route('/money')
def money():
    return render_template('money.html')


@app.route('/chill')
def chill():
    return render_template('chill.html')


@app.route('/borrowpages')
def borrowpages():
    return render_template('borrowpages.html')


@app.route('/submit', methods=['POST'])
def submit():

    # 1) an object from form user and save in class Borrow_Request
    borrow_request = Borrow_Request(
        name=request.form['name'],
        thisbook=request.form['thisbook'],
        borrow_date=request.form['borrow_date'],
        email=request.form['email']
    )

    # Debug print
    print(borrow_request.to_dict())

    # 2) send to make
    make_client.send(borrow_request.to_dict())

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)
