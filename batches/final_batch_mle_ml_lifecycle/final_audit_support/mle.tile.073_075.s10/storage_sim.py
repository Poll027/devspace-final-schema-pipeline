"""Bounded local Cloud Storage interface, never a real cloud client."""
from pathlib import Path
class PreconditionFailed(Exception):
    status_code = 412
class RecoverableFailure(Exception):
    pass
class StorageClient:
    def __init__(self, initial=None, race=None):
        self.objects = dict(initial or {})
        self.race = dict(race or {})
        self.uploads = []
        self.requests = []
    def blob(self, name):
        return Blob(self, name)
class Blob:
    def __init__(self, client, name):
        self.client, self.name = client, name
        self.generation = None
    def exists(self):
        return self.name in self.client.objects
    def reload(self):
        self.generation = self.client.objects[self.name]["generation"]
    def download_as_bytes(self, if_generation_match):
        self.client.requests.append((self.name, if_generation_match))
        obj = self.client.objects[self.name]
        if obj["generation"] != if_generation_match:
            raise PreconditionFailed("generation mismatch")
        return obj["data"]
    def upload_from_filename(self, path, if_generation_match):
        if if_generation_match != 0:
            raise ValueError("fixture contract permits create-only upload")
        if self.name in self.client.race:
            self.client.objects[self.name] = self.client.race.pop(self.name)
            raise PreconditionFailed("412 concurrent creation")
        if self.exists():
            raise PreconditionFailed("412 already exists")
        self.client.objects[self.name] = {"generation": 1, "data": Path(path).read_bytes()}
        self.client.uploads.append(self.name)
        self.reload()
