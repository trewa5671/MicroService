from flask import Flask, redirect, request, session, url_for, render_template
import os
import requests

app = Flask(__name__)
app.secret_key = "SOMETHING_UNIQUE_AND_SECRET"

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "evdokimov-client")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "evdokimov-realm")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "UHEeZYn079gMTdks9tIf2ppSSEwmnji2")
REDIRECT_URI = "http://localhost:5051/auth"

@app.route('/')
def index():
    if 'access_token' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    auth_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth?client_id={KEYCLOAK_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=openid"
    return redirect(auth_url)

@app.route('/auth')
def auth():
    code = request.args.get('code')
    if code:
        token_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': KEYCLOAK_CLIENT_ID,
            'client_secret': KEYCLOAK_CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(token_url, headers=headers, data=data)
        token_info = response.json()
        if 'access_token' in token_info:
            session['access_token'] = token_info['access_token']
            return redirect(url_for('index'))
        else:
            return "Ошибка при обмене кода на токен.", 400
    return "Код авторизации не предоставлен.", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051)