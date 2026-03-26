from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Sample data - in a real app, this would be a database
items = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99, 'description': 'High-performance laptop'},
    {'id': 2, 'name': 'Phone', 'price': 699.99, 'description': 'Latest smartphone'},
    {'id': 3, 'name': 'Headphones', 'price': 199.99, 'description': 'Wireless headphones'},
    {'id': 3, 'name': 'Headphoness', 'price': 199.99, 'description': 'Wireless headphones'},
]

@app.route('/')
def home():
    return render_template('home.html', items=items)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return render_template('item_detail.html', item=item)
    return 'Item not found', 404

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for item_id in session['cart']:
            item = next((item for item in items if item['id'] == item_id), None)
            if item:
                cart_items.append(item)
                total += item['price']
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    # In a real app, process payment here
    session.pop('cart', None)
    return render_template('checkout_success.html')

if __name__ == '__main__':
    app.run(debug=True)
