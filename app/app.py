from flask import (Flask, abort, request, flash, url_for, redirect, render_template, Markup, Response, session)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
#added
from flask_sqlalchemy import SQLAlchemy # extension for sqlalchemy
import datetime
from sqlalchemy import Column # pure sqlalchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"
app.config["SECRET_KEY"] = "random string"
admin_pass = "testing" #just for test
db = SQLAlchemy(app)

class Entry(db.Model):
   id = db.Column("entry_id", db.Integer, primary_key = True)
   title = db.Column("entry_title", db.String(100))
   slug = db.Column("entry_slug", db.String(50))
   content = db.Column("entry_content", db.String(200)) 
   pub_time = db.Column("entry_time", db.DateTime, default=datetime.datetime.now())

def __init__(self, title, slug, content, pub_time):
   self.title = title
   self.slug = slug
   self.content = content
   self.pub_time = pub_time

@app.route("/")
def show_all():
   tmp = Entry.query.all()
   return render_template("show_all.html", entry = Entry.query.all(), entr=tmp )

@app.route("/new", methods = ["GET", "POST"])
def new():
   if request.method == "POST":
      if not request.form["title"] or not request.form["slug"] or not request.form["cont"]:
         flash("Please enter all the fields", "error")
      else:
         entry = Entry(title=request.form["title"], slug=request.form["slug"],
            content=request.form["cont"])
         
         db.session.add(entry)
         db.session.commit()
         flash("Record was successfully added")
         return redirect(url_for("show_all"))
   return render_template("new.html")

@app.route("/", methods = ["GET", "POST"])
def delete():
   if request.method == "POST":
      if not request.form["del"]:
         flash("Please enter all the fields", "error")
      else:
         del_id = request.form["del"]
         entry = None
         try:
               entry = Entry.query.filter_by(id=int(del_id)).first()
               db.session.delete(entry)
               db.session.commit()
               flash("Record was successfully deleted: " + format(entry), "succsess")
         except Exception:
               flash("Record does not exist: " + format(del_id) + " " + format(entry))
                


      return redirect(url_for("show_all"))

@app.errorhandler(404)
def not_found(error):
      return Response("<h3>Not found 404</h3"), 404


if __name__ == "__main__":
   db.create_all()
   app.run(debug = True)