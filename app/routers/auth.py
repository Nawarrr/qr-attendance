from fastapi import APIRouter
from starlette.requests import Request
import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()


# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)



@router.get('/login/{id}' )
async def login(id:int , request : Request ):

    #redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    redirect_uri = os.environ.get('URL') + "/auth"
    request.session['id'] = id
    #print(request.state.id)
    print(request.session.id)
    return await oauth.google.authorize_redirect(request, redirect_uri ) 


@router.route('/auth')
async def auth( request : Request ):
    print(request.url)
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    request.session['user'] = dict(user_data)
    print(request.session.id)
    return RedirectResponse(url=f'/student')