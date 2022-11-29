from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, init, migrate
 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:my-secret-pw@localhost:3306/Hotell"
db = SQLAlchemy(app)
migrate = Migrate(app,db)
 
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_size = db.Column(db.Integer, unique=False, nullable=False)
    bed_count = db.Column(db.Integer, unique=False, nullable=False)

    
if __name__  == "__main__":
    with app.app_context():
        upgrade()
