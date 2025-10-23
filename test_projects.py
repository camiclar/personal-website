import pytest
import tempfile
import os
import time
from pathlib import Path
from flask import Flask
from app import app
from DAL import init_db, seed_projects


class TestFlaskRoutes:
    """Test Flask application routes and functionality."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask application."""
        # Create a temporary database for testing
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        
        # Temporarily change DB_PATH
        import DAL
        original_db_path = DAL.DB_PATH
        DAL.DB_PATH = Path(temp_file.name)
        
        # Initialize and seed the test database
        init_db()
        seed_projects()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            yield client
        
        # Cleanup - ensure all connections are closed
        try:
            # Force close any remaining connections
            import gc
            gc.collect()
            time.sleep(0.1)  # Give Windows time to release file handles
            
            DAL.DB_PATH = original_db_path
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
        except PermissionError:
            # If we can't delete, just restore the original path
            DAL.DB_PATH = original_db_path
    
    def test_index_route(self, client):
        """Test the home page route."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Hello, World!' in response.data
        assert b"I'm Camilla" in response.data
        assert b'Latest Projects' in response.data
    
    def test_about_route(self, client):
        """Test the about page route."""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'Nice to meet you!' in response.data
        assert b'Indiana University' in response.data
    
    def test_resume_route(self, client):
        """Test the resume page route."""
        response = client.get('/resume')
        assert response.status_code == 200
        assert b'Resume' in response.data
        assert b'Download or view my resume' in response.data
    
    def test_projects_route(self, client):
        """Test the projects listing page route."""
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'All Projects' in response.data
        assert b'IU Mobile User Feedback' in response.data
        assert b'Building A Mind UI' in response.data
        assert b'Career Resource Library' in response.data
    
    def test_iu_mobile_route(self, client):
        """Test the IU Mobile project page route."""
        response = client.get('/iu-mobile')
        assert response.status_code == 200
        assert b'IU Mobile User Feedback' in response.data
        assert b'User Research and Data Analysis' in response.data
    
    def test_building_a_mind_route(self, client):
        """Test the Building A Mind project page route."""
        response = client.get('/building-a-mind')
        assert response.status_code == 200
        assert b'Building A Mind UI' in response.data
        assert b'Computer Vision Research' in response.data
    
    def test_resource_library_route(self, client):
        """Test the Resource Library project page route."""
        response = client.get('/resource-library')
        assert response.status_code == 200
        assert b'Career Resource Library' in response.data
        assert b'Data Migration' in response.data
    
    def test_contact_get_route(self, client):
        """Test the contact page GET route (project submission form)."""
        response = client.get('/contact')
        assert response.status_code == 200
        assert b'Add a New Project' in response.data
        assert b'Project Title' in response.data
        assert b'Description' in response.data
        assert b'Project Image' in response.data
    
    def test_contact_post_route_valid_data(self, client):
        """Test the contact page POST route with valid data."""
        data = {
            'title': 'Test Project',
            'description': 'This is a test project description for testing purposes.'
        }
        
        response = client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'All Projects' in response.data  # Should redirect to projects page
        assert b'Test Project' in response.data  # New project should be visible
    
    def test_contact_post_route_missing_title(self, client):
        """Test the contact page POST route with missing title."""
        data = {
            'description': 'This is a test project description.'
        }
        
        response = client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Add a New Project' in response.data  # Should stay on form page
    
    def test_contact_post_route_missing_description(self, client):
        """Test the contact page POST route with missing description."""
        data = {
            'title': 'Test Project'
        }
        
        response = client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Add a New Project' in response.data  # Should stay on form page
    
    def test_contact_post_route_with_image(self, client):
        """Test the contact page POST route with image upload."""
        data = {
            'title': 'Test Project with Image',
            'description': 'This is a test project with an image.'
        }
        
        # Create a temporary image file
        temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_image.write(b'fake image data')
        temp_image.close()
        
        try:
            with open(temp_image.name, 'rb') as img_file:
                data['image'] = (img_file, 'test.jpg')
                response = client.post('/contact', data=data, follow_redirects=True)
                assert response.status_code == 200
                assert b'All Projects' in response.data
                assert b'Test Project with Image' in response.data
        finally:
            os.unlink(temp_image.name)
    
    def test_thank_you_route(self, client):
        """Test the thank you page route."""
        response = client.get('/thank-you')
        assert response.status_code == 200
        assert b'Thank You!' in response.data
        assert b'Message Sent Successfully' in response.data
    
    def test_nonexistent_route(self, client):
        """Test accessing a non-existent route."""
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
    
    def test_static_files_served(self, client):
        """Test that static files are properly served."""
        # Test CSS files
        response = client.get('/static/css/styles.css')
        assert response.status_code == 200
        
        response = client.get('/static/css/normalize.css')
        assert response.status_code == 200
        
        response = client.get('/static/css/hover.css')
        assert response.status_code == 200
    
    def test_project_images_served(self, client):
        """Test that project images are properly served."""
        response = client.get('/static/images/iu-mobile-sentiments.jpg')
        assert response.status_code == 200
        
        response = client.get('/static/images/bam-preview.jpg')
        assert response.status_code == 200
        
        response = client.get('/static/images/resource-library-preview.jpg')
        assert response.status_code == 200
    
    def test_navigation_links(self, client):
        """Test that navigation links work correctly."""
        # Test home page navigation
        response = client.get('/')
        assert b'href="/about"' in response.data
        assert b'href="/resume"' in response.data
        assert b'href="/contact"' in response.data
        assert b'href="/projects"' in response.data
    
    def test_project_page_navigation(self, client):
        """Test navigation on project pages."""
        response = client.get('/iu-mobile')
        assert b'href="/"' in response.data
        assert b'href="/about"' in response.data
        assert b'href="/resume"' in response.data
        assert b'href="/contact"' in response.data
    
    def test_resume_pdf_served(self, client):
        """Test that the resume PDF is properly served."""
        response = client.get('/static/Clark_Camilla_Resume.pdf')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/pdf'
    
    def test_form_validation_client_side(self, client):
        """Test that client-side form validation is present."""
        response = client.get('/contact')
        assert b'required' in response.data
        assert b'minlength' in response.data
        assert b'accept=' in response.data  # File input accept attribute
