from api.models import db, Person
from config import logger

class PersonService:
    @staticmethod
    def create_person(**kwargs):
        """ Create a new person """
        try:
            person = Person(**kwargs)
            db.session.add(person)
            db.session.commit()
            logger.info(f"Created new person: {person}")
            return person
        except Exception as e:
            logger.error(f"Error creating person: {e}")
            db.session.rollback()
            raise
        
    @staticmethod
    def get_person_by_id(person_id):
        """ Get a person by its ID """
        try:
            person = Person.query.get(person_id)
            if not person:
                logger.warning(f"Person with ID {person_id} not found")
                return None
            return person
        except Exception as e:
            logger.error(f"Error getting person by ID {person_id}: {e}")
            raise
    
    @staticmethod
    def list_persons():
        """ List all persons """
        try:
            persons = Person.query.all()
            logger.info(f"Found {len(persons)} persons")
            return persons
        except Exception as e:
            logger.error(f"Error listing persons: {e}")
            raise
    
    @staticmethod
    def update_person(person_id, **kwargs):
        """ Update a person by its ID """
        try:
            person = Person.query.get(person_id)
            if not person:
                logger.warning(f"Person with ID {person_id} not found")
                return None
            for key, value in kwargs.items():
                setattr(person, key, value)
            db.session.commit()
            logger.info(f"Updated person: {person}")
            return person
        except Exception as e:
            logger.error(f"Error updating person with ID {person_id}: {e}")
            db.session.rollback()
            raise
        
    @staticmethod
    def delete_person(person_id):
        """ Delete a person by its ID """
        try:
            person = Person.query.get(person_id)
            if not person:
                logger.warning(f"Person with ID {person_id} not found")
                return None
            db.session.delete(person)
            db.session.commit()
            logger.info(f"Deleted person with ID {person_id}")
            return person
        except Exception as e:
            logger.error(f"Error deleting person with ID {person_id}: {e}")
            db.session.rollback()
            raise