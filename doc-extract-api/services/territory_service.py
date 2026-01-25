from api.models import db, SalesTerritory
from config import logger

class TerritoryService:
    @staticmethod
    def create_territory(name, country_region_code, group):
        """ Create a new sales territory """
        try:
            territory = SalesTerritory(name=name, country_region_code=country_region_code, group=group)
            
            db.session.add(territory)
            db.session.commit()
            logger.info(f"Created new sales territory: {territory}")
            return territory
        except Exception as e:
            logger.error(f"Error creating sales territory: {e}")
            db.session.rollback()
            return None
        
    @staticmethod
    def get_territory_by_id(territory_id):
        """ Get a sales territory by its ID """
        try:
            territory = SalesTerritory.query.get(territory_id)
            logger.info(f"Retrieved sales territory with ID {territory_id}: {territory}")
            if not territory:
                logger.warning(f"Sales territory with ID {territory_id} not found")
                return None
            return territory
        except Exception as e:
            logger.error(f"Error retrieving sales territory with ID {territory_id}: {e}")
            raise
    
    @staticmethod
    def list_territories():
        """ Get all sales territories """
        try:
            territories = SalesTerritory.query.all()
            logger.info(f"Found {len(territories)} sales territories")
            return territories
        except Exception as e:
            logger.error(f"Error retrieving sales territories: {e}")
            raise
    
    @staticmethod
    def update_territory(territory_id, name=None, country_region_code=None, group=None):
        """ Update a sales territory """
        try:
            territory = SalesTerritory.query.get(territory_id)
            if not territory:
                logger.warning(f"Sales territory with ID {territory_id} not found")
                return None
            if name is not None:
                territory.name = name
            if country_region_code is not None:
                territory.country_region_code = country_region_code
            if group is not None:
                territory.group = group
            db.session.commit()
            logger.info(f"Updated sales territory: {territory}")
            return territory
        except Exception as e:
            logger.error(f"Error updating sales territory with ID {territory_id}: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def delete_territory(territory_id):
        """ Delete a sales territory """
        try:
            territory = SalesTerritory.query.get(territory_id)
            if not territory:
                logger.warning(f"Sales territory with ID {territory_id} not found")
                return False
            db.session.delete(territory)
            db.session.commit()
            logger.info(f"Deleted sales territory: {territory}")
            return True
        except Exception as e:
            logger.error(f"Error deleting sales territory with ID {territory_id}: {e}")
            db.session.rollback()
            return False