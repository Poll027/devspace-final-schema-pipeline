import json, ast
from pathlib import Path
B=Path('batches/final_batch_persistence')
r=json.loads((B/'scenario_asset_registry.json').read_text())
checks={}
checks['sqlalchemy.retrieve_resource']='''import unittest, json
from pathlib import Path
from support import make_store
from starter import retrieve
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_lookup(self):
        engine,factory=await make_store()
        try:
            async with factory() as session:
                for identity in C["existing_identities"]:
                    entity=await retrieve(session,identity)
                    self.assertEqual(entity.id,identity)
                for identity in C["absent_identities"]:
                    self.assertIsNone(await retrieve(session,identity))
        finally: await engine.dispose()
'''
checks['sqlalchemy.transaction_boundaries']='''import unittest
from support import Session
from starter import related_writes, recover_failed_flush, WriteFailure
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_joint_success(self):
        session=Session()
        await related_writes(session)
        self.assertEqual(session.durable,["first","second"])
        self.assertEqual(session.pending,[])
    async def test_joint_failure(self):
        session=Session(fail_second=True)
        with self.assertRaises(WriteFailure): await related_writes(session)
        self.assertEqual(session.durable,[])
        self.assertEqual(session.pending,[])
    async def test_recovery(self):
        session=Session(fail_flush=True)
        await recover_failed_flush(session)
        self.assertGreater(session.rollback_calls,0)
        self.assertFalse(session.failed)
'''
checks['auth.bearer_dependency']='''import json, unittest
from pathlib import Path
from fastapi.testclient import TestClient
from starter import app
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.TestCase):
    def test_extraction_cases(self):
        client=TestClient(app)
        for case in C["cases"]:
            response=client.get("/credential",headers=case["headers"])
            if case["accepted_extraction"]:
                self.assertTrue(response.is_success)
                scheme,credential=case["headers"]["Authorization"].split(" ",1)
                self.assertEqual(response.json(),{"scheme":scheme,"credentials":credential})
            else: self.assertFalse(response.is_success)
'''
checks['cache.redis_cache_aside']='''import unittest, json
from pathlib import Path
from support import PrimaryStore, Cache
from starter import read_order
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_miss_hit_and_separation(self):
        cache=Cache(); primary=PrimaryStore()
        requests=C["requests"]
        for request,expected in zip(requests,C["expected_primary_values"]):
            self.assertEqual(await read_order(*request,cache,primary),expected)
        calls=len(primary.calls)
        self.assertEqual(await read_order(*requests[-1],cache,primary),C["expected_primary_values"][0])
        self.assertEqual(len(primary.calls),calls)
        self.assertEqual(calls,len(C["expected_primary_values"]))
'''
checks['database.alembic_migrations']='''# Review exercise: human/evaluator checks the learner's comments against contract.json.
# No migration is executed; executable changes are outside the allowed syntax.
import ast, unittest
from pathlib import Path
class Checks(unittest.TestCase):
    def test_review_only_skeleton(self):
        tree=ast.parse(Path(__file__).with_name("starter.py").read_text())
        self.assertEqual([n.name for n in tree.body],["upgrade","downgrade"])
        for function in tree.body:
            self.assertTrue(all(isinstance(n,ast.Pass) for n in function.body))
# Comment meaning (possible rename, loss, correction, reversal verification) requires review.
'''
checks['database.service_query_indexes']='''import json,re,unittest
from pathlib import Path
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.TestCase):
    def test_index_target(self):
        source=Path(__file__).with_name("starter.sql").read_text()
        source="\\n".join(line.split("--",1)[0] for line in source.splitlines())
        pattern=r"CREATE\\s+INDEX\\s+\\w+\\s+ON\\s+"+re.escape(C["table"])+r"\\s*(?:USING\\s+btree\\s*)?\\(\\s*"+re.escape(C["column"])+r"\\s*\\)"
        self.assertRegex(source.lower(),re.compile(pattern,re.I))
# Workload and overhead annotations still require semantic review.
'''
checks['design.api_persistence_model_boundaries']='''import unittest,json
from pathlib import Path
from fastapi.testclient import TestClient
from starter import PublicInput, PublicOutput, order, app
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.TestCase):
    def test_contract(self):
        self.assertIsNot(PublicInput,PublicOutput)
        self.assertEqual(set(PublicInput.model_fields),set(C["public_input_fields"]))
        self.assertEqual(set(PublicOutput.model_fields),set(C["public_output_fields"]))
        self.assertTrue(PublicOutput.model_config.get("from_attributes"))
        value=PublicOutput.model_validate(order).model_dump()
        expected={k:C["row"][k] for k in C["public_output_fields"]}
        self.assertEqual(value,expected)
        self.assertEqual(TestClient(app).get("/orders/42").json(),expected)
'''
checks['fastapi.domain_error_translation']='''import unittest,json
from pathlib import Path
from fastapi.testclient import TestClient
from starter import app,recover,FailedSession
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_recovery_and_translation(self):
        session=FailedSession()
        await recover(session); await session.reuse()
        self.assertGreater(session.rollback_calls,0)
        response=TestClient(app).get("/conflict")
        self.assertEqual(response.status_code,C["declared_status"])
        self.assertNotIn("synthetic private",response.text)
        self.assertNotIn("uniqueness diagnostic",response.text)
'''
checks['fastapi.public_error_envelopes']='''import unittest,json
from pathlib import Path
from fastapi.testclient import TestClient
from starter import app
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.TestCase):
    def test_exception_variants(self):
        client=TestClient(app)
        for case in C["cases"]:
            response=client.get(case["path"])
            self.assertEqual(response.status_code,case["status"])
            self.assertEqual(response.json(),{C["body_field"]:case["reason"]})
            for name,value in case["headers"].items(): self.assertEqual(response.headers[name],value)
'''
checks['fastapi_backend.proxy_header_trust']='''import unittest,json,shlex
from pathlib import Path
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.TestCase):
    def test_launch_flags(self):
        source=Path(__file__).with_name("starter.sh").read_text()
        command=next(line for line in source.splitlines() if line.strip() and not line.lstrip().startswith("#"))
        tokens=shlex.split(command)
        def flag_value(flag):
            for i,token in enumerate(tokens):
                if token==flag: return tokens[i+1]
                if token.startswith(flag+"="): return token.split("=",1)[1]
            return None
        self.assertEqual(flag_value("--forwarded-allow-ips"),C["trusted_proxy_source"])
        self.assertEqual(flag_value("--root-path"),C["stripped_prefix"])
# Public redirect and documentation verification requires the externally supplied HTTPS proxy.
'''
checks['integration.webhook_contracts']='''import unittest,json
from pathlib import Path
from fastapi.testclient import TestClient
from starter import app
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.TestCase):
    def test_delivery_contract(self):
        client=TestClient(app)
        response=client.post("/order-events",json=C["accepted_body"])
        self.assertEqual(response.status_code,C["acknowledgement_status"])
        for body in C["invalid_bodies"]:
            self.assertFalse(client.post("/order-events",json=body).is_success)
        self.assertEqual(client.post("/order-events",content="unparsed text",headers={"Content-Type":C["unsupported_media_type"]}).status_code,415)
# Deferred scheduling and prompt acknowledgement are separately inspected; TestClient waits for background tasks.
'''
checks['observability.request_correlation']='''import unittest, asyncio, logging, json
from pathlib import Path
import httpx
from starter import app, received, logger
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Capture(logging.Handler):
    def __init__(self): super().__init__(); self.records=[]
    def emit(self,record): self.records.append(record)
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_concurrent_contexts(self):
        capture=Capture();logger.addHandler(capture);logger.setLevel(logging.INFO)
        received.clear()
        try:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url="http://test") as client:
                async def send(identifier):
                    return await client.get("/orders/42",headers={C["header_name"]:identifier})
                responses=await asyncio.gather(*(send(x) for x in C["accepted_ids"]))
                self.assertTrue(all(x.is_success for x in responses))
                ids=[h[C["header_name"].lower()] for h in received]
                self.assertCountEqual(ids,C["accepted_ids"])
                logs=[getattr(x,"interaction_id",None) for x in capture.records]
                for identifier in C["accepted_ids"]: self.assertIn(identifier,logs)
                for headers in [{},{C["header_name"]:C["rejected_ids"][0]},{C["header_name"]:C["rejected_ids"][1]}]:
                    previous=len(received)
                    response=await client.get("/orders/42",headers=headers)
                    self.assertTrue(response.is_success)
                    self.assertGreater(len(received),previous)
                    identifier=received[-1][C["header_name"].lower()]
                    self.assertRegex(identifier,r"^[A-Za-z0-9-]{1,32}$")
                    self.assertIn(identifier,[getattr(x,"interaction_id",None) for x in capture.records])
        finally: logger.removeHandler(capture)
'''
checks['rest.bounded_resource_listing']='''import unittest,json
from pathlib import Path
from support import make_store
from starter import listing
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_ordered_pages(self):
        engine,factory=await make_store()
        try:
            async with factory() as session:
                size=C["page_size_max"]
                for page in range(C["page_min"],C["page_max"]+1):
                    rows=await listing(session,page,size)
                    offset=(page-1)*size
                    self.assertLessEqual(offset,C["offset_ceiling"])
                    self.assertEqual([r.id for r in rows],C["ordered_matching_ids"][offset:offset+size])
        finally: await engine.dispose()
# Query numeric constraints and out-of-range rejection are inspected through the final route.
'''
checks['security.injection_resistant_inputs']='''import unittest,json
from pathlib import Path
from sqlalchemy import event
from support import make_store
from starter import lookup
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_binding(self):
        engine,factory=await make_store(); statements=[]
        @event.listens_for(engine.sync_engine,"before_cursor_execute")
        def capture(connection,cursor,statement,parameters,context,many):
            statements.append((statement,parameters))
        try:
            async with factory() as session:
                for value in C["supplied_values"]:
                    result=await lookup(session,value)
                    rows=result.scalars().all()
                    self.assertTrue(all(row==value for row in rows))
                self.assertEqual(len(set(s for s,p in statements)),1)
                self.assertTrue(all(p for s,p in statements))
        finally: await engine.dispose()
'''
checks['sqlalchemy.create_resource']='''import unittest,json
from pathlib import Path
from support import make_store, Entity
from starter import create
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_committed_creation(self):
        engine,factory=await make_store()
        try:
            async with factory() as session:
                identity=await create(session,C["supplied_values"],factory)
            self.assertIsNotNone(identity)
            async with factory() as fresh:
                entity=await fresh.get(Entity,identity)
                self.assertIsNotNone(entity)
                for name,value in C["supplied_values"].items(): self.assertEqual(getattr(entity,name),value)
        finally: await engine.dispose()
'''
checks['sqlalchemy.delete_resource']='''import unittest,json
from pathlib import Path
from support import make_store, Order
from starter import delete_order, verify_deletion
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class FailedDelete:
    def __init__(self,entity): self.entity=entity;self.deleted=False;self.rolled_back=False
    async def get(self,mapping,identity): return self.entity
    async def delete(self,entity): self.deleted=True
    async def flush(self): raise RuntimeError("synthetic flush failure")
    async def commit(self): raise AssertionError("commit after failure")
    async def rollback(self): self.rolled_back=True
class AbsentTarget:
    async def get(self,mapping,identity): return None
    async def delete(self,entity): raise AssertionError("delete called on absence")
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_deletion(self):
        engine,factory=await make_store()
        try:
            async with factory() as session: await delete_order(session,C["target_identity"])
            async with factory() as fresh:
                self.assertIsNone(await fresh.get(Order,C["target_identity"]))
                self.assertIsNotNone(await fresh.get(Order,C["other_identity"]))
            await verify_deletion(factory,C["target_identity"],C["other_identity"])
            await delete_order(AbsentTarget(),C["absent_identity"])
            async with factory() as session: entity=await session.get(Order,C["other_identity"])
            failure=FailedDelete(entity)
            with self.assertRaises(RuntimeError): await delete_order(failure,C["other_identity"])
            self.assertTrue(failure.rolled_back)
        finally: await engine.dispose()
'''
checks['sqlalchemy.update_resource']='''import unittest,json
from pathlib import Path
from support import make_store, Order
from starter import update_order, PartialUpdate
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_selective_committed_update(self):
        engine,factory=await make_store()
        try:
            async with factory() as session:
                await update_order(session,C["order_id"],PartialUpdate(**C["partial_update"]),factory)
            async with factory() as fresh:
                entity=await fresh.get(Order,C["order_id"])
                self.assertEqual(entity.note,C["partial_update"]["note"])
                self.assertEqual(entity.quantity,C["expected_unchanged_quantity"])
        finally: await engine.dispose()
'''
checks['auth.jwt_verification']='''import unittest
from fastapi.testclient import TestClient
from starter import app
from fixtures import credential_cases
class Checks(unittest.TestCase):
    def test_verified_output_only(self):
        client=TestClient(app)
        for name,token in credential_cases().items():
            response=client.get("/protected",headers={"Authorization":"Bearer "+token})
            if name=="valid":
                self.assertTrue(response.is_success)
                self.assertTrue(response.json()["protected"])
            else:
                self.assertFalse(response.is_success)
                self.assertNotIn('"protected":true',response.text.replace(" ",""))
'''
checks['cache.freshness_policy']='''import unittest,json,os
from pathlib import Path
from redis.asyncio import Redis
from starter import read_notes,change_notes
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_expiry_and_invalidation(self):
        # Exercise engine supplies an isolated connected Redis; no production default.
        if "EXERCISE_REDIS_URL" not in os.environ: self.skipTest("isolated Redis runtime required")
        cache=Redis.from_url(os.environ["EXERCISE_REDIS_URL"],decode_responses=True)
        key=C["cache_key"];primary={"notes":C["old_notes"]}
        async def load(): return primary["notes"]
        async def committed_update(notes): primary["notes"]=notes
        seconds=C["tolerance_seconds"]
        try:
            await cache.delete(key)
            self.assertEqual(await cache.ttl(key),C["ttl_sentinels"]["absent_key"])
            await cache.set(key,C["old_notes"])
            self.assertEqual(await cache.ttl(key),C["ttl_sentinels"]["no_expiry"])
            await cache.delete(key)
            self.assertEqual(await read_notes(cache,key,load,seconds),C["old_notes"])
            ttl=await cache.ttl(key)
            self.assertGreater(ttl,0);self.assertLessEqual(ttl,seconds)
            await change_notes(cache,key,committed_update,C["new_notes"])
            self.assertEqual(await cache.ttl(key),C["ttl_sentinels"]["absent_key"])
            self.assertEqual(await read_notes(cache,key,load,seconds),C["new_notes"])
        finally:
            await cache.delete(key);await cache.aclose()
'''
checks['cache.safe_failure_policy']='''import unittest,json
from pathlib import Path
from redis.exceptions import ConnectionError,TimeoutError
from support import FailingCache,Cache
from starter import safe_read
C=json.loads(Path(__file__).with_name("contract.json").read_text())
class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_failure_boundaries(self):
        async def load(): return C["primary_value"]
        for operation in C["failure_operations"]:
            for exception in (ConnectionError,TimeoutError):
                cache=FailingCache(operation,exception)
                self.assertEqual(await safe_read(cache,"synthetic-key",load,30),C["primary_value"])
        async def unavailable_primary(): raise RuntimeError("synthetic primary failure")
        with self.assertRaises(RuntimeError):
            await safe_read(Cache(),"synthetic-key",unavailable_primary,30)
# Finite Redis constructor settings are additionally inspected in starter.py.
'''
assert len(checks)==20
for a in r['assets']:
    if a['asset_kind']!='code_workspace':continue
    cid=a['asset_id'][3:]
    test=checks[cid];ast.parse(test)
    a['files'].append({'path':'test_scaffold.py','content':test})
    readme=next(f for f in a['files'] if f['path']=='README.md')
    readme['content']+='\nAfter completing TODOs, run python -m unittest test_scaffold. These supplied observable checks are not a complete semantic grader: allowed/blocked syntax, explicit absence handling, finite timeouts and explanatory review comments must also be inspected against contract.json. The proxy case requires the external HTTPS fixture; the freshness case requires an isolated Redis via EXERCISE_REDIS_URL.\n'
