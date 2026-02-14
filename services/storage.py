from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class PipelineResult(Base):
    __tablename__ = "results"
    id = Column(String, primary_key=True)
    uuid = Column(String)
    analysis = Column(Text)
    sentiment = Column(String)
    timestamp = Column(String)
    source = Column(String)

Base.metadata.create_all(engine)

def store_result(uuid, analysis, sentiment, timestamp, source):
    session = Session()
    record = PipelineResult(
        id=uuid,
        uuid=uuid,
        analysis=analysis,
        sentiment=sentiment,
        timestamp=timestamp,
        source=source
    )
    session.add(record)
    session.commit()
    session.close()
