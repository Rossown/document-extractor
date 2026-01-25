from api.models import db, SalesOrderHeader, SalesOrderDetail
from config import logger

class SalesOrderService:
    @staticmethod
    def create_sales_order(header, details):
        try:
            order = SalesOrderHeader(**header)
            db.session.add(order)
            db.session.flush()
            order.sales_order_number = f"SO{order.id}"
            if len(details) > 0:
                order.sales_order_details = [SalesOrderDetail(**detail) for detail in details]
            db.session.commit()
            logger.info(f"Sales order {order.sales_order_number} created successfully.")
            return order
        except Exception as e:
            logger.error(f"Error creating sales order: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_sales_order_by_id(order_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return None
        return order
    
    @staticmethod
    def list_sales_orders():
        return SalesOrderHeader.query.limit(10).all()
    
    @staticmethod
    def update_sales_order(order_id, **kwargs):
        try:
            order = SalesOrderHeader.query.get(order_id)
            if not order:
                logger.warning(f"Sales order with ID {order_id} not found.")
                return False
            for key, value in kwargs.items():
                if not hasattr(order, key):
                    logger.warning(f"Sales order does not have attribute {key}. Skipping update for this field.")
                    continue
                setattr(order, key, value)
            db.session.commit()
            logger.info(f"Sales order {order.sales_order_number} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error updating sales order: {e}")
            db.session.rollback()
            raise
        
    @staticmethod
    def delete_sales_order(order_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return False
        db.session.delete(order)
        db.session.commit()
        logger.info(f"Sales order {order.sales_order_number} deleted successfully.")
        return True
    
    @staticmethod
    def add_sales_order_detail(order_id, detail):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return None
        try:
            order_detail = SalesOrderDetail(**detail)
            order_detail.sales_order_id = order.id
            db.session.add(order_detail)
            db.session.commit()
            logger.info(f"Sales order detail {order_detail.id} added to order {order.sales_order_number} successfully.")
            return order_detail
        except Exception as e:
            logger.error(f"Error adding sales order detail: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_sales_order_details(order_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return []
        return order.sales_order_details
    
    @staticmethod
    def get_sales_order_detail_by_id(order_id, detail_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return None
        for detail in order.sales_order_details:
            if detail.id == detail_id:
                return detail
        logger.warning(f"Sales order detail with ID {detail_id} not found in order {order_id}.")
        return None
    
    @staticmethod
    def update_sales_order_detail(order_id, detail_id, **kwargs):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return False
        detail = SalesOrderDetail.query.get(detail_id)
        if not detail:
            logger.warning(f"Sales order detail with ID {detail_id} not found.")
            return False
        try:
            for key, value in kwargs.items():
                if not hasattr(detail, key):
                    logger.warning(f"Sales order detail does not have attribute {key}. Skipping update for this field.")
                    continue
                setattr(detail, key, value)
            db.session.commit()
            logger.info(f"Sales order detail {detail.id} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error updating sales order detail: {e}")
            db.session.rollback()
            raise
    
    
    @staticmethod
    def delete_sales_order_detail(order_id, detail_id):
        order = SalesOrderHeader.query.get(order_id)
        if not order:
            logger.warning(f"Sales order with ID {order_id} not found.")
            return False
        detail = SalesOrderDetail.query.get(detail_id)
        if not detail:
            logger.warning(f"Sales order detail with ID {detail_id} not found.")
            return False
        try:
            db.session.delete(detail)
            db.session.commit()
            logger.info(f"Sales order detail {detail.id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting sales order detail: {e}")
            db.session.rollback()
            raise