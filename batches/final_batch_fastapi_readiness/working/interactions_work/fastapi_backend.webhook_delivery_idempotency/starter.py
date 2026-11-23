from sqlalchemy import String, Integer, UniqueConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
class Base(DeclarativeBase):
    pass
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
class ProcessedEvent(Base):
    __tablename__ = 'processed_events'
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_event_id: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('publisher_event_id'),)
async def handle_authenticated_event(event, session):
    # TODO: event record and order update inside one session.begin transaction.
    # Confirm already processed identity before acknowledging a duplicate;
    # never translate unrelated IntegrityError into successful processing.
    raise NotImplementedError('Complete atomic persistent deduplication')
# application.py supplies request-scoped sessions and durable storage.
# The request-local SQLAlchemy after_flush_postexec hook injects failure
# before commit; no extra learner failure switch or verifier is needed.
