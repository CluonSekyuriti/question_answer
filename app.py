from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index1.html')


@app.route('/product')
def product():
    return render_template('index2.html')


@app.route('/settings')
def settings():
    return render_template('index3.html')


if __name__ == '__main__':
    app.run()
