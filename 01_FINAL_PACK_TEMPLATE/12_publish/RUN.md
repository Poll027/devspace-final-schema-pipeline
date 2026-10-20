# 12 publish — script (PLANNED)
Writes `tile_lessons_public/` + `grading/` + the asset registry to the backend store (object storage + DB rows keyed by `tile_id`/`content_hash`), registers new asset hashes, and merges reusable assets (datasets, templates) into the cross-path registry by `concept_id`. Not built yet; blocked on the backend contract in PLAYBOOK §5.
