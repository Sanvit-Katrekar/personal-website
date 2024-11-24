from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(120))
    comment = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Comment {self.name}>"

# Create the database tables (if not already created)
with app.app_context():
    db.create_all()

# Route for the homepage
@app.route('/')
def index():
    comments = Comment.query.all()
    return render_template('index.html', comments=[{'NAME': c.name, 'POSITION': c.position, 'COMMENT': c.comment} for c in comments])

# Route for handling the form submission
@app.route('/add_comment', methods=['POST'])
def add_comment():
    name = request.form['name']
    position = request.form['position']
    comment_text = request.form['comment']

    # Create a new comment instance and add it to the database
    new_comment = Comment(name=name, position=position, comment=comment_text)
    db.session.add(new_comment)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)