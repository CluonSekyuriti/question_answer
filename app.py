from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    img_url = Column(String)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # name = "apple"
    # price = 5
    # new_product = Product(name=name, price=price)
    # db.session.add(new_product)
    # db.session.commit()
    # Product.query.filter(Product.id == 1).update({
    #     "name": "Ananas",
    #     "price": 6,
    # })
    # Product.query.filter(Product.id == 1).delete()
    # db.session.commit()
    products = Product.query.order_by(Product.id).all()
    return render_template('index1.html', products=products)


@app.route('/product/<int:product_id>')
def product(product_id):
    product_info = Product.query.filter(Product.id == product_id).first()
    return render_template('index2.html', product_info=product_info)


@app.route('/settings')
def settings():
    return render_template('index3.html')


@app.route('/change')
def change():
    return render_template('index4.html')


@app.route('/register_product', methods=["POST"])
def register_product():
    product_name = request.form.get('product_name')
    product_price = int(request.form.get('product_price'))
    add = Product(name=product_name, price=product_price)
    db.session.add(add)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delet_product/<int:product_id>')
def delet_product(product_id):
    Product.query.filter(Product.id == product_id).delete()
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
