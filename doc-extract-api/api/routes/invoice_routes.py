from flask import Blueprint, request, jsonify
from services.ai_service import AIService
from services.document_service import DocumentService
from api.models import db, SalesOrderHeader
from utils import logger

invoice_bp = Blueprint('invoices', __name__)
ai_service = AIService()
document_service = DocumentService()

@invoice_bp.route('', methods=['POST'])
def create_invoice():
    logger.info(f"Received request to create invoice")
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        if not document_service.allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        document_text = None
        if file_ext in ['png', 'jpg', 'jpeg']:
            document_text = ai_service.extract_from_image(file)
            print(f"Extracted text from image: {document_text}")
        else:
            document_text = document_service.extract_text_from_file(file)
        
        response = ai_service.extract_invoice_data(document_text) # Json 
        
        # Order to create models in
        # ('StoreCustomers', Store),
        # ('IndividualCustomers', Person),
        # ('SalesTerritory', SalesTerritory),
        # ('Customers', Customer),
        # ('SalesOrderHeader', SalesOrderHeader),
        # ('ProductCategory', ProductCategory),
        # ('ProductSubCategory', ProductSubCategory),
        # ('Product', ProductData),
        # ('SalesOrderDetail', SalesOrderDetail),
        
        customers = AIService.map_customer(response) # either Store or Person
        
        logger.debug(f"Mapped customers: {customers}")


        return jsonify({"invoice_data": response}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500