from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload
class Base(DeclarativeBase):
    pass
class Entity(Base):
    __tablename__ = 'Entity'
    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_attribute: Mapped[list['Child']] = relationship(back_populates='parent')
class Child(Base):
    __tablename__ = 'relationship_attribute'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('Entity.id'))
    parent: Mapped[Entity] = relationship(back_populates='relationship_attribute')
engine = create_engine('sqlite://', echo=True)
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([Entity(id=11),Entity(id=22),Entity(id=33),
                     Child(id=111,parent_id=11),Child(id=112,parent_id=11),Child(id=221,parent_id=22)])
    session.commit()
def listing(session):
    statement = select(Entity).order_by(Entity.id).limit(3)
    # TODO: statement.options(selectinload(Entity.relationship_attribute))
    parents = session.execute(statement).scalars().all()
    return [{'id':p.id, 'children':[c.id for c in p.relationship_attribute]} for p in parents]
# Run baseline and changed listing in separate fresh sessions and capture echo
# output; do not reuse already-loaded relationships when measuring the change.
if __name__ == '__main__':
    with Session(engine) as session:
        print(listing(session))
