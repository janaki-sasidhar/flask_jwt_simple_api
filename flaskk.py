from flask import Flask,request,make_response,jsonify
import jwt
from functools import wraps
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThIsThEsEcReTkEy'


# Decorator
def token_is_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.args.get('token')
        try:
            data = jwt.decode(token,app.config['SECRET_KEY']) # The exception is thrown when the token is  invalid and if the secret key is wrong , then the token is invalid  , so it validates for correct token
        except:
            return jsonify({'Message':'Token is invalid , go to /login route and generate a token'}),403

        return f(*args,**kwargs)
    return decorated

@app.route('/normal')
def normal():
    return 'This doesnt need any login'

@app.route('/helloworld')
@token_is_required
def helloworld():
    return '<h1>Hello World</h1>'

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password' and auth.username == 'username':
        token = jwt.encode({'user':auth.username,'pass':auth.password},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8'), 'message' : 'Now add ?token=<token> in the /helloworld route'})
    return make_response('Couldnt verify!',401,{'WWW-Authenticate':'Basic realm ="Login Required"'})













