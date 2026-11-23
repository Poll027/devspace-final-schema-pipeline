# Publisher infrastructure, not a learner implementation task.
# oauthlib implements the authorization-code/PKCE protocol; PyJWT and
# cryptography provide signing. The resource server never owns this key.
import json, secrets, time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from oauthlib.oauth2 import Server, RequestValidator
cfg=json.loads(Path('issuer_configuration.json').read_text())
key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
kid=secrets.token_hex(16)
jwk=json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
jwk.update(kid=kid,use='sig',alg='RS256')
class Validator(RequestValidator):
    def __init__(self): self.codes={}
    def validate_client_id(self,client_id,request,*a,**kw): return client_id==cfg['client_id']
    def get_default_redirect_uri(self,client_id,request,*a,**kw): return cfg['redirect_uri']
    def validate_redirect_uri(self,client_id,redirect_uri,request,*a,**kw): return redirect_uri==cfg['redirect_uri']
    def validate_response_type(self,client_id,response_type,client,request,*a,**kw): return response_type=='code'
    def validate_scopes(self,client_id,scopes,client,request,*a,**kw): return set(scopes)<=set(cfg['scopes'])
    def get_default_scopes(self,client_id,request,*a,**kw): return list(cfg['scopes'])
    def save_authorization_code(self,client_id,code,request,*a,**kw):
        self.codes[code['code']]={'client_id':client_id,'redirect_uri':request.redirect_uri,'scopes':request.scopes,'challenge':request.code_challenge,'method':request.code_challenge_method}
    def is_pkce_required(self,client_id,request): return True
    def client_authentication_required(self,request,*a,**kw): return False
    def authenticate_client_id(self,client_id,request,*a,**kw):
        if client_id!=cfg['client_id']: return False
        request.client=type('RegisteredClient',(),{'client_id':client_id})();return True
    def validate_grant_type(self,client_id,grant_type,client,request,*a,**kw): return grant_type=='authorization_code'
    def validate_code(self,client_id,code,client,request,*a,**kw):
        record=self.codes.get(code)
        if not record or record['client_id']!=client_id: return False
        request.scopes=record['scopes'];request.user='training-principal';return True
    def confirm_redirect_uri(self,client_id,code,redirect_uri,client,request,*a,**kw): return self.codes.get(code,{}).get('redirect_uri')==redirect_uri
    def get_code_challenge(self,code,request): return self.codes.get(code,{}).get('challenge')
    def get_code_challenge_method(self,code,request): return self.codes.get(code,{}).get('method')
    def invalidate_authorization_code(self,client_id,code,request,*a,**kw): self.codes.pop(code,None)
    def save_bearer_token(self,token,request,*a,**kw): pass
validator=Validator()
def issue(request,refresh_token=False):
    now=int(time.time())
    return jwt.encode({'iss':cfg['issuer'],'aud':cfg['audience'],'sub':'training-principal','iat':now,'exp':now+600,'scope':' '.join(request.scopes)},key,algorithm='RS256',headers={'kid':kid})
server=Server(validator,token_generator=issue)
class Handler(BaseHTTPRequestHandler):
    def reply(self,status,body,headers=None):
        self.send_response(status)
        for k,v in (headers or {'Content-Type':'application/json'}).items():self.send_header(k,v)
        self.end_headers();self.wfile.write(body.encode())
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/jwks':return self.reply(200,json.dumps({'keys':[jwk]}))
        if path=='/health':return self.reply(200,json.dumps({'issuer':cfg['issuer'],'client_id':cfg['client_id']}))
        if path=='/client/callback':return self.reply(200,json.dumps(parse_qs(urlsplit(self.path).query)))
        if path=='/authorize':
            # The supplied publisher harness represents the already-approved
            # training user; no password grant or production login UI exists.
            headers,body,status=server.create_authorization_response(cfg['issuer']+self.path,scopes=list(cfg['scopes']),credentials={'user':'training-principal'})
            return self.reply(status,body or '',headers)
        self.reply(404,'{}')
    def do_POST(self):
        if urlsplit(self.path).path!='/token':return self.reply(404,'{}')
        body=self.rfile.read(int(self.headers.get('Content-Length',0))).decode()
        headers,body,status=server.create_token_response(cfg['token_url'],http_method='POST',body=body,headers=dict(self.headers))
        self.reply(status,body,headers)
if __name__=='__main__':
    url=urlsplit(cfg['issuer']); HTTPServer((url.hostname,url.port),Handler).serve_forever()
