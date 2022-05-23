from flask import Blueprint, redirect,render_template,flash,request, session
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .settings import info
from flask_mail import Mail,Message


shop=Blueprint('shop', __name__)

app=create_app()
mail=Mail()


@shop.route('/shop')
def interior_shop():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM products")
    products=cur.fetchall()
    return render_template('shop/shop.html',products=products)


@shop.route('/detail/<int:id>/<int:count>')
def detail(id,count):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM products WHERE product_id=%s",(id,))
    single_product=cur.fetchone()
    return render_template("shop/detail.html", single_product=single_product,count=count)



@shop.route('/cart')
def cart():
    return render_template("shop/cart.html")




@shop.route("/checkout",methods=["GET","POST"])
def checkout():
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(session["user"],))    
        user=cur.fetchone()
        if request.method=="POST":
            address=request.form.get("address")
            email=request.form.get("email")
            phone=request.form.get("phone")
            payment=request.form.get("payment")
            product=request.form.get("product_details")
            total=request.form.get("total")

            cur=db.connection.cursor() 
            cur.execute("INSERT INTO orders(username,email,phone,address,product,total,payment,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(user[1],email,phone,address,product,total,payment,datetime.now()))
            db.connection.commit()
            sms=f"Product:{product} Address:{address} Total Price:{total}"

            msg = Message("Book Order",sender="dekbovideo@gmail.com",recipients=[email])
            msg.html = f'<h1>Your Order Taken<h1><br><h2>{sms}</h2>'  
            mail.send(msg)

            flash("Send Mail",category="success")
            return redirect("/thankyou")           
        return render_template("shop/checkout.html")

    else:
        return redirect("/login")

@shop.route("/thankyou")
def thankyou():
    return render_template("shop/thankyou.html")


@shop.route("/product_category/<string:cat>")
def product_category(cat):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM products where category=%s",(cat,))    
    products=cur.fetchall()
    return render_template("shop/product_category.html",products=products,cat=cat)