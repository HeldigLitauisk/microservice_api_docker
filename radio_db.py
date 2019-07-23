"""
Database setup containing one table and helper methods
"""

from sqlalchemy import Column, DateTime, String, create_engine, Integer, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class RadioProfile(Base):
    __tablename__ = 'radio_profiles'
    id = Column(Integer, primary_key=True)
    alias = Column(String(100))
    location = Column(String(50), default=None)
    allowed_locations = Column(ARRAY(String(50)))
    created = Column(DateTime())

    def update(self, id=None, alias=None, allowed_locations=None, location=None, created=None):
        """ Method updating existing values in the table.

        :param id: unique primary key integer
        :param alias: string name of the device
        :param allowed_locations: list of allowed locations as strings
        :param location: string name of the location, must be part of allowed_locations
        :param created: datetime of creation
        :return: updates db object with new values
        """
        if id and alias and allowed_locations:
            self.id = id
            self.alias = alias
            self.allowed_locations = allowed_locations
        elif location:
            self.location = location
        if created:
            self.created = created

    def dump(self, keys=None):
        """

        :param keys: list of keys to return as json
        :return: if not keys are defined returns variables of the object as json
        """
        if keys:
            return dict([(k, v) for k, v in vars(self).items() if k in keys])
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


def init_db(uri):
    """

    :param uri: postgreSQL host and port to connect
    :return: SQLalchemy db session object
    """
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
