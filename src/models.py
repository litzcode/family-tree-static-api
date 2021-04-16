from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association table for parents<->children
children = db.Table('children',
                db.Column('child_id', db.Integer, db.ForeignKey('member.id')),
                db.Column('parent_id', db.Integer, db.ForeignKey('member.id'))
                )

class Member(db.Model):
    """Node within the family tree."""

    __tablename__ = "member"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    parents = db.relationship('Member',
                          secondary=children,
                          primaryjoin=(children.c.child_id == id),
                          secondaryjoin=(children.c.parent_id == id),
                          backref=db.backref('children', lazy='dynamic'),
                          lazy='dynamic')
    
    def __repr__(self):
        return '<Member %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "age": self.age
        }
        