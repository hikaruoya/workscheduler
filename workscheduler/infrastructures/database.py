# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, sql_connection, echo=False):
        self._engine = create_engine(sql_connection, echo=echo)

    def init(self):
        self.drop()
        import workscheduler.domains.models as models
        models.Base.metadata.create_all(bind=self._engine)

        # set initial users and roles
        from workscheduler.domains.models.user import UserFactory
        from workscheduler.infrastructures.user_repository import UserRepository

        session = self.create_session()
        user_repository = UserRepository(session)

        user_repository.store_user(UserFactory.new_user('admin', 'minAd', '管理者', is_admin=True, is_operator=False))
        user_repository.store_user(UserFactory.new_user('user', 'user', 'ユーザ', is_admin=False, is_operator=True))

        session.commit()

    def create_session(self):
        session = sessionmaker(bind=self._engine)
        return session()

    def drop(self):
        import workscheduler.domains.models as models
        models.Base.metadata.drop_all(self._engine)