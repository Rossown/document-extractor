from api.models import db, Person
from api.errors import NotFoundError, BadRequestError
from config import Config, logger
from utils import paginate

class PersonService:
    @staticmethod
    def create_person(**kwargs):
        """ Create a new person """
        if not kwargs.get('name') or not kwargs.get('name').strip():
            raise BadRequestError("Person name is required")
        person = Person(**kwargs)  
        db.session.add(person)
        db.session.commit()
        logger.info(f"Created new person: {person}")
        return person
        
    @staticmethod
    def get_person_by_id(person_id):
        """ Get a person by its ID """
        person = Person.query.get(person_id)
        if not person:
            logger.warning(f"Person with ID {person_id} not found")
            raise NotFoundError(f"Person with ID {person_id} not found")
        logger.info(f"Retrieved person with ID {person_id}: {person}")
        return person
    
    @staticmethod
    def list_persons(cursor_id=None, limit=Config.PAGINATION_DEFAULT_LIMIT):
        """ List all persons """
        persons = Person.query
        if not persons:
            logger.warning("No persons found")
            raise NotFoundError("No persons found")
        return paginate(persons, cursor_id=cursor_id, limit=limit)
    
    @staticmethod
    def update_person(person_id, **kwargs):
        """ Update a person by its ID """
        person = Person.query.get(person_id)
        if not person:
            logger.warning(f"Person with ID {person_id} not found")
            raise NotFoundError(f"Person with ID {person_id} not found")
        for key, value in kwargs.items():
            setattr(person, key, value)
        db.session.commit()
        logger.info(f"Updated person: {person}")
        return person
    
    @staticmethod
    def delete_person(person_id):
        """ Delete a person by its ID """
        person = Person.query.get(person_id)
        if not person:
            logger.warning(f"Person with ID {person_id} not found")
            raise NotFoundError(f"Person with ID {person_id} not found")
        db.session.delete(person)
        db.session.commit()
        logger.info(f"Deleted person with ID {person_id}")