import datetime
import functools
import os
import re
import urllib
from flask import (Flask, abort, request, flash, url_for, redirect, render_template, Markup, Response, session)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *
#added
from flask_sqlalchemy import SQLAlchemy # extension for sqlalchemy
import datetime
from sqlalchemy import Column # pure sqlalchemy
from werkzeug import secure_filename
import utility.utility_helper as uHelper

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"
app.config["SECRET_KEY"] = "random string"
app.config["ADMIN_PASSWORD"] = "justForTest"
UPLOAD_FOLDER = './static/img/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
db = SQLAlchemy(app)

class Entry(db.Model):
   id = db.Column("entry_id", db.Integer, primary_key = True)
   title = db.Column("entry_title", db.String(100))
   slug = db.Column("entry_slug", db.String(50))
   content = db.Column("entry_content", db.String(200)) 
   pub_time = db.Column("entry_time", db.DateTime)
   img = db.Column("entry_img", db.String(200)) 

@app.route("/entry")
def entry():
      li = "test" # uHelper.list_images()
      page = request.args.get("page", 1, type=int)
      entry = Entry.query.paginate(per_page=2, page=page, error_out=True)
      next_url = url_for("entry", page=entry.next_num)
      
      prev_url = url_for("entry", page=entry.prev_num)
      # utiliy helper check with images from db and load correct
      return render_template("page.html", entry=entry, next_url=next_url, prev_url=prev_url, li=li)



@app.route("/")
def show_all():
      # pagination
   tmp = Entry.query.all()
   return render_template("show_all.html", entry = Entry.query.all(), entr=tmp, ti=datetime.datetime.now() )

@app.route("/new", methods = ["GET", "POST"])
def new():
   if request.method == "POST":
      if not request.form["title"] or not request.form["slug"] or not request.form["cont"]: #or not uHelper.check_file(request.files["file"] == True):
         flash("Please enter all the fields", "error")
      else:
         try:
               fil = request.files["file"]
               filename = secure_filename(fil.filename)
               fil.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         except Exception:
               # there was no image uploaded
               fil = "NoImage" + format(datetime.datetime.now())

         entry = Entry(title=request.form["title"], slug=request.form["slug"],
            content=request.form["cont"], pub_time=datetime.datetime.now(), img=str(fil))
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