from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'contabot.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, 
    echo=False,
    connect_args={'check_same_thread': False, 'timeout': 30}
)

# Habilitar WAL (Write-Ahead Logging) para permitir lecturas mientras se insertan millones de RUCs
from sqlalchemy import event
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

metadata = MetaData()

Base = declarative_base()


class TimbradosModel(Base):
    __tablename__ = 'timbrados'

    id = Column(Integer, primary_key=True)
    timbrado_number = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    numero_inicio = Column(String(255), nullable=False)
    numero_fin = Column(String(255), nullable=False)
    end_date = Column(Date, nullable=False)


class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_bot = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)  # True por defecto para no romper flujos actuales
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class GroupsModel(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    title = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)  # True por defecto
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MessagesModel(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    from_user_id = Column(Integer, nullable=False)
    text = Column(String)
    date = Column(DateTime, nullable=False)


class ContribuyenteModel(Base):
    __tablename__ = 'contribuyentes'

    id = Column(Integer, primary_key=True)
    ci = Column(String(50), index=True)      # Agregado índice para búsquedas instantáneas
    ruc = Column(String(50), index=True)     # Agregado índice para búsquedas instantáneas
    dv = Column(String(10))
    fullname = Column(String(255))
    status = Column(String(100))


Session = sessionmaker(bind=engine)
from sqlalchemy.orm import scoped_session
session = scoped_session(Session)

Base.metadata.create_all(bind=engine)
