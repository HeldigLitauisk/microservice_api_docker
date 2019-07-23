#!/usr/bin/env python3

"""
Main API page for returning information postreSQL database
JSON requests scheme is being validated inside swagger.yaml file

Usage:
docker-compose up -d
docker-compose build
docker run --network="host" -p 8080:8080 main_api
"""
import datetime
import logging
import connexion
from connexion import NoContent
import radio_db


def get_location(radio_id):
    """ Returns json with the name of the location

    :param radio_id: Radio ID (a unique integer)
    :return: json notation {“location”: string} if location exists 404 otherwise

    """
    resp = db_session.query(radio_db.RadioProfile).filter(radio_db.RadioProfile.id == radio_id).one_or_none()
    loc = resp.dump(keys=['location']) if resp else None
    return (loc, 200) if loc and loc['location'] else (NoContent, 404)


def post_location(radio_id, location):
    """ Sets location if location is among allowed locations

    :param radio_id: Radio ID (a unique integer)
    :param location: string name of the location
    :return: 200 if location was set otherwise 403
    """
    loc_obj = db_session.query(radio_db.RadioProfile).filter(radio_db.RadioProfile.id == radio_id).one_or_none()
    if loc_obj:
        if location['location'] in list(loc_obj.allowed_locations):
            logging.info('Updating location >>> {}'.format(radio_id))
            loc_obj.location = location['location']
            db_session.commit()
            return NoContent, 200
    return NoContent, 403


def post_register_radio(radio_id, radio):
    """ Updates or creates a new radio id with given details. Never changes location details

    :param radio_id: Radio ID (a unique integer)
    :param radio: json objects coming from post request
    :return:
    """
    radio_ex = db_session.query(radio_db.RadioProfile).filter(radio_db.RadioProfile.id == radio_id).one_or_none()
    radio['id'] = radio_id
    radio['location'] = None
    if radio_ex:
        logging.info('Updating radio profile >>> {}'.format(radio_id))
        radio_ex.update(**radio)
    else:
        logging.info('Creating new radio profile >>> {}'.format(radio_id))
        radio['created'] = datetime.datetime.utcnow()
        db_session.add(radio_db.RadioProfile(**radio))
    db_session.commit()
    return NoContent, (200 if radio_ex else 201)


logging.basicConfig(level=logging.INFO)
# Uses postgresql database server running as docker instance
db_session = radio_db.init_db('postgresql+psycopg2://postgres@localhost/postgres?port=5432')
app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml')


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
