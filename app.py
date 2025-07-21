from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Document
from auth import auth_blueprint
from ai import get_ai_suggestions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collab.db'
db.init_app(app)

socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    doc = Document.query.first()
    if not doc:
        doc = Document(content="Start writing here...")
        db.session.add(doc)
        db.session.commit()
    return render_template('index.html', content=doc.content)

@socketio.on('join')
def on_join():
    join_room("document")

@socketio.on('text_update')
def on_text_update(data):
    content = data['content']
    doc = Document.query.first()
    doc.content = content
    db.session.commit()
    emit('text_update', {'content': content}, room="document", include_self=False)

@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    text = data.get("text", "")

    suggestions = []
    if "is" in text:
        suggestions.append("Consider replacing 'is' with stronger verbs.")
    if "are" in text:
        suggestions.append("Check subject-verb agreement for 'are'.")
    if len(text.split()) > 10:
        suggestions.append("Try to shorten the sentence for clarity.")

    return jsonify({"suggestions": suggestions})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)