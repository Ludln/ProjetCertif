import logging
import subprocess

from flask import Flask, render_template, request, redirect, url_for, session, flash
from configparser import ConfigParser

import traceback

from db_functions import create_user, get_user_by_username, get_all_vulnerabilities, \
    get_vulnerability_by_id, create_vulnerability, update_vulnerability, delete_vulnerability, get_all_vulnerabilities_by, db_init_app, generate_report, get_all_users

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

app = Flask(__name__)
app.secret_key = 'LSAIDIUduududzo7787hh'
app.config['PROPAGATE_EXCEPTIONS'] = True

def _read_config(app, filename='../config.ini', section='database'):
    parser = ConfigParser()
    parser.read(filename)

    # Vérifie que la section 'database' existe dans le fichier de configuration
    if parser.has_section(section):
        params = parser.items(section)
        # Convertit les paramètres en un dictionnaire
        db_params = {param[0]: param[1] for param in params}

        db_user = db_params['user']
        db_pass = db_params['password']
        db_port = db_params['port']
        db_host = db_params['host']

        app.config['SQLALCHEMY_DATABASE_URI'] = (
                'postgresql://' + db_user + ':' + db_pass + '@' + db_host +':' + db_port + '/your_database'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    else:
        raise Exception(f"Unable to read DB config file from  <{filename}>")

_read_config(app)
db_init_app(app)

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug(f'Incoming login request {request.method} -> {request.form} ')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    vulnerabilities = get_all_vulnerabilities()
    return render_template('index.html', vulnerabilities=vulnerabilities)

@app.route('/create', methods=['GET', 'POST'])
def create():
    logging.debug(f'Vulnerability creation request')

    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        create_vulnerability(
            score=request.form['score'],
            location=request.form['location'],
            status=request.form['status'],
            discovery_date=request.form['discovery_date'],
            category=request.form['category']
        )
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/server_date')
def server_date():
    try:
        date_format = request.args.get('format', default='%Y-%m-%d %H:%M:%S')
        result = subprocess.check_output(['/bin/date +"' + date_format + '"'], shell=True)
        result = result.decode('utf-8').strip()

        return {'server_date': result}
    except Exception as e:
        return {'error': str(e)}

@app.route('/debug')
def dump_params():
    params = {
        'cnx': app.config['SQLALCHEMY_DATABASE_URI'],
        'App_id': app.secret_key
    }
    return params

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    logging.debug(f'Vulnerability update request')
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    vulnerability = get_vulnerability_by_id(id)
    if request.method == 'POST':
        update_vulnerability(
            vulnerability,
            score=request.form['score'],
            location=request.form['location'],
            status=request.form['status'],
            discovery_date=request.form['discovery_date'],
            category=request.form['category']
        )
        return redirect(url_for('index'))

    return render_template('update.html', vulnerability=vulnerability)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    logging.debug(f'Vulnerability delete request')
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    vulnerability = get_vulnerability_by_id(id)
    delete_vulnerability(vulnerability)
    return redirect(url_for('index'))

@app.route('/list_users')
def list_users():
    logging.debug(f'List users request')
    users = get_all_users()
    return render_template('list_users.html', users=users)

# Route to view all vulnerabilities with filters and sorting
@app.route('/vulnerabilities', methods=['GET'])
def view_all():
    logging.debug(f'Vulnerability list request')
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    # Get filter and sort parameters
    category = request.args.get('category', '')
    min_score = request.args.get('min_score', type=float)
    max_score = request.args.get('max_score', type=float)
    sort_by = request.args.get('sort', 'id')  # Default sort by ID

    vulnerabilities = get_all_vulnerabilities_by(category, min_score, max_score, sort_by)
    return render_template('view_all.html', vulnerabilities=vulnerabilities)

# Route to view all vulnerabilities with filters and sorting
@app.route('/report/<string:criteria>', methods=['GET'])
def report(criteria):
    logging.debug(f'Report creation request')
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    # Get filter and sort parameters
    criteria = request.args.get('criteria', '')

    vulnerabilities = generate_report(criteria)
    return render_template('view_all.html', vulnerabilities=vulnerabilities)


@app.errorhandler(500)
def internal_server_error(error):
    error_details = str(error)
    stack_trace = traceback.format_exc()

    logging.error(f"Internal Server Error: {error_details}")
    return render_template('500.html', error_details=error_details, stack_trace=stack_trace), 500


@app.errorhandler(400)
def handle_bad_request(e):
    if 'CSRF token missing' in str(e):
        return render_template('400.html'), 400

@app.errorhandler(404)
def not_found_error(error):
    logging.warning(f"Page not found: {request.url}")
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=8080)
