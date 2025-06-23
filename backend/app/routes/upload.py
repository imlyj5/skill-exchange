import os
import uuid
from datetime import datetime
from io import BytesIO
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import magic
from ..db import db
from ..models.user import User
from .route_utilities import validate_model
from ..config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

upload_bp = Blueprint("upload_bp", __name__, url_prefix="/upload")

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_file(file):
    """Validate that the uploaded file is actually an image"""
    if not file:
        return False, "No file provided"
    
    if file.filename == "":
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "File type not allowed. Please upload PNG, JPG, or JPEG"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large"
    
    # Validate file content using magic numbers
    # Reads first 2048 bytes (enough to detect file type)
    try:
        file_content = file.read(2048)
        file.seek(0)  # Reset file pointer to the beginning
        mime_type = magic.from_buffer(file_content, mime=True)  # Get the MIME type of the file
        
        if not mime_type.startswith("image/"):
            return False, "File is not a valid image"
        
        return True, "File is valid"
    except Exception as e:
        return False, f"Error validating file: {str(e)}"

def get_upload_folder():
    """Get the upload folder path"""
    return os.path.join(current_app.root_path, "..", "uploads")

def get_profile_images_folder():
    """Get the profile images folder path"""
    return os.path.join(get_upload_folder(), "profile_images")

def generate_unique_filename(user_id, original_filename):
    """Generate a unique filename for profile images"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    secure_original_filename = secure_filename(original_filename or "image")
    file_extension = secure_original_filename.rsplit(".", 1)[1].lower() if "." in secure_original_filename else "jpg"
    return f"profile_{user_id}_{timestamp}_{unique_id}.{file_extension}"

def process_and_save_image(file, file_path):
    """Process and save an image with resizing and optimization"""
    # At this point, the file object has been read to:
    # validate_image_file() read 2048 bytes for magic number check
    # file.seek(0) reset the position to the beginning of the file
    
    # But we need to read the entire file content for Python Imaging Library
    file_content = file.read()  # Read all remaining bytes
    file_stream = BytesIO(file_content)  # Create new stream from content
    
    # Open image with Pillow for processing
    # PIL's Image.open() expects file-like object with read() method
    # BytesIO gives us a clean, fresh file-like object
    image = Image.open(file_stream)
    
    # Convert to RGB if necessary (for JPEG compatibility)
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGB")
    
    # Resize image if it's too large
    max_size = (800, 800)
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)  # Resize image to max size
    
    # Save the processed image
    image.save(file_path, quality=85, optimize=True)

def update_user_image_url(user, image_url):
    """Update user's image_url in database"""
    user.image_url = image_url
    db.session.commit()

def delete_file_from_path(file_path):
    """Delete a file if it exists"""
    if os.path.exists(file_path):
        os.remove(file_path)

@upload_bp.get("/uploads/<path:filename>")
def serve_uploaded_file(filename):
    """Get uploaded files from the upload folder"""
    return send_from_directory(get_upload_folder(), filename)

def cleanup_old_profile_images(user_id, keep_count=1):
    """Delete old profile images, keeping only the most recent ones for a user"""
    try:
        profile_folder = get_profile_images_folder()
        if not os.path.exists(profile_folder):
            return
        
        # Get all profile images for this user
        user_files = []
        for filename in os.listdir(profile_folder):
            if filename.startswith(f"profile_{user_id}_"):
                file_path = os.path.join(profile_folder, filename)
                # Get file creation time for sorting
                creation_time = os.path.getctime(file_path)
                user_files.append((file_path, creation_time, filename))
        
        # Sort by creation time
        user_files.sort(key=lambda x: x[1], reverse=True)
        
        # Delete old files, keeping only the most recent ones
        files_to_delete = user_files[keep_count:]
        for file_path, _, filename in files_to_delete:
            try:
                delete_file_from_path(file_path)
                print(f"Deleted old profile image: {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
                
    except Exception as e:
        print(f"Error during cleanup for user {user_id}: {e}")

@upload_bp.post("/profile-image/<user_id>")
def upload_profile_image(user_id):
    """Upload a profile image for a user"""
    try:
        # Validate user exists
        user = validate_model(User, user_id)
        
        # Check if file was uploaded
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files["image"]
        
        # Validate the file
        is_valid, message = validate_image_file(file)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Create uploads directory if it doesn't exist
        profile_folder = get_profile_images_folder()
        os.makedirs(profile_folder, exist_ok=True)
        
        # Generate unique filename and path
        new_filename = generate_unique_filename(user_id, file.filename)
        file_path = os.path.join(profile_folder, new_filename)
        
        # Save and process the image
        try:
            process_and_save_image(file, file_path)
        except Exception as e:
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500
        
        # Generate URL for the uploaded image
        image_url = f"/upload/uploads/profile_images/{new_filename}"
        
        # Update user's image_url in database
        update_user_image_url(user, image_url)
        
        # Clean up old profile images (keep only the most recent 1)
        cleanup_old_profile_images(user_id, keep_count=1)
        
        return jsonify({
            "message": "Profile image uploaded successfully",
            "image_url": image_url,
            "filename": new_filename
        }), 200
        
    except Exception as e:
        # Check if this is an abort exception (from validate_model)
        if hasattr(e, 'code'):
            # This is an abort exception, let it propagate
            raise
        # This is a real error, return 500
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@upload_bp.delete("/profile-image/<user_id>")
def delete_profile_image(user_id):
    """Delete a user's profile image"""
    try:
        user = validate_model(User, user_id)
        
        if not user.image_url:
            return jsonify({"error": "No profile image to delete"}), 404
        
        # Remove the file from the filesystem
        if user.image_url.startswith("/upload/uploads/"):
            file_path = os.path.join(get_upload_folder(), user.image_url.replace("/upload/uploads/", ""))
            delete_file_from_path(file_path)
        
        # Clear the image_url from the database
        update_user_image_url(user, None)
        
        return jsonify({"message": "Profile image deleted successfully"}), 200
        
    except Exception as e:
        # Check if this is an abort exception (from validate_model)
        if hasattr(e, 'code'):
            # This is an abort exception, let it propagate
            raise
        # This is a real error, return 500
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500 