from venv import create
from flask import Blueprint, redirect,render_template,flash,request, session
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .settings import info


admin=Blueprint('admin', __name__)
app=create_app()

@admin.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')

        if email==info['admin_email'] and password==info['admin_password']:
            session['admin']=email
            return redirect("/dashboard")
        else:
            flash("wrong email or password", category="error")
    return render_template("admin/admin_login.html")



@admin.route("/admin_logout")
def admin_logout():
    session.pop("admin",None)
    return redirect("/admin_login")


@admin.route("/dashboard")
def dashboard():
    cur=db.connection.cursor()  
    cur.execute("SELECT count(id) from orders")
    total_order=cur.fetchone()


    cur=db.connection.cursor()  
    cur.execute("SELECT count(username) from users")
    total_user=cur.fetchone()

    cur=db.connection.cursor()  
    cur.execute("SELECT count(product_id) from products")
    total_product=cur.fetchone()

    if 'admin' in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()
        
        return render_template("admin/index.html",users=users,total_order=total_order,total_product=total_product,total_user=total_user)

    else:
        return redirect("/admin_login")


@admin.route("/delete_user/<int:sno>")
def delete_user(sno):
    cur=db.connection.cursor()
    cur.execute("DELETE FROM users WHERE sno=%s",(sno,))
    cur.connection.commit()
    return redirect("/dashborad")



@admin.route("/product_dashboard")
def product_dashboard():
    cur=db.connection.cursor()  
    cur.execute("SELECT count(product_id) from products")
    total_product=cur.fetchone()
    if 'admin' in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM products")
        products=cur.fetchall()
        
        return render_template("admin/product_dashboard.html",products=products,total_product=total_product)

    else:
        return redirect("/admin_login")   

@admin.route("/add_product",methods=["GET","POST"])
def add_product():
    if "admin" in session:
        if request.method=="POST":
            name=request.form.get("name")
            category=request.form.get("category")
            image=request.form.get("image")
            price=request.form.get("price")
            description=request.form.get("description")

            image = request.files['image']
            if image.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
                cur=db.connection.cursor()
                cur.execute("INSERT INTO products(name,category,image,price,description,date) VALUES (%s,%s,%s,%s,%s,%s)",(name,category,image.filename,price,description,datetime.now(),))
                db.connection.commit()
                flash("product added successfully!",category="success")
                return redirect("/product_dashboard")
        
        return render_template("admin/add_product.html")
    
    else:
        return redirect("/admin_login")


@admin.route("/delete_product/<int:id>")
def delete_product(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM products WHERE product_id=%s",(id,))
        db.connection.commit()
        flash("product delete",category="error")
        return redirect("/product_dashboard")
    
    else:
        return redirect("/admin_login")
    



@admin.route("/all_order")
def all_order():
    if "admin" in session:
        cur=db.connection.cursor()  
        cur.execute("SELECT count(id) from orders")
        total_order=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM orders")
        orders=cur.fetchall()
        return render_template("admin/all_order.html",orders=orders,total_order=total_order)

    else:
        return redirect("/admin_login")


@admin.route("/delete_order/<int:id>")
def delete_order(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM orders WHERE id=%s",(id,))
        db.connection.commit()
        flash("Delete order!",category="error")
        return redirect("/all_order")
    
    else:
        return redirect("/admin_login")


