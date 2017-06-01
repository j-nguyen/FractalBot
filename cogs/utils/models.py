from sqlalchemy import Column, String, Sequence, Integer, ForeignKey, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    # Create the table fields
    name = Column(String(250), primary_key=True)
    description = Column(String(), nullable=False)

class User(Base):
    __tablename__ = "users"
    # Create table fields
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    levels = relationship("Level", uselist=False, back_populates="users")
    name = Column(String(250), nullable=False, unique=True)
    location = Column(String(10))
    platform = Column(String(25))

class Rank(Base):
    __tablename__ = "ranks"
    id = Column(Integer, Sequence('rank_id_seq'), primary_key=True)
    levels = relationship("Level", uselist=False, back_populates="ranks")
    roles = relationship("Role", uselist=False, back_populates="roles")
    xp = Column(Integer)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, Sequence('roles_id_seq'), primary_key=True)
    levels = relationship("Level", uselist=False, back_populates="roles")
    role_id = Column(Integer)
    rank_id = Column(Integer, ForeignKey('ranks.id'))
    ranks = relationship("Rank", back_populates="roles")

class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, Sequence('levels_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship("User", back_populates="levels")
    rank_id = Column(Integer, ForeignKey('ranks.id'))
    ranks = relationship("Rank", back_populates="levels")
    role_id = Column(Integer, ForeignKey('roles.id'))
    roles = relationship("Role", back_populates="levels")
    xp = Column(Integer)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, Sequence('topics_id_seq'), primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    role_id = Column(BIGINT, nullable=False)