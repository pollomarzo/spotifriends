from flask import Flask, request

from cred import scopes, redirect_uri, client_id, client_secret

from flask import Flask, request, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
from datetime import datetime
import uuid

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Spotify App credentials
SPOTIFY_CLIENT_ID = client_id
SPOTIFY_CLIENT_SECRET = client_secret
REDIRECT_URI = "https://1b64-151-81-26-199.ngrok-free.app/callback"
SCOPES = scopes


TOKENS_FILE = 'spotify_tokens.json'

# handle DB
def load_tokens():
    """Load tokens from JSON file"""
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    """Save tokens to JSON file"""
    with open(TOKENS_FILE, 'w+') as f:
        json.dump(tokens, f, indent=2)

def store_token(user_id, token_info, spotify_username):
    """Store token information in JSON file"""
    tokens = load_tokens()
    tokens[user_id] = {
        'access_token': token_info['access_token'],
        'refresh_token': token_info['refresh_token'],
        'expires_at': token_info['expires_at'],
        'spotify_username': spotify_username
    }
    save_tokens(tokens)

def get_token(user_id):
    """Retrieve token information from JSON file"""
    tokens = load_tokens()
    return tokens.get(user_id)

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=' '.join(SCOPES)
)

@app.route('/')
def home():
    user_id = str(uuid.uuid4())
    return f"""
    <html>
        <head>
            <title>Spotify Bot</title>
        </head>
        <body>
            <h1>Spotify Bot</h1>
            <p>Click below to authenticate with Spotify:</p>
            <a href="/login/{user_id}">Login with Spotify</a>
            <p>Your User ID: {user_id}</p>
            <p>It's morbin time!</p>
        </body>
    </html>
    """

@app.route('/login/<user_id>')
def login(user_id):
    auth_url = sp_oauth.get_authorize_url()
    print(client_id)
    auth_url += f"&state={user_id}"
    print(auth_url)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    user_id = request.args.get('state')
    
    if code and user_id:
        # try:
        token_info = sp_oauth.get_access_token(code, check_cache=False)
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        user_info = sp.current_user()
        
        store_token(user_id, token_info, user_info['id'])
        
        return f"""
        <h1>Authentication successful!</h1>
        <p>Welcome, {user_info['display_name']}!</p>
        <p>Your User ID: {user_id}</p>
        <p>Save this ID to access your bot later!</p>
        """
        # except Exception as e:
        #     return f"Error: {str(e)}"
    
    return "Error: Invalid callback"

@app.route('/api/token/<user_id>')
def get_user_token(user_id):
    """API endpoint to get token info for a specific user"""
    token_info = get_token(user_id)
    
    if not token_info:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if token needs refresh
    if datetime.now().timestamp() > token_info['expires_at']:
        try:
            new_token = sp_oauth.refresh_access_token(token_info['refresh_token'])
            store_token(user_id, new_token, token_info['spotify_username'])
            token_info = new_token
        except Exception as e:
            return jsonify({'error': f'Token refresh failed: {str(e)}'}), 401
    
    return jsonify({
        'access_token': token_info['access_token'],
        'expires_at': token_info['expires_at']
    })

def create_spotify_client(user_id):
    """Helper function to create a Spotipy client for a specific user"""
    token_info = get_token(user_id)
    if not token_info:
        return None
    
    if datetime.now().timestamp() > token_info['expires_at']:
        try:
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            store_token(user_id, token_info, token_info['spotify_username'])
        except:
            return None
    
    return spotipy.Spotify(auth=token_info['access_token'])

if __name__ == '__main__':
    app.run(port=5000)