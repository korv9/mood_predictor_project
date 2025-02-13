"""import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# LÄGG TILL ALTERNATIV FÖR DB URL
def pytest_addoption(parser):
    parser.addoption('--dburl',
                     action='store',
                     default='sqlite:///:memory:',
                     help='URL TILL DATABASEN FÖR TESTER')

# SKAPA EN SQLALCHEMY ENGINE OCH RENSAD EFTER SESSION
@pytest.fixture(scope='session')
def db_engine(request):
    db_url = request.config.getoption("--dburl")
    engine_ = create_engine(db_url, echo=True)
    yield engine_
    engine_.dispose()

# SKAPA EN SKOPAD SESSIONFABRIK
@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))

# SKAPA EN NY SESSION FÖR VARJE TEST OCH ROLLBACKA EFTER TESTET
@pytest.fixture(scope='function')
def db_session(db_session_factory):
    session_ = db_session_factory()
    yield session_
    session_.rollback()
    session_.close()"""