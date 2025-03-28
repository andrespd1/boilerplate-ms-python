from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from boilerplate_ms_python.config.db_client import Base


class StubModel(Base):
    __tablename__ = "stub_table_python"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
