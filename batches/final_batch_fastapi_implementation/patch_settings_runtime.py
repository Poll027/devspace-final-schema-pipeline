import json
from pathlib import Path
p=Path('batches/final_batch_implementation/interactions.json')
d=json.loads(p.read_text())
ix=next(s['interaction'] for t in d['tiles'] for s in t['interactions'] if s['step_id']=='tile_024.s06')
old='from pydantic_settings import BaseSettings, SettingsConfigDict\nfrom pydantic import ValidationError\n'
new='''# Supplied sandbox compatibility scaffold: pydantic_settings is not installed.
# Use Pydantic's bundled v1 BaseSettings with a controlled dotenv source.
# This adapter supports the model_config/env_file spelling used in this exercise;
# it is not the full pydantic_settings package. Leave this scaffold unchanged.
from pydantic.v1 import BaseSettings as _BaseSettings, ValidationError
from typing import ClassVar
import shlex

SettingsConfigDict = dict

class BaseSettings(_BaseSettings):
    model_config: ClassVar[dict] = {}

    class Config:
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            def dotenv_settings(settings):
                filename = settings.model_config.get("env_file")
                if not filename or not Path(filename).exists():
                    return {}
                entries = {}
                for line in Path(filename).read_text(encoding="utf-8").splitlines():
                    if "=" in line:
                        name, raw = line.split("=", 1)
                        tokens = shlex.split(raw)
                        entries[name.strip().upper()] = tokens[0] if tokens else ""
                return {name: entries[name.upper()] for name in settings.__fields__
                        if name.upper() in entries}
            return init_settings, env_settings, dotenv_settings, file_secret_settings
'''
for f in ix['public']['workspace']['files']+ix['grading']['solution_files']:
 assert f['content'].startswith(old)
 f['content']=new+f['content'][len(old):]
ix['public']['prompt'] += ' The supplied sandbox adapter uses Pydantic’s bundled v1 BaseSettings because pydantic_settings is unavailable here; leave the adapter unchanged. It supports the model_config/env_file spelling for these controlled APP_NAME fixtures, not the full pydantic_settings API.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
from collections import Counter
print('tiles',len(d['tiles']),'interactions',sum(len(t['interactions']) for t in d['tiles']),Counter(s['interaction']['type'] for t in d['tiles'] for s in t['interactions']))
