# Personal Website - Flask Application

This is Camilla Clark's personal website, refactored from static HTML to a Flask application using Jinja2 templates.

## Project Structure

```
personal-website/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static files
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── images/          # Images
│   └── Clark_Camilla_Resume.pdf
├── templates/           # Jinja2 templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── about.html       # About page
│   ├── contact.html     # Contact page
│   ├── resume.html      # Resume page
│   ├── iu_mobile.html   # IU Mobile project
│   ├── building_a_mind.html  # Building A Mind project
│   ├── resource_library.html # Resource Library project
│   └── thank_you.html   # Thank you page
└── prompt/
    └── dev_notes.md
```

## Features

- **Responsive Design**: Bootstrap-based responsive layout
- **Template Inheritance**: Uses Jinja2 base template for consistent structure
- **Dynamic Navigation**: Active page highlighting in navigation
- **Contact Form**: Client-side validation with Flask routing
- **Project Showcase**: Individual pages for each project
- **Resume Display**: PDF viewer with download functionality

## Installation and Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   ```

3. **Access the website**:
   Open your browser and navigate to `http://localhost:5000`

## Routes

- `/` - Home page
- `/about` - About page
- `/contact` - Contact page with form
- `/resume` - Resume page with PDF viewer
- `/iu-mobile` - IU Mobile User Feedback project
- `/building-a-mind` - Building A Mind UI project
- `/resource-library` - Career Resource Library project
- `/thank-you` - Thank you page after form submission

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Templates**: Jinja2 templating engine
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JavaScript for form validation
- **Icons**: Bootstrap Icons, Google Material Symbols

## Development Notes

The website was refactored from static HTML files to a Flask application to improve maintainability and enable future dynamic features. All static assets (CSS, JavaScript, images) have been moved to the `static/` directory, and HTML files have been converted to Jinja2 templates in the `templates/` directory.

The base template (`base.html`) provides the common structure including navigation, footer, and external dependencies, while individual page templates extend this base and provide page-specific content.
