import base64, hashlib, secrets
from urllib.parse import urlsplit, parse_qs
import httpx
class AcquisitionHarness:
    def __init__(self,configuration):self.configuration=configuration
    def acquire(self):
        c=self.configuration
        verifier=secrets.token_urlsafe(48)
        challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
        state=secrets.token_urlsafe(24)
        with httpx.Client(follow_redirects=False) as client:
            redirect=client.get(c['authorization_url'],params={'response_type':'code','client_id':c['client_id'],'redirect_uri':c['redirect_uri'],'scope':' '.join(c['scopes']),'state':state,'code_challenge':challenge,'code_challenge_method':'S256'})
            if redirect.status_code != 302: raise RuntimeError(redirect.text)
            location=redirect.headers['location']
            if location.split('?')[0]!=c['redirect_uri']:raise ValueError('Unregistered callback')
            callback=client.get(location);callback.raise_for_status()
            params=parse_qs(urlsplit(location).query)
            if params.get('state')!=[state]:raise ValueError('State mismatch')
            response=client.post(c['token_url'],data={'grant_type':'authorization_code','client_id':c['client_id'],'code':params['code'][0],'redirect_uri':c['redirect_uri'],'code_verifier':verifier})
            response.raise_for_status()
            return response.json()['access_token']
