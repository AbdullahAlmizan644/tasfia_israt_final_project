from flask import Blueprint,render_template


shop=Blueprint('shop', __name__)

@shop.route('/shop')
def interior_shop():
    return render_template('shop/shop.html')


@shop.route('/detail')
def detail():
    return render_template("shop/detail.html")


@shop.route('/checkout')
def checkout():
    return render_template("shop/checkout.html")



@shop.route('/cart')
def cart():
    return render_template("shop/cart.html")

