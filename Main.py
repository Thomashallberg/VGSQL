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
    bokningar = db.relationship('Booking', backref='room', lazy=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(80), unique=False, nullable=False)
    telefonnummer = db.Column(db.String(80), unique=False, nullable=False)
    bokningar = db.relationship('Booking', backref='customer', lazy=True)
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_date = db.Column(db.Date, unique=False, nullable=False)
    end_date = db.Column(db.Date, unique=False, nullable=False)
    
if __name__  == "__main__":
    with app.app_context():
        upgrade()


    with app.app_context():
        while True:
            print("1. Register customer")
            print("2. Edit customer")
            print("3. Book a room")
            sel = input("What would you like to do?:")

            if sel == "1":
                c = Customer()
                c.namn = input("Ange namn:")
                c.telefonnummer = input("Ange telefonnummer:")
                db.session.add(c)
                db.session.commit()
            if sel == "2":
                for x in Customer.query.all():
                    print(f"{x.id} {x.namn} {x.telefonnummer}")
                sel = int(input("Vilket kund id vill du ändra?"))
                u = Customer.query.filter_by(id=sel).first()
                u.namn = input("Ange nytt namn:")
                u.telefonnummer = input("Ange nytt nummer:")
                db.session.commit()
            if sel == "3":
                b = Booking()
                b.customer_id = input("Ange customer ID:")
                b.room_id = input("Ange Room ID")
                b.start_date = input("Datum format (yyyy-mm-dd")
                b.end_date = input("Datum format (yyyy-mm-dd")
                db.session.add(b)
                db.session.commit()