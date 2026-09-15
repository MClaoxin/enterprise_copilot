from sqlalchemy.orm import Session


class UnitOfWork:
    """Owns the transaction boundary for a single service operation."""

    def __init__(self, db: Session):
        self.db = db

    def commit(self) -> None:
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, instance: object) -> None:
        self.db.refresh(instance)
