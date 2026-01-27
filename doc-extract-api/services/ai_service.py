import json
import base64
from openai import OpenAI
from config import logger, Config
from api.models import SalesOrderHeader, SalesOrderDetail, ProductData, Customer, Person, Store, db

class AIService:
    """Service for interacting with OpenAI API"""
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    model = Config.OPENAI_MODEL
    max_tokens = Config.OPENAI_MAX_TOKENS
    
    @staticmethod
    def extract_from_image(file):
        img_bytes = file.read()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        data_url = f"data:image/png;base64,{img_b64}"
        
        response = AIService.client.responses.create(
            model=AIService.model,
            temperature=0.2,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Extract all text from this image. If no text is found, respond with 'There is no visible text in this image.'"},
                        {"type": "input_image", "image_url": data_url}
                    ],
                }
            ]
        )
        extracted_text = response.output_text
        return extracted_text
    
    @staticmethod
    def get_invoice_extraction_prompt(document_text):
        """Generate a prompt for invoice extraction"""
        return f"""
        You are an expert financial document parser.

        Extract ALL possible structured information from the invoice below.
        Return ONLY valid JSON that EXACTLY matches this schema.
        If a field is missing, return null.
        If a value is inferred, do so conservatively.
        Do NOT fabricate IDs.
        Do NOT include commentary or explanations.
        Images are base64 encoded
        If no invoice data is found, return an empty JSON object without any fields.

        JSON Schema:
        {{
            "sales_order_header": {{
                "sales_order_number": "string",
                "revision_number": 1,
                "order_date": "YYYY-MM-DD",
                "due_date": "YYYY-MM-DD",
                "ship_date": "YYYY-MM-DD",
                "status": 1,
                "online_order_flag": true,
                "purchase_order_number": "string",
                "account_number": "string",
                "customer": {{
                    "type": "person | store | unknown",
                    "customer_id": null,
                    "person": {{
                        "first_name": "string",
                        "middle_name": "string",
                        "last_name": "string",
                        "address_line1": "string",
                        "address_line2": "string",
                        "city": "string",
                        "state_province": "string",
                        "postal_code": "string",
                        "country_region": "string"
                    }},
                    "store": {{
                        "name": "string",
                        "address_line1": "string",
                        "address_line2": "string",
                        "city": "string",
                        "state_province": "string",
                        "postal_code": "string",
                        "country_region": "string"
                    }}
                }},
                "territory_id": null,
                "bill_to_address_id": null,
                "ship_to_address_id": null,
                "currency_rate_id": null,
                "sub_total": 0.0,
                "tax_amt": 0.0,
                "freight": 0.0,
                "total_due": 0.0
            }},
            "sales_order_details": [
                {{
                    "line_number": 1,
                    "product": {{
                        "product_name": "string",
                        "product_number": "string",
                        "make_flag": true,
                        "finished_goods_flag": true,
                        "color": "string",
                        "size": "string",
                        "product_line": "string",
                        "class_field": "string",
                        "style": "string",
                        "product_subcategory_id": null,
                        "product_model_id": null
                    }},
                    "order_qty": 0,
                    "unit_price": 0.0,
                    "unit_price_discount": 0.0,
                    "line_total": 0.0,
                    "carrier_tracking_number": "string",
                    "special_offer_id": null
                }}
            ],
            "confidence": {{
                "overall": 0.0,
                "fields": {{
                    "sales_order_number": 0.0,
                    "total_due": 0.0,
                    "customer_name": 0.0
                }}
            }}
        }}

        Invoice text:
        {document_text}
        """
    
    @staticmethod
    def extract_invoice_data(document_text):
        """
        Send document text to OpenAI and extract invoice information
        
        Args:
            document_text (str): The extracted text from the invoice document
            
        Returns:
            dict: Extracted invoice data as JSON
            
        Raises:
            Exception: If OpenAI API call fails
        """
        try:
            logger.info("Sending invoice to OpenAI for analysis")
            
            prompt = AIService.get_invoice_extraction_prompt(document_text)
            
            response = AIService.client.chat.completions.create(
                model=AIService.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You extract structured invoice data and return only valid JSON. If you cannot find any invoice data, return an empty JSON object."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_completion_tokens=AIService.max_tokens,
                response_format={"type": "json_object"}  # <-- IMPORTANT
            )
            
            # Extract the response content
            response_text = response.choices[0].message.content.strip()
            if not response_text or response_text == "":
                raise Exception("Empty response from OpenAI")
            
            logger.debug(f"OpenAI response: {response_text}")
            
            # Parse JSON response
            extracted_data = json.loads(response_text)
            logger.info("Invoice data extracted successfully")
            
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise Exception(f"Invalid JSON response from OpenAI: {e}")
        except Exception as e:
            logger.error(f"Error during invoice extraction: {e}")
            raise Exception(f"Failed to extract invoice data: {e}")
        
    @staticmethod
    def map_territory(territory_payload: dict):
        """
        Create or resolve a SalesTerritory object from AI JSON.
        Returns the SalesTerritory.id to be used in other models.
        """
        from api.models import SalesTerritory
        if not territory_payload:
            return None
        territory_id = territory_payload.get("id")
        name = territory_payload.get("name")
        country_region_code = territory_payload.get("country_region_code")
        group = territory_payload.get("group")
        territory = None
        if territory_id:
            territory = SalesTerritory.query.get(territory_id)
        if not territory and name:
            territory = SalesTerritory.query.filter_by(name=name).first()
        if not territory and name:
            territory = SalesTerritory(name=name, country_region_code=country_region_code, group=group)
            db.session.add(territory)
            db.session.flush()
        return getattr(territory, "id", None)

    @staticmethod
    def map_product(product_payload: dict):
        """
        Create or resolve a ProductData object from AI JSON.
        Returns the ProductData.id to be used in SalesOrderDetail.
        """
        from api.models import ProductData, ProductCategory, ProductSubCategory
        if not product_payload:
            return None
        product_number = product_payload.get("product_number")
        product = None
        if product_number:
            product = ProductData.query.filter_by(product_number=product_number).first()
        if not product:
            # Handle category/subcategory creation if present
            category_obj = None
            if "category" in product_payload and product_payload["category"]:
                cat = product_payload["category"]
                category_obj = ProductCategory.query.filter_by(name=cat.get("name")).first()
                if not category_obj and cat.get("name"):
                    category_obj = ProductCategory(name=cat["name"])
                    db.session.add(category_obj)
                    db.session.flush()
            subcat_obj = None
            if "subcategory" in product_payload and product_payload["subcategory"]:
                subcat = product_payload["subcategory"]
                subcat_obj = ProductSubCategory.query.filter_by(name=subcat.get("name")).first()
                if not subcat_obj and subcat.get("name"):
                    subcat_obj = ProductSubCategory(name=subcat["name"], category_id=getattr(category_obj, "id", None))
                    db.session.add(subcat_obj)
                    db.session.flush()
            prod_fields = {k: v for k, v in product_payload.items() if v is not None and k not in ["category", "subcategory"]}
            if subcat_obj:
                prod_fields["product_subcategory_id"] = subcat_obj.id
            product = ProductData(**prod_fields)
            db.session.add(product)
            db.session.flush()
        return getattr(product, "id", None)
        
    @staticmethod
    def map_sales_order_header(extracted: dict) -> SalesOrderHeader:
        soh_data = extracted["sales_order_header"]
        customer_data = soh_data.get("customer", {})

        return SalesOrderHeader(
            sales_order_number=soh_data.get("sales_order_number"),
            revision_number=soh_data.get("revision_number"),
            order_date=soh_data.get("order_date"),
            due_date=soh_data.get("due_date"),
            ship_date=soh_data.get("ship_date"),
            status=soh_data.get("status"),
            online_order_flag=soh_data.get("online_order_flag", False),
            purchase_order_number=soh_data.get("purchase_order_number"),
            account_number=soh_data.get("account_number"),
            customer_id=customer_data.get("customer_id"),
            territory_id=soh_data.get("territory_id"),
            bill_to_address_id=soh_data.get("bill_to_address_id"),
            ship_to_address_id=soh_data.get("ship_to_address_id"),
            currency_rate_id=soh_data.get("currency_rate_id"),
            sub_total=soh_data.get("sub_total"),
            tax_amt=soh_data.get("tax_amt"),
            freight=soh_data.get("freight"),
            total_due=soh_data.get("total_due")
        )

        
    @staticmethod
    def map_sales_order_details(extracted: dict, sales_order_id: int) -> list[SalesOrderDetail]:
        details = []
        for item in extracted.get("sales_order_details", []):
            product_payload = item.get("product", {})
            product_id = AIService.resolve_product_id(product_payload)

            details.append(
                SalesOrderDetail(
                    sales_order_id=sales_order_id,
                    order_qty=item.get("order_qty", 0),
                    unit_price=item.get("unit_price", 0.0),
                    unit_price_discount=item.get("unit_price_discount", 0.0),
                    line_total=item.get("line_total", 0.0),
                    product_id=product_id,
                    carrier_tracking_number=item.get("carrier_tracking_number"),
                    special_offer_id=item.get("special_offer_id")
                )
            )
        return details

    @staticmethod
    def resolve_product_id(product_payload: dict) -> int | None:
        """
        Try to find a matching product in the database.
        """
        if not product_payload:
            return None

        # Exact match by product_number
        product_number = product_payload.get("product_number")
        if product_number:
            product = ProductData.query.filter_by(product_number=product_number).first()
            if product:
                return product.id


        return None

    @staticmethod
    def requires_review(extracted: dict) -> bool:
        return extracted["confidence"]["overall"] < 0.85
    
    @staticmethod
    def map_customer(customer_payload: dict) -> int | None:
        """
        Create or resolve a Customer object from AI JSON.
        Returns the Customer.id to be used in SalesOrderHeader.
        """
        if not customer_payload:
            return None

        cust_type = customer_payload.get("type")
        account_number = customer_payload.get("account_number")
        territory_id = customer_payload.get("territory_id")

        # Try to find existing customer by account_number
        if account_number:
            customer = Customer.query.filter_by(account_number=account_number).first()
            if customer:
                return customer.id

        if cust_type == "person":
            person_data = customer_payload.get("person", {})
            # Try to find existing person by name (and optionally address)
            person = None
            if person_data.get("first_name") and person_data.get("last_name"):
                person = Person.query.filter_by(
                    first_name=person_data.get("first_name"),
                    last_name=person_data.get("last_name")
                ).first()
            if not person:
                person = Person(
                    first_name=person_data.get("first_name"),
                    middle_name=person_data.get("middle_name"),
                    last_name=person_data.get("last_name"),
                    address_line1=person_data.get("address_line1"),
                    address_line2=person_data.get("address_line2"),
                    city=person_data.get("city"),
                    state_province=person_data.get("state_province"),
                    postal_code=person_data.get("postal_code"),
                    country_region=person_data.get("country_region")
                )
                db.session.add(person)
                db.session.flush()

            customer = Customer(
                person_id=person.business_entity_id,
                account_number=account_number,
                territory_id=territory_id
            )
            db.session.add(customer)
            db.session.flush()
            return customer.id

        elif cust_type == "store":
            store_data = customer_payload.get("store", {})
            store = None
            if store_data.get("name"):
                store = Store.query.filter_by(name=store_data.get("name")).first()
            if not store:
                store = Store(
                    name=store_data.get("name"),
                    address_line1=store_data.get("address_line1"),
                    address_line2=store_data.get("address_line2"),
                    city=store_data.get("city"),
                    state_province=store_data.get("state_province"),
                    postal_code=store_data.get("postal_code"),
                    country_region=store_data.get("country_region")
                )
                db.session.add(store)
                db.session.flush()

            customer = Customer(
                store_id=store.business_entity_id,
                account_number=account_number,
                territory_id=territory_id
            )
            db.session.add(customer)
            db.session.flush()
            return customer.id

        # For unknown or missing type, return None
        return None
    
    

    @staticmethod
    def save_extracted_invoice(extracted: dict):
        # 1. Store/Person/Customer
        customer_id = AIService.map_customer(extracted["sales_order_header"].get("customer"))
        extracted["sales_order_header"]["customer"]["customer_id"] = customer_id

        # 2. SalesTerritory
        territory_payload = extracted["sales_order_header"].get("territory")
        if territory_payload:
            territory_id = AIService.map_territory(territory_payload)
            extracted["sales_order_header"]["territory_id"] = territory_id

        # 3. Product mapping for each detail
        for detail in extracted.get("sales_order_details", []):
            product_data = detail.get("product")
            if product_data and any(product_data.values()):
                product_id = AIService.map_product(product_data)
                detail["product_id"] = product_id

        # 4. SalesOrderHeader (uses updated payload)
        order = AIService.map_sales_order_header(extracted)
        db.session.add(order)
        db.session.flush()  # get order.id

        # 5. SalesOrderDetails (uses updated details)
        details = AIService.map_sales_order_details(extracted, order.id)
        db.session.add_all(details)

        db.session.commit()
        return order.id
