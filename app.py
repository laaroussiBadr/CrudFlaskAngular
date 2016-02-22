import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

# Create application
app = Flask(__name__)

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.username

# Create M2M table
post_tags_table = db.Table('post_tags', db.Model.metadata,
                           db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                           db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                           )

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='posts')

    tags = db.relationship('Tag', secondary=post_tags_table)

    def __unicode__(self):
        return self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(64))

    def __unicode__(self):
        return self.name


def add_cors_header(response):
        allow = 'HEAD, OPTIONS'

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = allow
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

manager = APIManager(app, flask_sqlalchemy_db=db)
app.after_request(add_cors_header)

manager.create_api(User, methods=['GET', 'POST', 'DELETE','PUT'])
manager.create_api(Post, methods=['GET', 'POST', 'DELETE','PUT'])
manager.create_api(Tag, methods=['GET', 'POST', 'DELETE','PUT'])

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    
    if not os.path.exists(database_path):
        db.create_all()

    # Start app
    app.run(debug=True)