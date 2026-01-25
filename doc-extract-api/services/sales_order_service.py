from api.models import db, SalesOrderHeader, SalesOrderDetail
from api.errors import NotFoundError, BadRequestError
from config import Config, logger
from utils import paginate

class SalesOrderService:
    @staticmethod
    def create_sales_order(header, details):
        if not header:
            raise BadRequestError("Sales order header is required.")
        
        for key in Config.SALES_ORDER_DETAIL_ALLOWED_FIELDS:
            if key not in header.keys():
                raise BadRequestError(f"Missing required field in sales order header: {key}")
            
        order = SalesOrderHeader(**header)
        db.session.add(order)
        db.session.flush()
        order.sales_order_number = f"SO{order.id}"
        if len(details) > 0:
            
            for detail in details:
                for key in Config.SALES_ORDER_DETAIL_ALLOWED_FIELDS:
                    if key not in detail.keys():
                        raise BadRequestError(f"Missing required field in sales order detail: {key}")
            order.sales_order_details = [SalesOrderDetail(**detail) for detail in details]
        db.session.commit()
        logger.info(f"Sales order {order.sales_order_number} created successfully.")
        return order
    
    @staticmethod
    def get_sales_order_by_id(order_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")
        return order
    
    @staticmethod
    def list_sales_orders(cursor_id=None, limit=20):
        query = SalesOrderHeader.query
        if not query:
            raise NotFoundError("No sales orders found.")
        return paginate(query, cursor_id=cursor_id, limit=limit)
    
    @staticmethod
    def update_sales_order(order_id, **kwargs):
        for key in Config.SALES_ORDER_HEADER_ALLOWED_FIELDS:
            if key not in kwargs.keys():
                raise BadRequestError(f"Missing required field in sales order header: {key}")
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")
        updated = False
        for key, value in kwargs.items():
            if not hasattr(order, key):
                logger.warning(f"Sales order does not have attribute {key}. Skipping update for this field.")
                continue
            setattr(order, key, value)
            updated = True
        if not updated:
            raise BadRequestError(f"No valid fields provided for update on sales order {order.sales_order_number}.")
        db.session.commit()
        logger.info(f"Sales order {order.sales_order_number} updated successfully.")
        return order
        
    @staticmethod
    def delete_sales_order(order_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")
        db.session.delete(order)
        db.session.commit()
        logger.info(f"Sales order {order.sales_order_number} deleted successfully.")
    
    @staticmethod
    def add_sales_order_detail(order_id, detail):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")

        for key in Config.SALES_ORDER_DETAIL_ALLOWED_FIELDS:
            if key not in detail.keys():
                raise BadRequestError(f"Missing required field in sales order detail: {key}")
        order_detail = SalesOrderDetail(**detail)
        order_detail.sales_order_id = order.id
        db.session.add(order_detail)
        db.session.commit()
        logger.info(f"Sales order detail {order_detail.id} added to order {order.sales_order_number} successfully.")
        return order_detail

    
    @staticmethod
    def get_sales_order_details(order_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")
        return order.sales_order_details
    
    @staticmethod
    def get_sales_order_detail_by_id(order_id, detail_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")
        for detail in order.sales_order_details:
            if detail.id == detail_id:
                return detail
        logger.warning(f"Sales order detail with ID {detail_id} not found in order {order_id}.")
        raise NotFoundError(f"Sales order detail with ID {detail_id} not found in order {order_id}.")
    
    @staticmethod
    def update_sales_order_detail(order_id, detail_id, **kwargs):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")  
        detail = SalesOrderDetail.query.get(detail_id)
        if not detail:
            logger.warning(f"Sales order detail with ID {detail_id} not found.")
            raise NotFoundError(f"Sales order detail with ID {detail_id} not found.")
        updated = False
        for key, value in kwargs.items():
            if not hasattr(detail, key):
                logger.warning(f"Sales order detail does not have attribute {key}. Skipping update for this field.")
                continue
            setattr(detail, key, value)
            updated = True
        if not updated:
            raise BadRequestError(f"No valid fields provided for update on sales order detail {detail.id}.")
        db.session.commit()
        logger.info(f"Sales order detail {detail.id} updated successfully.")
        return order
    
    
    @staticmethod
    def delete_sales_order_detail(order_id, detail_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            raise NotFoundError(f"Sales order with ID {order_id} not found.")
        detail = SalesOrderDetail.query.get(detail_id)
        if not detail:
            logger.warning(f"Sales order detail with ID {detail_id} not found.")
            raise NotFoundError(f"Sales order detail with ID {detail_id} not found.")
        db.session.delete(detail)
        db.session.commit()
        logger.info(f"Sales order detail {detail.id} deleted successfully.")