from flask import Flask, url_for, session, redirect, render_template, request,jsonify
from flask.ext.oauth import OAuth
from app import app
from app import db, models


app.secret_key = 'my secret-key-!@#$'

oauth = OAuth()
trello = oauth.remote_app('trello',
                          base_url='',
                          request_token_url='https://trello.com/1/OAuthGetRequestToken',
                          access_token_url='https://trello.com/1/OAuthGetAccessToken',
                          authorize_url='https://trello.com/1/OAuthAuthorizeToken',
                          consumer_key='0c967eff30367539f04c711d283aba53',
                          consumer_secret='0a5ad962770bc02019b8f0737c5cb429760e5dadc25236e47067d45db3c1d162')


@trello.tokengetter
def token_getter(token=None):
    return session.get('token')

@app.route('/')
def index():
    return trello.authorize(callback=url_for('authorized'))

@app.route('/authorized/')
@trello.authorized_handler
def authorized(resp):
    session['token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']

    )
    return redirect(url_for('members'))


@app.route('/members', methods=['POST', 'GET'])
def members():
    if request.method == 'POST':
        org_user = request.form['organization']
        base_url = 'https://api.trello.com/1/organizations/'

        data = trello.get(base_url + org_user + '/members').data
        #raise
        # return jsonify(data=data)
        for member in data:
            if models.User.query.filter_by(username=member['username']).first():
                continue
            u = models.User(username=member['username'], fullName=member['fullName'], trello_id=member['id'])
            db.session.add(u)
            db.session.commit()


        return render_template('members.html', members=data)

    return render_template('login.html')

@app.route('/boards', methods=['POST', 'GET'])
def boards():
    if request.method == 'POST':
        org_user = request.form['organization']
        base_url = 'https://api.trello.com/1/organizations/'
        data = trello.get(base_url + org_user + '/boards').data
        return jsonify(data=data)
        for board in data:
            u = models.Board(username=member['username'], fullName=member['fullName'], trello_id=member['id'])
            db.session.add(u)
            db.session.commit()


        return render_template('boards.html', boards=data)
    return render_template('login.html')
@app.route('/list')
def list():
    return render_template('list.html')
