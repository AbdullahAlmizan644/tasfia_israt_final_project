from flask import Blueprint,render_template,session,flash,redirect,request
from .__init__ import db,create_app
from flask_mail import Mail,Message

interior=Blueprint('interior', __name__)
app=create_app()
mail=Mail()



@interior.route("/")
def index():
    return render_template("interior/index.html")


@interior.route("/team")
def team():
    return render_template("interior/team.html")


@interior.route("/pricing")
def pricing():
    return render_template("interior/pricing.html")



@interior.route("/about")
def about():
    return render_template("interior/about.html")



@interior.route("/faq")
def faq():
    return render_template("interior/faq.html")


@interior.route("/projects")
def projects():
    return render_template("interior/projects.html")


@interior.route("/news")
def news():
    return render_template("interior/news.html")



@interior.route("/service")
def service():
    return render_template("interior/service.html")

    


@interior.route("/contact",methods=["GET","POST"])
def contact():
    if "user" in session:
        if request.method=="POST":
            name=request.form.get("name")
            email=request.form.get("email")
            message=request.form.get("message")
            if len(message)<20:
                flash("please write greater than 20 alphabet.",category="error")
                return "<script>Write more than 20 alphabet</script>"

            msg = Message(f'message from {name}',sender=email,recipients=['dekbovideo@gmail.com'])  
            msg.body = str(message)  
            mail.send(msg) 
            flash("thanks for your message we will reply soon",category="success")
            return redirect("/")
        return render_template("interior/contact.html")
    else:
        return redirect("/login")


