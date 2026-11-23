import json, time
from pathlib import Path
import jwt
config=json.loads(Path('test_trust.json').read_text())
fixtures=json.loads(Path('fixtures.json').read_text())
tokens={}
for name in ['verified_with_permission','verified_without_permission']:
    context=fixtures[name]
    tokens[name]=jwt.encode({'iss':config['issuer'],'aud':config['audience'],
        'sub':context['owner_id'],'exp':int(time.time())+3600,
        'scope':' '.join(context['scopes'])},config['test_key'],algorithm='HS256')
Path('bearer_fixtures.json').write_text(json.dumps(tokens,indent=2)+'\n')