# Register the histogram source alongside the dashboard data, rather than making later stages rely on a working file.
a=next(x for x in r['assets'] if x['asset_id']=='ds.service_signals')
hist=json.loads((B/'working/service_signal_histograms.json').read_text())
a['description']+=' Histogram bucket counts are supplied in ds.service_signal_histograms for each same-group window.'
# A smallest long-format table with cumulative histogram buckets and explicit +Inf bucket.
rows=[]
for h in hist:
    for i,(bound,count) in enumerate(zip(h['bucket_bounds_seconds'],h['cumulative_bucket_counts'])):
        rows.append([h['window'],'GET','/orders/{order_id}','le='+str(bound),i,count])
    rows.append([h['window'],'GET','/orders/{order_id}','+Inf',len(h['bucket_bounds_seconds']),len(h['durations_seconds'])])
r['assets'].insert(3,{'asset_id':'ds.service_signal_histograms','asset_kind':'dataset','scenario_id':r['scenarios'][0]['scenario_id'],'title':'Synthetic grouped latency histogram buckets','description':'Cumulative duration bucket counts underlying ds.service_signals; bucket_le_seconds is a textual bucket label including +Inf, not a directly aggregatable duration measure. bucket_order gives deterministic display order. Same window/method/route grouping as the dashboard; every bucket is cumulative, so counts must not be summed across buckets.','columns':[{'name':'window','type':'string','semantic_role':'categorical'},{'name':'method','type':'string','semantic_role':'categorical'},{'name':'route_template','type':'string','semantic_role':'categorical'},{'name':'bucket_le_seconds','type':'string','semantic_role':'categorical','description':'Textual histogram upper-bound label prefixed le=, including +Inf.'},{'name':'bucket_order','type':'integer','semantic_role':'numerical','description':'Display ordering position, not an event count.'},{'name':'cumulative_count','type':'integer','semantic_role':'numerical'}],'rows':rows,'variants':[],'provenance':'generated_by_script'})
(B/'scenario_asset_registry.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print('Added 20 supplied workspace test scaffolds; registered histogram provenance as a fourth dataset.')
