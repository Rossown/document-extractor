from api.models import db, ProductData, ProductCategory, ProductSubCategory
from config import logger

class ProductService:

    @staticmethod
    def to_dict_with_relations(product):
        data = product.to_dict()
        # Add subcategory info
        subcat = ProductSubCategory.query.get(product.product_subcategory_id) if product.product_subcategory_id else None
        if subcat:
            data["subcategory"] = subcat.to_dict()
            # Add category info
            cat = ProductCategory.query.get(subcat.category_id) if subcat.category_id else None
            if cat:
                data["subcategory"]["category"] = cat.to_dict()
        return data
    
    # Category
    @staticmethod
    def create_category(data):
        try:
            category = ProductCategory(**data)
            db.session.add(category)
            db.session.commit()
            logger.info(f"ProductCategory {category.name} created successfully.")
            return category
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def get_category_by_id(category_id):
        category = ProductCategory.query.get(category_id)
        if not category:
            logger.warning(f"ProductCategory with ID {category_id} not found.")
            return None
        return category

    @staticmethod
    def list_categories():
        return ProductCategory.query.all()

    @staticmethod
    def update_category(category_id, **kwargs):
        try:
            category = ProductCategory.query.get(category_id)
            if not category:
                logger.warning(f"ProductCategory with ID {category_id} not found.")
                return False
            for key, value in kwargs.items():
                if not hasattr(category, key):
                    logger.warning(f"ProductCategory does not have attribute {key}. Skipping update for this field.")
                    continue
                setattr(category, key, value)
            db.session.commit()
            logger.info(f"ProductCategory {category.name} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def delete_category(category_id):
        category = ProductCategory.query.get(category_id)
        if not category:
            logger.warning(f"ProductCategory with ID {category_id} not found.")
            return False
        db.session.delete(category)
        db.session.commit()
        logger.info(f"ProductCategory {category.name} deleted successfully.")
        return True

    # SubCategory
    @staticmethod
    def create_subcategory(data):
        try:
            subcategory = ProductSubCategory(**data)
            db.session.add(subcategory)
            db.session.commit()
            logger.info(f"ProductSubCategory {subcategory.name} created successfully.")
            return subcategory
        except Exception as e:
            logger.error(f"Error creating subcategory: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def get_subcategory_by_id(subcategory_id):
        subcategory = ProductSubCategory.query.get(subcategory_id)
        if not subcategory:
            logger.warning(f"ProductSubCategory with ID {subcategory_id} not found.")
            return None
        return subcategory

    @staticmethod
    def list_subcategories():
        return ProductSubCategory.query.all()

    @staticmethod
    def update_subcategory(subcategory_id, **kwargs):
        try:
            subcategory = ProductSubCategory.query.get(subcategory_id)
            if not subcategory:
                logger.warning(f"ProductSubCategory with ID {subcategory_id} not found.")
                return False
            for key, value in kwargs.items():
                if not hasattr(subcategory, key):
                    logger.warning(f"ProductSubCategory does not have attribute {key}. Skipping update for this field.")
                    continue
                setattr(subcategory, key, value)
            db.session.commit()
            logger.info(f"ProductSubCategory {subcategory.name} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error updating subcategory: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def delete_subcategory(subcategory_id):
        subcategory = ProductSubCategory.query.get(subcategory_id)
        if not subcategory:
            logger.warning(f"ProductSubCategory with ID {subcategory_id} not found.")
            return False
        db.session.delete(subcategory)
        db.session.commit()
        logger.info(f"ProductSubCategory {subcategory.name} deleted successfully.")
        return True
        
    # Product
    @staticmethod
    def create_product(data):
        try:
            product = ProductData(**data)
            db.session.add(product)
            db.session.commit()
            logger.info(f"Product {product.product_name} created successfully.")
            return product
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def get_product_by_id(product_id):
        product = ProductData.query.get(product_id)
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            return None
        return ProductService.to_dict_with_relations(product)

    @staticmethod
    def list_products():
        products = ProductData.query.all()
        return [ProductService.to_dict_with_relations(p) for p in products]

    @staticmethod
    def update_product(product_id, **kwargs):
        try:
            product = ProductData.query.get(product_id)
            if not product:
                logger.warning(f"Product with ID {product_id} not found.")
                return False
            for key, value in kwargs.items():
                if not hasattr(product, key):
                    logger.warning(f"Product does not have attribute {key}. Skipping update for this field.")
                    continue
                setattr(product, key, value)
            db.session.commit()
            logger.info(f"Product {product.product_name} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error updating product: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def delete_product(product_id):
        product = ProductData.query.get(product_id)
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            return False
        db.session.delete(product)
        db.session.commit()
        logger.info(f"Product {product.product_name} deleted successfully.")
        return True
    