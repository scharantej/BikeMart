
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikes.db'
db = SQLAlchemy(app)

class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Bike %r>' % self.name

@app.route('/')
def home():
    bikes = Bike.query.all()
    return render_template('home.html', bikes=bikes)

@app.route('/bike_detail/<int:bike_id>')
def bike_detail(bike_id):
    bike = Bike.query.get_or_404(bike_id)
    return render_template('bike_detail.html', bike=bike)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    bike_id = request.form.get('bike_id')
    quantity = request.form.get('quantity')
    bike = Bike.query.get_or_404(bike_id)
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    if bike_id in cart:
        cart[bike_id]['quantity'] += int(quantity)
    else:
        cart[bike_id] = {'bike': bike, 'quantity': int(quantity)}
    return redirect(url_for('home'))

@app.route('/show_cart')
def show_cart():
    cart = session['cart']
    return render_template('cart.html', cart=cart)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    cart = session['cart']
    total = 0
    for bike_id, item in cart.items():
        bike = item['bike']
        quantity = item['quantity']
        total += bike.price * quantity
    # process the order
    session.pop('cart', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
