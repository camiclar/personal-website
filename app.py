from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
from DAL import init_db, seed_projects, get_project_by_slug, get_all_projects, insert_project

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

UPLOAD_FOLDER = Path('static/images')
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
DEFAULT_IMAGE = 'Image-Coming-Soon.png'

# Ensure database and seed data are available when the app starts (dev convenience)
init_db()
seed_projects()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Project submission form (was contact)."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        image_file_name = DEFAULT_IMAGE
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = Path(filename).suffix.lower()
            if ext in ALLOWED_EXTENSIONS:
                save_path = UPLOAD_FOLDER / filename
                # Avoid overwrite by adding suffix if exists
                counter = 1
                base = save_path.stem
                while save_path.exists():
                    save_path = UPLOAD_FOLDER / f"{base}-{counter}{ext}"
                    counter += 1
                file.save(save_path)
                image_file_name = save_path.name
            else:
                flash('Unsupported image type. Allowed: png, jpg, jpeg, gif, webp')

        if not title or not description:
            flash('Title and Description are required')
            return render_template('contact.html')

        insert_project(title=title, description=description, image_file_name=image_file_name)
        return redirect(url_for('projects'))

    return render_template('contact.html')

@app.route('/resume')
def resume():
    """Resume page"""
    return render_template('resume.html')

@app.route('/iu-mobile')
def iu_mobile():
    """IU Mobile project page"""
    project = get_project_by_slug('iu-mobile')
    return render_template('iu_mobile.html', project=project)

@app.route('/building-a-mind')
def building_a_mind():
    """Building A Mind project page"""
    project = get_project_by_slug('building-a-mind')
    return render_template('building_a_mind.html', project=project)

@app.route('/resource-library')
def resource_library():
    """Resource Library project page"""
    project = get_project_by_slug('resource-library')
    return render_template('resource_library.html', project=project)

@app.route('/thank-you')
def thank_you():
    """Thank you page after form submission"""
    return render_template('thank_you.html')

@app.route('/projects')
def projects():
    """Projects listing page"""
    projects = get_all_projects()
    return render_template('projects.html', projects=projects)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
