from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "nasigoreng"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cart_data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

data = [
    {
        "path": "../static/img/vegan  burger.png",
        "title": "Vegan burger",
        "cost": 4
    },
    {
        "path": "../static/img/meat lovers.png",
        "title": "Meat lovers",
        "cost": 4
    },
    {
        "path": "../static/img/chicken crispy burger.png",
        "title": "Chicken crispy",
        "cost": 5
    },
]


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    path = db.Column(db.String(250))
    amount = db.Column(db.Integer)
    cost = db.Column(db.String(250))
db.create_all()

@app.route("/")
def home():
    global data
    data = data
    return render_template("index.html", data=data)

@app.route("/done")
def done():
    data = db.session.query(Cart).all()
    for i in data:
        db.session.delete(i)
        db.session.commit()
    return render_template("done.html")

@app.route("/payment")
def payment():
    data = db.session.query(Cart).all()
    total = 0
    for i in data:
        total += int(i.cost)
    return render_template("payment.html", data=data, total=total)

@app.route("/shop")
def shop():
    data = db.session.query(Cart).all()
    total = 0
    for i in data:
        total += int(i.cost)
    return render_template("cart.html", data=data, total=total)

@app.route("/delete")
def delete():
    id = request.args.get('id')
    item = Cart.query.get(int(id))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('shop'))

@app.route("/delete1")
def delete_1_item():
    id = request.args.get('id')
    item = Cart.query.get(int(id))
    if item.amount == "1":
        db.session.delete(item)
        db.session.commit()
    else:
        item.amount = int(item.amount) - 1
        db.session.commit()
    return redirect(url_for('shop'))

@app.route("/cart")
def cart():
    name = request.args.get('name')
    cost = request.args.get('cost')
    burger = Cart.query.filter_by(name=name).first()
    print(burger)
    if burger != None:
        burger.amount = int(burger.amount) + 1
        burger.cost = int(burger.cost) + int(cost)
        db.session.commit()
        
    else:
        new_data = Cart(
            name = request.args.get('name'),
            path = request.args.get('path'),
            amount = 1,
            cost = request.args.get('cost'),
        )
        db.session.add(new_data)
        db.session.commit()
    return render_template("index.html", data=data)
if __name__ == "__main__":
    app.run(debug=True)