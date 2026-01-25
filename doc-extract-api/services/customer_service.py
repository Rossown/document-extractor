from api.models import db, Customer
from config import logger

class CustomerService:
    @staticmethod
    def create_customer(person_id, store_id, territory_id, account_number):
        """ Create a new customer """
        try:
            customer = Customer(person_id=person_id, store_id=store_id, territory_id=territory_id, account_number=account_number)
            db.session.add(customer)
            db.session.commit()
            logger.info(f"Created new customer: {customer}")
            return customer
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            db.session.rollback()
            raise
        
    @staticmethod
    def get_customer_by_id(customer_id):
        """ Get a customer by its ID """
        try:
            customer = Customer.query.get(customer_id)
            if customer:
                logger.info(f"Found customer: {customer}")
            else:
                logger.warning(f"Customer with ID {customer_id} not found")
            return customer
        except Exception as e:
            logger.error(f"Error retrieving customer with ID {customer_id}: {e}")
            raise
        
    @staticmethod
    def list_customers():
        """ Get all customers """
        try:
            customers = Customer.query.all()
            logger.info(f"Found {len(customers)} customers")
            return customers
        except Exception as e:
            logger.error(f"Error retrieving customers: {e}")
            raise
    
    @staticmethod
    def update_customer(customer_id, person_id=None, store_id=None, territory_id=None, account_number=None):
        """ Update a customer's information """
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                logger.warning(f"Customer with ID {customer_id} not found")
                return None
            if person_id:
                customer.person_id = person_id
            if store_id:
                customer.store_id = store_id
            if territory_id:
                customer.territory_id = territory_id
            if account_number:
                customer.account_number = account_number
            db.session.commit()
            logger.info(f"Updated customer: {customer}")
            return customer
        except Exception as e:
            logger.error(f"Error updating customer with ID {customer_id}: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def delete_customer(customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                logger.warning(f"Customer with ID {customer_id} not found")
                return False
            db.session.delete(customer)
            db.session.commit()
            logger.info(f"Deleted customer with ID {customer_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting customer with ID {customer_id}: {e}")
            db.session.rollback()
            return False
        