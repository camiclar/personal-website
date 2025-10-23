import pytest
import sqlite3
import tempfile
import os
import time
from pathlib import Path
from DAL import init_db, seed_projects, get_all_projects, get_project_by_slug, insert_project, _slugify, _unique_slug


class TestDatabaseOperations:
    """Test database operations with temporary database files."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        
        # Store original DB_PATH
        import DAL
        original_db_path = DAL.DB_PATH
        DAL.DB_PATH = Path(temp_file.name)
        
        # Initialize the database
        init_db()
        
        yield temp_file.name
        
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
    
    def test_init_db_creates_table(self, temp_db):
        """Test that init_db creates the projects table."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        
        # Check if table exists
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None
        assert result[0] == 'projects'
    
    def test_seed_projects_populates_database(self, temp_db):
        """Test that seed_projects adds initial data."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        
        # Seed the database
        seed_projects()
        
        # Check if projects were added
        projects = get_all_projects()
        assert len(projects) == 3
        
        # Check specific projects
        project_titles = [p['title'] for p in projects]
        assert 'IU Mobile User Feedback' in project_titles
        assert 'Building A Mind UI' in project_titles
        assert 'Career Resource Library' in project_titles
    
    def test_seed_projects_idempotent(self, temp_db):
        """Test that seed_projects doesn't duplicate data when run multiple times."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        
        # Run seed_projects twice
        seed_projects()
        seed_projects()
        
        # Should still have only 3 projects
        projects = get_all_projects()
        assert len(projects) == 3
    
    def test_get_all_projects_returns_list(self, temp_db):
        """Test that get_all_projects returns a list of dictionaries."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        seed_projects()
        
        projects = get_all_projects()
        assert isinstance(projects, list)
        assert len(projects) > 0
        
        # Check structure of first project
        project = projects[0]
        assert isinstance(project, dict)
        assert 'id' in project
        assert 'slug' in project
        assert 'title' in project
        assert 'description' in project
        assert 'image_file_name' in project
    
    def test_get_project_by_slug_existing(self, temp_db):
        """Test getting an existing project by slug."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        seed_projects()
        
        project = get_project_by_slug('iu-mobile')
        assert project is not None
        assert project['title'] == 'IU Mobile User Feedback'
        assert project['slug'] == 'iu-mobile'
    
    def test_get_project_by_slug_nonexistent(self, temp_db):
        """Test getting a non-existent project by slug."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        seed_projects()
        
        project = get_project_by_slug('nonexistent-project')
        assert project is None
    
    def test_insert_project_creates_new_project(self, temp_db):
        """Test inserting a new project."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        seed_projects()
        
        new_project = insert_project(
            title='Test Project',
            description='A test project description',
            image_file_name='test-image.jpg'
        )
        
        assert new_project is not None
        assert new_project['title'] == 'Test Project'
        assert new_project['description'] == 'A test project description'
        assert new_project['image_file_name'] == 'test-image.jpg'
        assert new_project['slug'] == 'test-project'
        
        # Verify it was actually inserted
        projects = get_all_projects()
        assert len(projects) == 4
        
        # Verify we can retrieve it by slug
        retrieved = get_project_by_slug('test-project')
        assert retrieved is not None
        assert retrieved['title'] == 'Test Project'
    
    def test_slugify_function(self):
        """Test the slugify function."""
        assert _slugify('Hello World') == 'hello-world'
        assert _slugify('Test Project 123') == 'test-project-123'
        assert _slugify('Special@Characters#Here!') == 'special-characters-here'
        assert _slugify('') == 'project'
        assert _slugify('   ') == 'project'
    
    def test_unique_slug_generation(self, temp_db):
        """Test that unique slugs are generated for duplicate titles."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        seed_projects()
        
        # Insert first project
        project1 = insert_project('Test Project', 'Description 1', 'image1.jpg')
        assert project1['slug'] == 'test-project'
        
        # Insert second project with same title
        project2 = insert_project('Test Project', 'Description 2', 'image2.jpg')
        assert project2['slug'] == 'test-project-2'  # Fixed: starts from 2, not 1
        
        # Insert third project with same title
        project3 = insert_project('Test Project', 'Description 3', 'image3.jpg')
        assert project3['slug'] == 'test-project-3'
    
    def test_database_connection_handling(self, temp_db):
        """Test that database connections are properly handled."""
        import DAL
        DAL.DB_PATH = Path(temp_db)
        seed_projects()
        
        # Multiple operations should work without connection issues
        projects1 = get_all_projects()
        project = get_project_by_slug('iu-mobile')
        projects2 = get_all_projects()
        
        assert len(projects1) == len(projects2)
        assert project is not None
