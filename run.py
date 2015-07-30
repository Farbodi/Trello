from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.oauth import OAuth

app = Flask(__name__)

app.secret_key = 'faRBODGHISDI#$^'

oauth = OAuth()
trello = oauth.remote_app('trello',
                          base_url='',
                          request_token_url='https://trello.com/1/OAuthGetRequestToken',
                          access_token_url='https://trello.com/1/OAuthGetAccessToken',
                          authorize_url='https://trello.com/1/OAuthAuthorizeToken',
                          consumer_key='bf4f2c0e89de05fa7aa14ac46117fd8d',
                          consumer_secret='6d583c387b880c60839155e2661f5f5bd67974f7863b94171884d692194632b0')



app.config['SECRET_KEY'] = 'FaRbodGhIAsi*&^*'
moment = Moment(app)
manager = Manager(app)
bootstrap = Bootstrap(app)


@trello.tokengetter
def token_getter(token=None):
    return session.get('token')

class NameForm(Form):
    name = StringField('What is your Trello username?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(' have changed your name :) !')
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/login')
def login():
    return trello.authorize(callback=url_for('authorized'))

@app.route('/authorized/')
@trello.authorized_handler
def authorized(resp):
    session['token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    return redirect(url_for('members'))

@app.route('/members/')
def test():
    data = trello.get('https://api.trello.com/1/organizations/farbodi1/').data
    return jsonify(data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def intrernal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
    #app.run(debug=True)
