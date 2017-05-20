from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    # Create the table fields
    name = Column(String(250), primary_key=True)
    description = Column(String(), nullable=False)

    def __repr__(self):
        return "<Tag(name='{}', description='{}'>".format(self.name, self.description)