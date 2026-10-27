"""Pack checkers, merged into three dispatch tables used by validate_tile.py:
    BLOCK[type](C, step, block, rep)   INTERACTION[type](C, step, interaction, rep)   ASSET[kind](C, asset, rep)

To add a pack (e.g. software, security): write checkers/<pack>.py exposing BLOCK / INTERACTION / ASSET dicts and import it below.
validate_tile.py is FAIL-CLOSED: a block/interaction/asset type used by a lesson that has no checker is reported UNVERIFIED
(a warning normally, an error under --strict) instead of silently passing.
"""
from . import code, core, data

BLOCK = {**core.BLOCK, **data.BLOCK}
NO_CHECK_NEEDED = set(core.NO_CHECK_NEEDED)
INTERACTION = {**core.INTERACTION, **data.INTERACTION, **code.INTERACTION}
ASSET = {**core.ASSET, **data.ASSET}
