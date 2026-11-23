def upgrade():
    # DROP COLUMN destroys stored notes; ADD COLUMN produces an empty replacement,
    # so this is not a data-preserving rename.
    # Before approval, manually amend the candidate and test upgrade and downgrade
    # against a disposable database.
    pass
def downgrade():
    # A recreated column cannot recover the deleted values.
    pass
