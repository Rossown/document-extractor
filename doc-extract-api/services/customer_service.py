from api.models import db, Customer, SalesTerritory
from api.errors import NotFoundError, BadRequestError
from config import Config, logger
from utils import paginate

class CustomerService:
    @staticmethod
    def create_customer(person_id, store_id, territory_id, account_number):
        """ Create a new customer """
        try:
            # Check for duplicate account_number
            if Customer.query.filter_by(account_number=account_number).first():
                logger.warning(f"Account number {account_number} already exists.")
                raise BadRequestError("Account number already exists.")
            # Check for valid territory_id
            if territory_id is not None and not SalesTerritory.query.get(territory_id):
                logger.warning(f"Territory ID {territory_id} does not exist.")
                raise NotFoundError("Territory ID does not exist.")
            customer = Customer(person_id=person_id, store_id=store_id, territory_id=territory_id, account_number=account_number)
            db.session.add(customer)
            db.session.commit()
            logger.info(f"Created new customer: {customer}")
            return customer
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            db.session.rollback()
            raise BadRequestError(str(e))
        
    @staticmethod
    def get_customer_by_id(customer_id):
        """ Get a customer by its ID """
        customer = Customer.query.get(customer_id)
        if not customer:
            logger.warning(f"Customer with ID {customer_id} not found")
            raise NotFoundError(f"Customer with ID {customer_id} not found")
        return customer
        
    @staticmethod
    def list_customers(cursor_id=None, limit=Config.PAGINATION_DEFAULT_LIMIT):
        """ Get all customers """
        customers = Customer.query
        if not customers:
            logger.warning("No customers found")
            raise NotFoundError("No customers found")
        return paginate(customers, order_by=Customer.id, cursor_id=cursor_id, limit=limit)

    @staticmethod
    def update_customer(customer_id, person_id=None, store_id=None, territory_id=None, account_number=None):
        """ Update a customer's information """
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                logger.warning(f"Customer with ID {customer_id} not found")
                raise NotFoundError(f"Customer with ID {customer_id} not found")
            
            if person_id:
                customer.person_id = person_id
            if store_id:
                customer.store_id = store_id
            if territory_id:
                customer.territory_id = territory_id

            db.session.commit()
            logger.info(f"Updated customer: {customer}")
            return customer
        except Exception as e:
            logger.error(f"Error updating customer with ID {customer_id}: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def delete_customer(customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            logger.warning(f"Customer with ID {customer_id} not found")
            raise NotFoundError(f"Customer with ID {customer_id} not found")
        db.session.delete(customer)
        db.session.commit()
        logger.info(f"Deleted customer with ID {customer_id}")
