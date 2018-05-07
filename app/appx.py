# http://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/
import datetime
import functools
import os
import re
import urllib

from flask import (Flask, abort, flash, Markup, redirect, render_template, 
request, Response, session, url_for)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
#
# from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
# from playhouse.sqlite_ext import *
from flask_sqlalchemy import SQLAlchemy


ADM = "json.conf" # just prototype, use config or oneway hash
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DB = "sqlite:///blog.db"
print("\n"+ format(DB))
DEBUG = False
SECRET_KEY = "UseRandomAndOsForCryptKey" # used by flask to encrypt sess cookie
SITE_WIDTH = 800

app = Flask(__name__)
app.config.from_object(__name__)

DB = SQLAlchemy(app)

oembed_providers = bootstrap_basic(OEmbedCache())

class Entry(DB.Model):
    id = DB.Column("entry_id", DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100))
    slug = DB.Column(DB.String(100))
    content = DB.Column(DB.String(500))
    published = DB.Column(DB.Boolean)
    timestamp = DB.Column(DB.String(100))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub("[^\w]+", "-", self.title.lower())
        ret = super(Entry, self).save(*args, **kwargs)
        # store search content
        self.update_search_index()
        return ret

@app.errorhandler(404)
def not_found():
    return Response("<h3> Not Found</h3>")

def main():
    global DB
    rv = DB.create_all()
    print("\n" + format(rv))
    app.run(debug=True)

if __name__ == "__main__":
    main()
    

