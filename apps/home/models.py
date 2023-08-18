from apps import db

class Transaction(db.Model):
    __tablename__ = 'Transaction'

    uid=db.Column(db.Integer,db.ForeignKey('Users.id'),nullable=False)
    tran_id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    Stock_name = db.Column(db.String(64),nullable=False)
    buySell = db.Column(db.Integer,nullable=False)
    Price = db.Column(db.Integer,nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

