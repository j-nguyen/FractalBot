from sqlalchemy import Column, String, Sequence, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    # Create the table fields
    name = Column(String(250), primary_key=True)
    description = Column(String(), nullable=False)

    def __repr__(self):
        return "<Tag(name='{}', description='{}'>".format(self.name, self.description)

class User(Base):
    __tablename__ = "users"
    # Create table fields
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    level = relationship("levels", uselist=False, back_populates="users")
    name = Column(String(250), nullable=False, unique=True)
    location = Column(String(10))
    platform = Column(String(25))

    def __repr__(self):
        return "<User(name='{}', description='{}'>".format(self.name, self.description)

class Rank(Base):
    __tablename__ = "ranks"
    id = Column(Integer, Sequence('rank_id_seq'), primary_key=True)
    xp = Column(Integer)

    def __repr__(self):
        return "<Rank(name='{}', description='{}'>".format(self.name, self.description)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, Sequence('roles_id_seq'), primary_key=True)
    role_id = Column(Integer)

    def __repr__(self):
        return "<Role(name='{}', description='{}'>".format(self.name, self.description)

class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, Sequence('levels_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("users", back_populates="levels")
    rank_id = Column(Integer, ForeignKey('ranks.id'))
    rank = relationship("ranks", back_populates="levels")
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("roles", back_populates="levels")
    xp = Column(Integer)


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, Sequence('topics_id_seq'), primary_key=True)
    name = Column(String(250), nullable=False)
    rank_id = Column(Integer, nullable=False)