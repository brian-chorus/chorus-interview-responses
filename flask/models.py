import enum
from sqlalchemy import create_engine, Column, Integer, String, Enum, TIMESTAMP, Boolean, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from db import db  # Import db instance

Base = declarative_base()

class CadenceEnum(enum.Enum):
    daily = 'DAILY'
    weekly = 'WEEKLY'
    monthly = 'MONTHLY'

class OccurrenceStatusEnum(enum.Enum):
    not_started = 'NOT_STARTED'
    in_progress = 'IN_PROGRESS'
    completed = 'COMPLETED'

class Worker(db.Model):
    __tablename__ = 'Worker'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String(255), nullable=False, comment='Worker full name')
    active = Column(Boolean, default=True, comment='Whether the worker is active')
    created_at = Column(TIMESTAMP, server_default=text("now()"))

class Task(db.Model):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='Task name')
    cadence = Column(Enum(CadenceEnum, name='cadence_enum'), nullable=False, comment='A task can reoccur at a cadence of daily, weekly, monthly')
    occurrences = Column(Integer, nullable=False, comment='A task will repeat at a cadence and complete after x occurrences')
    initialized_at = Column(TIMESTAMP, nullable=True, comment='The task will begin on a certain date and time')
    created_at = Column(TIMESTAMP, server_default=text("now()"))

class Occurrence(db.Model):
    __tablename__ = 'Occurrence'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('Task.id'), nullable=False)
    occurrence_timestamp = Column(TIMESTAMP, nullable=False, comment='This will be populated by a script to indicate when an occurrence needs to happen')
    occurrence_status = Column(Enum(OccurrenceStatusEnum, name='occurrence_status_enum'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("now()"))

class OccurrenceAssignment(db.Model):
    __tablename__ = 'OccurrenceAssignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_worker_id = Column(UUID(as_uuid=True), ForeignKey('Worker.id'), nullable=False, comment='Multiple people can work on an Occurrence')
    occurrence_id = Column(Integer, ForeignKey('Occurrence.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("now()"))

# Example usage
DATABASE_URL = "postgresql://user:password@db-service:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
