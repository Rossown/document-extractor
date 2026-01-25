from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


# Initialize the database
db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class ProductData(BaseModel):
    __tablename__ = 'product_data'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_number = db.Column(db.String(100), unique=True)
    make_flag = db.Column(db.Boolean, default=False)
    finished_goods_flag = db.Column(db.Boolean, default=False)
    color = db.Column(db.String(50))
    standard_cost = db.Column(db.Float)
    list_price = db.Column(db.Float)
    size = db.Column(db.String(50))
    product_line = db.Column(db.String(50))
    class_field = db.Column(db.String(50))
    style = db.Column(db.String(50))
    product_subcategory_id = db.Column(db.Integer, db.ForeignKey('product_subcategory.id'))
    product_model_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<ProductData {self.product_number}>'
    
class ProductCategory(BaseModel):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<ProductCategory {self.name}>'
    
class ProductSubCategory(BaseModel):
    __tablename__ = 'product_subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category = db.relationship('ProductCategory', backref='subcategories')

    def __repr__(self):
        return f'<ProductSubCategory {self.name}>'

# Done
class SalesOrderHeader(BaseModel):
    __tablename__ = 'sales_order_header'
    id = db.Column(db.Integer, primary_key=True)
    revision_number = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime)
    ship_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    online_order_flag = db.Column(db.Boolean, default=False)
    sales_order_number = db.Column(db.String(25), unique=True)
    purchase_order_number = db.Column(db.String(25))
    account_number = db.Column(db.String(25))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    sales_person_id = db.Column(db.String(50))
    territory_id = db.Column(db.Integer, db.ForeignKey('sales_territory.id'))
    bill_to_address_id = db.Column(db.Integer)
    ship_to_address_id = db.Column(db.Integer)
    ship_method_id = db.Column(db.Integer)
    credit_card_id = db.Column(db.String(15))
    credit_card_approval_code = db.Column(db.String(25))
    currency_rate_id = db.Column(db.Integer)
    sub_total = db.Column(db.Float)
    tax_amt = db.Column(db.Float)
    freight = db.Column(db.Float)
    total_due = db.Column(db.Float)
    
    sales_order_details = db.relationship('SalesOrderDetail', backref='sales_order', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<SalesOrderHeader {self.id}>'

# Done    
class SalesOrderDetail(BaseModel):
    __tablename__ = 'sales_order_detail'
    id = db.Column(db.Integer, primary_key=True)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_order_header.id'))
    carrier_tracking_number = db.Column(db.String(25))
    order_qty = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product_data.id'))
    special_offer_id = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    unit_price_discount = db.Column(db.Float)
    line_total = db.Column(db.Float)
    
    def __repr__(self):
        return f'<SalesOrderDetail {self.id} for Order {self.sales_order_id}>'
    
# Done
class SalesTerritory(BaseModel):
    __tablename__ = 'sales_territory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    country_region_code = db.Column(db.String(10))
    group = db.Column(db.String(50))

    def __repr__(self):
        return f'<SalesTerritory {self.name}>'

# Done    
class Customer(BaseModel):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    territory_id = db.Column(db.Integer, db.ForeignKey('sales_territory.id'))
    account_number = db.Column(db.String(25), unique=True)
    
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'
    
# Done
class Person(BaseModel):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address_type = db.Column(db.String(25))
    address_line1 = db.Column(db.String(100))
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state_province = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    country_region = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

# Done    
class Store(BaseModel):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address_type = db.Column(db.String(25))
    address_line1 = db.Column(db.String(100))
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state_province = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    country_region = db.Column(db.String(50))
    def __repr__(self):
        return f'<Store {self.name}>'