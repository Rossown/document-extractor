from api.models import db, ProductData, ProductCategory, ProductSubCategory
from api.errors import NotFoundError, BadRequestError
from config import Config, logger
from utils import paginate
from sqlalchemy.orm import selectinload

class ProductService:

    @staticmethod
    def to_dict_with_relations(product):
        """
        Converts a ProductData instance to dict, including nested subcategory & category.
        """
        data = product.to_dict()

        if hasattr(product, "subcategory") and product.subcategory:
            subcat = product.subcategory
            data["subcategory"] = subcat.to_dict()

            if hasattr(subcat, "category") and subcat.category:
                data["subcategory"]["category"] = subcat.category.to_dict()

        return data
    
    # Category
    @staticmethod
    def create_category(data):
        if not data.get("name"):
            raise BadRequestError("Category name is required")
        category = ProductCategory(name=data["name"])
        db.session.add(category)
        db.session.commit()
        logger.info(f"ProductCategory {category.name} created successfully.")
        return category

    @staticmethod
    def get_category_by_id(category_id):
        category = ProductCategory.query.get(category_id)
        if not category:
            logger.warning(f"ProductCategory with ID {category_id} not found.")
            raise NotFoundError(f"ProductCategory with ID {category_id} not found.")
        return category

    @staticmethod
    def list_categories(cursor_id=None, limit=Config.PAGINATION_DEFAULT_LIMIT):
        categories = ProductCategory.query
        if not categories:
            logger.warning("No ProductCategories found.")
            raise NotFoundError("No ProductCategories found")
        return paginate(categories, order_by=ProductCategory.id, cursor_id=cursor_id, limit=limit)

    @staticmethod
    def update_category(category_id, **kwargs):
        category = ProductCategory.query.get(category_id)
        if not category:
            logger.warning(f"ProductCategory with ID {category_id} not found.")
            raise NotFoundError(f"ProductCategory with ID {category_id} not found.")
        updated = False
        for key, value in kwargs.items():
            if not hasattr(category, key):
                logger.warning(f"ProductCategory does not have attribute {key}. Skipping update for this field.")
                continue
            setattr(category, key, value)
            updated = True
        if not updated:
            logger.warning(f"No valid fields provided for update on ProductCategory with ID {category_id}.")
            raise BadRequestError(f"No valid fields provided for update on ProductCategory with ID {category_id}.")
        db.session.commit()
        logger.info(f"ProductCategory {category.name} updated successfully.")
        return category

    @staticmethod
    def delete_category(category_id):
        category = ProductCategory.query.get(category_id)
        if not category:
            logger.warning(f"ProductCategory with ID {category_id} not found.")
            raise NotFoundError(f"ProductCategory with ID {category_id} not found.")
        db.session.delete(category)
        db.session.commit()
        logger.info(f"ProductCategory {category.name} deleted successfully.")

    # SubCategory
    @staticmethod
    def create_subcategory(data):
        if not data.get("name"):
            raise BadRequestError("Subcategory name is required")
        if not data.get("category_id"):
            raise BadRequestError("Category ID is required for subcategory")
        category = ProductCategory.query.get(data["category_id"])
        if not category:
            raise NotFoundError(f"ProductCategory with ID {data['category_id']} not found.")
        subcategory = ProductSubCategory(**data)
        db.session.add(subcategory)
        db.session.commit()
        logger.info(f"ProductSubCategory {subcategory.name} created successfully.")
        return subcategory

    @staticmethod
    def get_subcategory_by_id(subcategory_id):
        subcategory = ProductSubCategory.query.get(subcategory_id)
        if not subcategory:
            logger.warning(f"ProductSubCategory with ID {subcategory_id} not found.")
            raise NotFoundError(f"ProductSubCategory with ID {subcategory_id} not found.")
        return subcategory

    @staticmethod
    def list_subcategories(cursor_id=None, limit=Config.PAGINATION_DEFAULT_LIMIT):
        subcategories = ProductSubCategory.query.all()
        if not subcategories:
            logger.warning("No ProductSubCategories found.")
            raise NotFoundError("No ProductSubCategories found")
        return paginate(subcategories, order_by=ProductSubCategory.id, cursor_id=cursor_id, limit=limit)

    @staticmethod
    def update_subcategory(subcategory_id, **kwargs):
        subcategory = ProductSubCategory.query.get(subcategory_id)
        if not subcategory:
            logger.warning(f"ProductSubCategory with ID {subcategory_id} not found.")
            raise NotFoundError(f"ProductSubCategory with ID {subcategory_id} not found.")
        
        updated = False
        for key, value in kwargs.items():
            if not hasattr(subcategory, key):
                logger.warning(f"ProductSubCategory does not have attribute {key}. Skipping update for this field.")
                continue
            setattr(subcategory, key, value)
            updated = True
        if not updated:
            logger.warning(f"No valid fields provided for update on ProductSubCategory with ID {subcategory_id}.")
            raise BadRequestError(f"No valid fields provided for update on ProductSubCategory with ID {subcategory_id}.")
        db.session.commit()
        logger.info(f"ProductSubCategory {subcategory.name} updated successfully.")
        return subcategory


    @staticmethod
    def delete_subcategory(subcategory_id):
        subcategory = ProductSubCategory.query.get(subcategory_id)
        if not subcategory:
            logger.warning(f"ProductSubCategory with ID {subcategory_id} not found.")
            raise NotFoundError(f"ProductSubCategory with ID {subcategory_id} not found.")
        db.session.delete(subcategory)
        db.session.commit()
        logger.info(f"ProductSubCategory {subcategory.name} deleted successfully.")
        
    # Product
    @staticmethod
    def create_product(data):
        for allowed_field in Config.PRODUCT_ALLOWED_FIELDS:
            if allowed_field not in data:
                logger.warning(f"Field {allowed_field} is missing in input data. Setting it to None.")
                raise BadRequestError(f"Field {allowed_field} is required for creating a Product.")
        subcategory = ProductSubCategory.query.get(data.get("product_subcategory_id"))
        if not subcategory:
            logger.warning(f"ProductSubCategory with ID {data.get('product_subcategory_id')} not found.")
            raise NotFoundError(f"ProductSubCategory with ID {data.get('product_subcategory_id')} not found.")
        product = ProductData(**data)
        db.session.add(product)
        db.session.commit()
        logger.info(f"Product {product.product_name} created successfully.")
        return product

    @staticmethod
    def get_product_by_id(product_id):
        product = ProductData.query.get(product_id)
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            raise NotFoundError(f"Product with ID {product_id} not found.")
        return ProductService.to_dict_with_relations(product)

    @staticmethod
    def list_products(cursor_id=None, limit=Config.PAGINATION_DEFAULT_LIMIT):
        query = ProductData.query.options(
            selectinload(ProductData.subcategory).selectinload(ProductSubCategory.category)
        )
        if not query:
            raise NotFoundError("No products found.")
        paginated = paginate(query, order_by=ProductData.id, cursor_id=cursor_id, limit=limit)
        items_with_relations = [ProductService.to_dict_with_relations(p) for p in query.filter(ProductData.id.in_([item["id"] for item in paginated["items"]])).all()]
        paginated["items"] = items_with_relations
        return paginated

    @staticmethod
    def update_product(product_id, **kwargs):
        product = ProductData.query.get(product_id)
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            raise NotFoundError(f"Product with ID {product_id} not found.")
        
        updated = False
        for key, value in kwargs.items():
            if key in Config.PRODUCT_ALLOWED_FIELDS:
                setattr(product, key, value)
                updated = True
        if not updated:
            logger.warning(f"No valid fields provided for update on Product with ID {product_id}.")
            raise BadRequestError(f"No valid fields provided for update on Product with ID {product_id}.")
        db.session.commit()
        logger.info(f"Product {product.product_name} updated successfully.")
        return product

    @staticmethod
    def delete_product(product_id):
        product = ProductData.query.get(product_id)
        if not product:
            logger.warning(f"Product with ID {product_id} not found.")
            raise NotFoundError(f"Product with ID {product_id} not found.")
        db.session.delete(product)
        db.session.commit()
        logger.info(f"Product {product.product_name} deleted successfully.")