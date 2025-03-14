from flask_sqlalchemy import SQLAlchemy
import psycopg2
import yaml

db = SQLAlchemy()

# Models
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    discovery_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    last_login = db.Column(db.String(30), nullable=True)

# Database functions
def create_user(username, password):
    print(f"Create user - {username} / {password}")
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_all_users():
    return User.query.all()

def get_all_vulnerabilities():
    return Vulnerability.query.all()

def get_VulnerabilitiesByCategory(category):
    result = db.session.execute(f"SELECT * FROM Vulnerability WHERE category = '{category}'")
    return Vulnerability.query.all()

def get_all_vulnerabilities_by(category, min_score, max_score, sort_by):
    # Build query
    query = Vulnerability.query

    if category:
        query = query.filter(Vulnerability.category.ilike(f"%{category}%"))
    if min_score is not None:
        query = query.filter(Vulnerability.score >= min_score)
    if max_score is not None:
        query = query.filter(Vulnerability.score <= max_score)

    # Apply sorting
    if sort_by in ['category', 'score', 'status', 'discovery_date']:
        query = query.order_by(sort_by)


    return query.all()

def get_vulnerability_by_id(vuln_id):
    return Vulnerability.query.get_or_404(vuln_id)

def create_vulnerability(score, location, status, discovery_date, category):
    vuln = Vulnerability(score=score, location=location, status=status,
                         discovery_date=discovery_date, category=category)
    db.session.add(vuln)
    db.session.commit()

def update_vulnerability(vuln, score, location, status, discovery_date, category):
    vuln.score = score
    vuln.location = location
    vuln.status = status
    vuln.discovery_date = discovery_date
    vuln.category = category
    db.session.commit()

def delete_vulnerability(vuln):
    db.session.delete(vuln)
    db.session.commit()

def db_init_app(app):
    db.init_app(app)

# Reporting function
def generate_report(yaml_input):
    try:
        data = yaml.load(yaml_input)
        print("Report Generated:", data)
        return data
    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")
        return None