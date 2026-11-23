import base64,hashlib,json,subprocess,sys
from pathlib import Path
m=json.loads(Path('middleware_distribution.json').read_text())
p=Path('vendor')/m['wheel_filename']
p.write_bytes(base64.b64decode(Path(str(p)+'.b64').read_text()))
assert hashlib.sha256(p.read_bytes()).hexdigest()==m['wheel_sha256']
subprocess.run([sys.executable,'-m','pip','install','--no-index','--no-deps',str(p)],check=True)
