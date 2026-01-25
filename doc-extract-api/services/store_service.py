from api.models import db, Store
from config import logger


class StoreService:
    @staticmethod
    def create_store(name, address_data):
        """Create a new store"""
        try:
            store = Store(
                name=name,
                **address_data
            )
            db.session.add(store)
            db.session.commit()
            logger.info(f"Store created: {store.name} (ID: {store.id})")
            return store
        except Exception as e:
            logger.error(f"Error creating store: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_store(store_id):
        """Get store by ID"""
        try:
            store = Store.query.get(store_id)
            if not store:
                logger.warning(f"Store not found: {store_id}")
                return None
            return store
        except Exception as e:
            logger.error(f"Error getting store: {e}")
            raise
    
    @staticmethod
    def list_stores():
        """Get all stores"""
        try:
            stores = Store.query.all()
            logger.info(f"Retrieved {len(stores)} stores")
            return stores
        except Exception as e:
            logger.error(f"Error listing stores: {e}")
            raise
    
    @staticmethod
    def update_store(store_id, **kwargs):
        """Update store by ID"""
        try:
            store = Store.query.get(store_id)
            if not store:
                logger.warning(f"Store not found: {store_id}")
                return None
            
            for key, value in kwargs.items():
                if hasattr(store, key):
                    setattr(store, key, value)
            
            db.session.commit()
            logger.info(f"Store updated: {store.name} (ID: {store_id})")
            return store
        except Exception as e:
            logger.error(f"Error updating store: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def delete_store(store_id):
        """Delete store by ID"""
        try:
            store = Store.query.get(store_id)
            if not store:
                logger.warning(f"Store not found: {store_id}")
                return False
            
            db.session.delete(store)
            db.session.commit()
            logger.info(f"Store deleted: ID {store_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting store: {e}")
            db.session.rollback()
            raise