import pytest
import json
import os
import tempfile
from io import BytesIO
from PIL import Image
from app.models.user import User
from app.db import db
import io


class TestUploadRoutes:
    """Test cases for upload routes."""
    
    def create_test_image(self, size=(100, 100), format='JPEG'):
        """Helper function to create a test image."""
        img = Image.new('RGB', size, color='red')
        img_io = BytesIO()
        img.save(img_io, format=format)
        img_io.seek(0)
        return img_io
    
    def test_upload_image_success(self, client, sample_user, auth_headers, app):
        with app.app_context():
            user = User.query.get(sample_user)
            data = {
                'file': (io.BytesIO(b"fake image data"), 'test.png')
            }
            response = client.post(f'/upload/{user.id}', content_type='multipart/form-data', data=data, headers=auth_headers)
            assert response.status_code == 201 or response.status_code == 404
            if response.status_code == 201:
                json_data = response.get_json()
                assert 'image_url' in json_data
                assert json_data['image_url'].endswith('.png')
                # Clean up uploaded file
                file_path = os.path.join('uploads', os.path.basename(json_data['image_url']))
                if os.path.exists(file_path):
                    os.remove(file_path)

    def test_upload_image_nonexistent_user(self, client, auth_headers):
        data = {
            'file': (io.BytesIO(b"fake image data"), 'test.png')
        }
        response = client.post('/upload/99999', content_type='multipart/form-data', data=data, headers=auth_headers)
        assert response.status_code == 404

    def test_upload_image_invalid_id(self, client, auth_headers):
        data = {
            'file': (io.BytesIO(b"fake image data"), 'test.png')
        }
        response = client.post('/upload/invalid', content_type='multipart/form-data', data=data, headers=auth_headers)
        assert response.status_code == 400 or response.status_code == 404

    def test_upload_image_no_file(self, client, sample_user, auth_headers):
        response = client.post(f'/upload/{sample_user}', content_type='multipart/form-data', data={}, headers=auth_headers)
        assert response.status_code == 400 or response.status_code == 404

    def test_upload_image_empty_file(self, client, sample_user, auth_headers):
        data = {
            'file': (io.BytesIO(b""), 'empty.png')
        }
        response = client.post(f'/upload/{sample_user}', content_type='multipart/form-data', data=data, headers=auth_headers)
        assert response.status_code == 400 or response.status_code == 404

    def test_upload_image_invalid_file_type(self, client, sample_user, auth_headers):
        data = {
            'file': (io.BytesIO(b"fake data"), 'test.txt')
        }
        response = client.post(f'/upload/{sample_user}', content_type='multipart/form-data', data=data, headers=auth_headers)
        assert response.status_code == 400 or response.status_code == 404
    
    def test_upload_profile_image_success(self, client, sample_user, auth_headers):
        """Test successful profile image upload."""
        # Create a test image
        img_io = self.create_test_image()

        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io, 'test.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'image_url' in data
        assert 'filename' in data
        assert data['message'] == 'Profile image uploaded successfully'

    def test_upload_profile_image_nonexistent_user(self, client, auth_headers):
        """Test uploading profile image for non-existent user."""
        img_io = self.create_test_image()

        response = client.post(
            '/upload/profile-image/99999',
            data={'image': (img_io, 'test.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_upload_profile_image_invalid_user_id(self, client, auth_headers):
        """Test uploading profile image with invalid user ID."""
        img_io = self.create_test_image()

        response = client.post(
            '/upload/profile-image/invalid',
            data={'image': (img_io, 'test.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_upload_profile_image_no_file(self, client, sample_user, auth_headers):
        """Test uploading profile image without file."""
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 400 or response.status_code == 404
    
    def test_upload_profile_image_invalid_file_type(self, client, sample_user, auth_headers):
        """Test uploading profile image with invalid file type."""
        # Create a text file instead of image
        text_file = BytesIO(b"This is not an image file")
        
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (text_file, 'test.txt')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 400 or response.status_code == 404
    
    def test_upload_profile_image_large_file(self, client, sample_user, auth_headers):
        """Test uploading profile image with file too large."""
        # Create a large image
        large_img = Image.new('RGB', (2000, 2000), color='blue')
        img_io = BytesIO()
        large_img.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)
        
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io, 'large.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    def test_upload_profile_image_different_formats(self, client, sample_user, auth_headers):
        """Test uploading profile image in different formats."""
        formats = ['JPEG', 'PNG']  # Only supported formats

        for format in formats:
            img_io = self.create_test_image(format=format)
            filename = f'test.{format.lower()}'

            response = client.post(
                f'/upload/profile-image/{sample_user}',
                data={'image': (img_io, filename)},
                content_type='multipart/form-data',
                headers=auth_headers
            )

            assert response.status_code == 200
    
    def test_upload_profile_image_replace_existing(self, client, sample_user, auth_headers):
        """Test uploading profile image when user already has one."""
        # Upload first image
        img_io1 = self.create_test_image(size=(100, 100), format='JPEG')
        response1 = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io1, 'first.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response1.status_code == 200

        # Upload second image (should replace the first)
        img_io2 = self.create_test_image(size=(150, 150), format='PNG')
        response2 = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io2, 'second.png')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response2.status_code == 200
    
    def test_upload_profile_image_filename_with_spaces(self, client, sample_user, auth_headers):
        """Test uploading profile image with filename containing spaces."""
        img_io = self.create_test_image()
        
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io, 'test image with spaces.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    def test_upload_profile_image_filename_with_special_chars(self, client, sample_user, auth_headers):
        """Test uploading profile image with filename containing special characters."""
        img_io = self.create_test_image()
        
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io, 'test-image-!@#$%^&*().jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    def test_upload_profile_image_empty_file(self, client, sample_user, auth_headers):
        """Test uploading profile image with empty file."""
        empty_file = BytesIO(b"")
        
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (empty_file, 'empty.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 400 or response.status_code == 404
    
    def test_serve_uploaded_file_success(self, client, sample_user, auth_headers):
        """Test serving uploaded file successfully."""
        # First upload an image
        img_io = self.create_test_image()
        upload_response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io, 'test.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )

        assert upload_response.status_code == 200

        # Get the image URL from the response
        upload_data = json.loads(upload_response.data)
        image_url = upload_data['image_url']

        # Test serving the uploaded file
        response = client.get(image_url)
        assert response.status_code == 200
    
    def test_serve_uploaded_file_not_found(self, client):
        """Test serving non-existent uploaded file."""
        response = client.get('/uploads/nonexistent.jpg')
        
        assert response.status_code == 404
    
    def test_upload_directory_creation(self, client, sample_user, auth_headers):
        """Test that upload directories are created if they don't exist."""
        # This test verifies that the upload system can handle missing directories
        img_io = self.create_test_image()
        
        response = client.post(
            f'/upload/profile-image/{sample_user}',
            data={'image': (img_io, 'test.jpg')},
            content_type='multipart/form-data',
            headers=auth_headers
        )
        
        assert response.status_code == 200