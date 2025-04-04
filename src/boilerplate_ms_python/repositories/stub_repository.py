from boilerplate_ms_python.config.db_client import with_session
from boilerplate_ms_python.models.stub_model import StubModel


class StubRepository:
    @with_session
    def get_first_stub(self, *, session):
        return session.query(StubModel).first()
