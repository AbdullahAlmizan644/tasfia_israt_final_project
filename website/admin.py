from flask import Blueprint, redirect,render_template,flash,request, session
from .__init__ import db
from .settings import info


admin=Blueprint('admin', __name__)

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



@admin.route("/dashboard")
def dashboard():
    if 'admin' in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()
        
        return render_template("admin/index.html",users=users)

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
    if 'admin' in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM products")
        products=cur.fetchall()
        
        return render_template("admin/product_dashboard.html",products=products)

    else:
        return redirect("/admin_login")   

    
    




