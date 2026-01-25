from api.models import db, SalesTerritory
from api.errors import NotFoundError, BadRequestError
from config import Config, logger
from utils import paginate

class TerritoryService:
    @staticmethod
    def create_territory(name, country_region_code, group):
        """ Create a new sales territory """
        if not name or not name.strip():
            raise BadRequestError("Sales territory name is required")
        if not country_region_code or not country_region_code.strip():
            raise BadRequestError("Country/Region code is required")
        if not group or not group.strip():
            raise BadRequestError("Sales territory group is required")
        
        territory = SalesTerritory(name=name, country_region_code=country_region_code, group=group)
        
        db.session.add(territory)
        db.session.commit()
        logger.info(f"Created new sales territory: {territory}")
        return territory
        
    @staticmethod
    def get_territory_by_id(territory_id):
        """ Get a sales territory by its ID """
        territory = SalesTerritory.query.get(territory_id)
        if not territory:
            logger.warning(f"Sales territory with ID {territory_id} not found")
            raise NotFoundError(f"Sales territory with ID {territory_id} not found")
        logger.info(f"Retrieved sales territory with ID {territory_id}: {territory}")
        return territory

    
    @staticmethod
    def list_territories(cursor_id=None, limit=Config.PAGINATION_DEFAULT_LIMIT):
        """ Get all sales territories """
        territories = SalesTerritory.query
        if not territories:
            logger.warning("No sales territories found")
            raise NotFoundError("No sales territories found")
        return paginate(territories, order_by=SalesTerritory.id,cursor_id=cursor_id, limit=limit)
    
    @staticmethod
    def update_territory(territory_id, name=None, country_region_code=None, group=None):
        """ Update a sales territory """
        territory = SalesTerritory.query.get(territory_id)
        if not territory:
            logger.warning(f"Sales territory with ID {territory_id} not found")
            raise NotFoundError(f"Sales territory with ID {territory_id} not found")
        if name is not None:
            territory.name = name
        if country_region_code is not None:
            territory.country_region_code = country_region_code
        if group is not None:
            territory.group = group
        db.session.commit()
        logger.info(f"Updated sales territory: {territory}")
        return territory
    
    @staticmethod
    def delete_territory(territory_id):
        """ Delete a sales territory """
        territory = SalesTerritory.query.get(territory_id)
        if not territory:
            logger.warning(f"Sales territory with ID {territory_id} not found")
            raise NotFoundError(f"Sales territory with ID {territory_id} not found")
        db.session.delete(territory)
        db.session.commit()
        logger.info(f"Deleted sales territory: {territory}")