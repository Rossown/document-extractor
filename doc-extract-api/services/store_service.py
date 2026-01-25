from api.models import db, Store
from api.errors import NotFoundError, BadRequestError
from config import Config, logger


class StoreService:
    @staticmethod
    def create_store(name, address_data):
        """Create a new store"""
        if not name or not name.strip():
            raise BadRequestError("Store name is required")
        store = Store(
            name=name,
            **address_data
        )
        db.session.add(store)
        db.session.commit()
        logger.info(f"Store created: {store.name} (ID: {store.id})")
        return store
    
    @staticmethod
    def get_store(store_id):
        """Get store by ID"""
        store = Store.query.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            raise NotFoundError(f"Store not found: {store_id}")
        return store
    
    @staticmethod
    def list_stores():
        """Get all stores"""
        stores = Store.query.all()
        if not stores:
            raise NotFoundError("No stores found")
        logger.info(f"Retrieved {len(stores)} stores")
        return stores

    
    @staticmethod
    def update_store(store_id, **kwargs):
        """Update store by ID"""
        store = Store.query.get(store_id)
        if not store:
            raise NotFoundError(f"Store not found: {store_id}")

        updated = False
        for key, value in kwargs.items():
            if key in Config.STORE_ALLOWED_FIELDS:
                setattr(store, key, value)
                updated = True

        if not updated:
            raise BadRequestError("No valid fields provided for update")

        db.session.commit()
        logger.info(f"Store updated: ID {store_id}")
        return store

    
    @staticmethod
    def delete_store(store_id):
        """Delete store by ID"""
        store = Store.query.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            raise NotFoundError(f"Store not found: {store_id}")
        db.session.delete(store)
        db.session.commit()
        logger.info(f"Store deleted: ID {store_id}")