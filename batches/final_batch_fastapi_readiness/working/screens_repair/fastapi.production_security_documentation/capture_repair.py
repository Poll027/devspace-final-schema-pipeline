import json
from application import app
schema=app.openapi()
print(json.dumps({'components':{'securitySchemes':schema['components']['securitySchemes']},
                  'operations':{method.upper()+' '+path:operation['security']
                     for path,methods in schema['paths'].items()
                     for method,operation in methods.items()}},indent=2))
