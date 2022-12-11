from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, init, migrate
from sqlalchemy import not_, or_
from datetime import date, datetime, timedelta

 
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
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=True)
    
    
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_belopp = db.Column(db.Integer, unique=False, nullable=False)
    forfallodatum = db.Column(db.Date, unique=False, nullable=False)
    betald = db.Column(db.Boolean,unique=False, nullable=False)
    bokningar = db.relationship('Booking', backref='invoice', lazy=True)
    
    
    
def BusyRooms(borjan_date, slut_date):
    
    upptagna = []
    for r in Room.query.join(Booking).filter(or_(Booking.start_date.between(borjan_date, slut_date),(Booking.end_date.between(borjan_date,slut_date)))):
        upptagna.append(r.id)
    return upptagna
    
def PrintBusyRooms(borjan_date, slut_date):
    
    for r in Room.query.join(Booking).filter(or_(Booking.start_date.between(borjan_date, slut_date),(Booking.end_date.between(borjan_date,slut_date)))):
        print(f"Rum: {r.id} ")
        upptagna.append(r.id)
        for b in r.bokningar:
            print(f"    {b.start_date} {b.end_date}  Dessa rum går inte att boka!")
        print(" 1-5 är alla rum som går att boka")
        
def SearchFreeRooms(borjan_date, slut_date):
    
    for r in Room.query.join(Booking).filter(or_(Booking.start_date.between(borjan_date, slut_date),(Booking.end_date.between(borjan_date,slut_date)))):    
        print(f"Rum: {r.id} ")
        for b in r.bokningar:
            c = Customer.query.filter_by(id=b.customer_id).first()
            print(f"    {b.start_date} {b.end_date} Bokat utav: {c.namn}  Dessa rum går inte att boka!")


    
    
if __name__  == "__main__":
    with app.app_context():
        upgrade()

    with app.app_context():
        while True:
            print("1. Register customer")
            print("2. Edit customer")
            print("3. Book a room")
            print("4. Search free rooms and customer")
            print("5. Remove a customer")
            print("6. Remove a booking")
            print("7. Change booking")
            print("8. Register payment")
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
               
                borjan_date = input("Format YYYY-MM-DD (Default: 2022-12-02): ") or "2022-12-02"
                slut_date = input("Format YYYY-MM-DD (Default: 2022-12-16): ") or "2022-12-16"
                
                upptagna = BusyRooms(borjan_date, slut_date)
                PrintBusyRooms(borjan_date, slut_date)
                
            
                b = Booking()
                b.customer_id = input("Ange customer ID:")
                b.room_id = int(input(("Ange Room ID (1-5 finns)")))
                b.start_date = borjan_date
                b.end_date = slut_date
                print(upptagna)
                if b.room_id in upptagna:
                    print("Det går ej att boka detta rum, byt ID")
                else:
                    now = datetime.now()
                    tiodagar = timedelta(days=10)
                    
                    f = Invoice()
                    f.invoice_belopp = 200
                    f.forfallodatum = (now+tiodagar).date()
                    f.betald = False
                    b.invoice = f
                    db.session.add(b)
                    db.session.commit()
                    print("Rum ombokat")
            if sel == "4":
                borjan_date = input("Format YYYY-MM-DD (Default: 2010-01-01): ") or "2010-01-01"
                slut_date = input("Format YYYY-MM-DD (Default: 2040-10-10): ") or "2040-10-10"
                
                SearchFreeRooms(borjan_date, slut_date)
                print("Rummen som finns är 1-5")
    
            if sel == "5":
                for x in Customer.query.all():
                    print(f"{x.id} {x.namn} {x.telefonnummer} Har bokningar?: {len(x.bokningar)}")
                delete = input("Skriv in kund-id som ska tas bort")
                c = Customer.query.filter_by(id=delete).first()
                if len(c.bokningar) > 0:
                    print("Du kan inte ta bort en kund med stående bokning")
                else:
                    Customer.query.filter_by(id=delete).delete()
                    db.session.commit()
                    print("Kund borttagen")
                    
            if sel == "6":
                for x in Booking.query.all():
                    print(x.id)
                delete = input("Which booking ID would you like to remove?")
                Booking.query.filter_by(id=delete).delete()
                db.session.commit()
                print("Bokning borttagen")
                
            if sel == "7":
                
                for x in Booking.query.all():
                    print(x.id)
                booking_id = input("Vilken bokning vill du ändra?")
                
                borjan_date = input("Format YYYY-MM-DD (Default: 2022-12-02): ") or "2022-12-02"
                slut_date = input("Format YYYY-MM-DD (Default: 2022-12-16): ") or "2022-12-16"
                upptagna = []
                upptagna = BusyRooms(borjan_date, slut_date)
                PrintBusyRooms(borjan_date, slut_date)
                
                b = Booking.query.filter_by(id=booking_id).first()
                b.start_date = borjan_date
                b.end_date = slut_date
                if b.room_id in upptagna:
                    print("Det går ej att boka detta rum, byt ID")
                else:
                    db.session.commit()
                    print("Rum ombokat")
            if sel == "8":
                for x in Invoice.query.all():
                    print(x.id)
                id = input("Which invoice would you like to register?")
                f = Invoice.query.filter_by(id=id).first()
                f.betald = True
                db.session.commit()
                print("invoice paid")
                
                
                