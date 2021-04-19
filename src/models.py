from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association table for children<->parents
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
                          primaryjoin=(children.c.child_id == id), # primaryjoin means left side of association table is child_id
                          secondaryjoin=(children.c.parent_id == id), # secondaryjoin means right side of association table is parent_id
                          backref=db.backref('children', lazy='dynamic'),
                          lazy='dynamic')

                          # for testing relationships, for example to search for the childs of an specific member_id, run:
                          # $ mysql
                          # USE example;
                          # SHOW TABLES;  (to verify tables names in current database 'example')
                          # SELECT * FROM member, children WHERE member.id = children.parent_id;
    
    def __repr__(self):
        return '<Member %r>' % self.name

    def serialize(self, member_type): # add member_type parameter to serialize member_type
        return {
            member_type : {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "age": self.age
            }
        }
        