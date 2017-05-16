from sqlalchemy import Column, String

class Tags(Base):
	__tablename__ = 'tags'
	# Create the table fields
	id = Column(String(250), primary_key=True)
	command = Column(String(500), nullable=False)