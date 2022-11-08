from flask import Flask, render_template, request, redirect
from src.models import User, Info
from src.db import db_session
print(dir(Flask))
app = Flask(__name__)
app.debug = True
app.debug = "development"


@app.route("/", strict_slashes=False)
def index():
    users = db_session.query(User).all()
    infos = db_session.query(Info).all()
    return render_template("index.html", users=users, infos=infos)

@app.route('/healthcheck')
def healthcheck():
    return 'I am there'

@app.route("/detail/<id>", strict_slashes=False)
def detail(id):
    user = db_session.query(User).filter(User.id == id).first()
    info = db_session.query(Info).filter(Info.id == id).first()
    return render_template("detail.html", user=user, info=info)


@app.route("/contact/", methods=["GET", "POST"], strict_slashes=False)
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        birthday = request.form.get("birthday")
        address = request.form.get("address")
        user = User(username=username, phone=phone)
        db_session.add(user)
        db_session.commit()
        info = Info(name=name, surname=surname, email=email,
                    birthday=birthday, address=address, info_id=user.id)
        db_session.add(info)
        db_session.commit()
        return redirect("/")

    return render_template("contact.html")


@app.route("/delete/<id>", strict_slashes=False)
def delete(id):
    db_session.query(User).filter(User.id == id).delete()
    db_session.query(Info).filter(Info.id == id).delete()
    db_session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run()