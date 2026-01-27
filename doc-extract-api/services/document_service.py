import base64
import os
from werkzeug.utils import secure_filename
from config import logger, Config
import PyPDF2
from PIL import Image


class DocumentService:
    """Service for handling document uploads and processing"""
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'bmp', 'gif'}
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in DocumentService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_upload_file(file):
        """
        Save uploaded file to disk
        
        Args:
            file: Flask file object from request
            
        Returns:
            str: Path to saved file
            
        Raises:
            Exception: If file is invalid or save fails
        """
        try:
            if not file or file.filename == '':
                raise Exception("No file selected")
            
            if not DocumentService.allowed_file(file.filename):
                raise Exception(f"File type not allowed. Allowed types: {', '.join(DocumentService.ALLOWED_EXTENSIONS)}")
            
            if file.content_length > Config.MAX_FILE_SIZE:
                raise Exception(f"File too large. Max size: {Config.MAX_FILE_SIZE / 1024 / 1024}MB")
            
            # Create upload folder if it doesn't exist
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            # Save file with secure filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            file.save(filepath)
            logger.info(f"File saved: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise
    
    @staticmethod
    def extract_text_from_file(file):
        """
        Extract text from document file
        
        Args:
            file: Flask file object from request
            
        Returns:
            str: Extracted text from document
            
        Raises:
            Exception: If extraction fails
        """
        try:
            filepath = DocumentService.save_upload_file(file)
            file_ext = filepath.rsplit('.', 1)[1].lower()
            
            if file_ext == 'txt':
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                logger.info(f"Text extracted from {filepath}")
                return text
            
            elif file_ext == 'pdf':
                text = ""
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                
                logger.info(f"Text extracted from PDF: {filepath}")
                
                return text
            
            elif file_ext in {'png', 'jpg', 'jpeg', 'bmp', 'gif'}:
                pass
            
            else:
                raise Exception(f"Unsupported file type: {file_ext}")
        
        except Exception as e:
            logger.error(f"Error extracting text from file: {e}")
            raise
    
    @staticmethod
    def delete_file(filepath):
        """Delete uploaded file after processing"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"File deleted: {filepath}")
        except Exception as e:
            logger.error(f"Error deleting file {filepath}: {e}")
