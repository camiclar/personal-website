from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/resume')
def resume():
    """Resume page"""
    return render_template('resume.html')

@app.route('/iu-mobile')
def iu_mobile():
    """IU Mobile project page"""
    return render_template('iu_mobile.html')

@app.route('/building-a-mind')
def building_a_mind():
    """Building A Mind project page"""
    return render_template('building_a_mind.html')

@app.route('/resource-library')
def resource_library():
    """Resource Library project page"""
    return render_template('resource_library.html')

@app.route('/thank-you')
def thank_you():
    """Thank you page after form submission"""
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
