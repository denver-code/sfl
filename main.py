from flask import Flask, render_template, request
import flask
#from flask_login import LoginManager,UserMixin,login_user
import flask_login
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.secret_key = 'lol'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'denver': {'password': 'denver'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template("login.html")
    username = flask.request.form['username']
    if flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))
    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    #return 'Login: ' + flask_login.current_user.
    return render_template("protec.html", login = flask_login.current_user.id)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    #return 'Logged out'
    return flask.redirect(flask.url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('401.html')

@app.route('/', methods=["POST","GET"])
def home():
    if request.method == "GET":
        return render_template('main.html')
    elif request.method == "POST":
        print(request.form)
        data = request.form.to_dict(flat = False)
        print(data)
        #return 'Username '+str(data["Username"]+":"+data["Password"])

if __name__ == '__main__':
    app.run(debug=True)