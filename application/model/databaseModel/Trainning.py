import datetime

from application import db, app


class Trainning(db.Model):
    """User account model."""
    __tablename__ = 'Trainning'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("Users.id")
    )
    version = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    over_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def createTrainning(self):
        self.created_on=datetime.datetime.utcnow()
        with app.app_context():
            db.session.add(self)

    def isOver(self):
        self.over_on = datetime.datetime.utcnow()

    def commit(self):
        with app.app_context():
            db.session.commit()

    def __repr__(self):
        return '<Train {}>'.format(self.username)