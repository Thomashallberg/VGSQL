from Main import Room
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, init, migrate
 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:my-secret-pw@localhost:3306/Hotell"
db = SQLAlchemy(app)

with app.app_context():
    room = Room()
    room.room_size = 1
    room.bed_count = 1
    db.session.add(room)
    
    room2 = Room()
    room2.room_size = 1
    room2.bed_count = 1
    db.session.add(room2)
    
    room3 = Room()
    room3.room_size = 1
    room3.bed_count = 1
    db.session.add(room3)
    db.session.commit()