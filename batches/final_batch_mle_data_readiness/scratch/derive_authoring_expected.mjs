import fs from 'node:fs';
import path from 'node:path';
import {loadPyodide} from '../../../00_FINAL_PIPELINE_CORE/sandbox/node_modules/pyodide/pyodide.mjs';
const B='batches/final_batch_mle.region.data_readiness';
const d=JSON.parse(fs.readFileSync(B+'/interactions.json','utf8'));
const ix=Object.fromEntries(d.tiles.flatMap(t=>t.interactions.map(e=>[e.step_id,e.interaction])));
const py=await loadPyodide({indexURL:path.resolve('00_FINAL_PIPELINE_CORE/sandbox/node_modules/pyodide')+'/',stdout:()=>{},stderr:()=>{}});
await py.loadPackage(['numpy','pandas']);
let i=ix['mle.tile.007_008.s05'];let fixture=structuredClone(i.grading.tests[0].spec.args[0]);fixture.columns.push('extra');fixture.rows.forEach(r=>r.push(0));
py.runPython(i.grading.solution_files[0].content);py.globals.set('_fixture_json',JSON.stringify(fixture));
const schema=JSON.parse(py.runPython("import json\njson.dumps(evaluate(json.loads(_fixture_json)))"));
i=ix['mle.tile.004_006.s11'];
let reg=JSON.parse(fs.readFileSync(B+'/scenario_asset_registry.json','utf8'));
for(let m of i.public.workspace.asset_mounts){let a=reg.assets.find(a=>a.asset_id===m.asset_id);py.FS.writeFile(m.mount_path,fs.readFileSync(B+'/'+a.data_file.uri,'utf8'));}
py.runPython(i.grading.solution_files[0].content);py.globals.set('_budget',i.grading.tests.find(t=>t.test_id==='t1').spec.args[0]);
const chunk=JSON.parse(py.runPython('json.dumps(evaluate(_budget))'));
// Evaluate the eight-row fixture described by the finding, without modifying registered assets.
for(let m of i.public.workspace.asset_mounts){let a=reg.assets.find(a=>a.asset_id===m.asset_id);let csv=fs.readFileSync(B+'/'+a.data_file.uri,'utf8').trimEnd().split('\n').slice(0,9).join('\n')+'\n';py.FS.writeFile(m.mount_path,csv);}
const finding_chunk=JSON.parse(py.runPython('json.dumps(evaluate(_budget))'));
fs.writeFileSync(B+'/scratch/authoring_expected.json',JSON.stringify({schema,chunk,fixture,finding_chunk}));
console.log(JSON.stringify({schema,chunk,finding_chunk}));
