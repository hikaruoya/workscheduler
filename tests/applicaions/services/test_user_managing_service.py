# -*- coding: utf-8 -*-

from workscheduler.applications.services.user_query import UserQuery


class TestUserManagingService:
    def test_store_new_user(self, user_managing_service, session):
        user_repository = UserQuery(session)
        count = len(user_repository.get_users())
        user_managing_service.join_a_member('test1', 'test1pass', 'テスト１', True, True, )
        session.commit()
        assert count + 1 == len(user_repository.get_users())
        user_managing_service.join_a_member('test2', 'test2pass', 'テスト２', False, False)
        session.commit()
        assert count + 2 == len(user_repository.get_users())
        
    def test_store_update_user(self, user_managing_service, session):
        user_repository = UserQuery(session)
        users = user_repository.get_users()
        count = len(users)
        user = users[0]
        user_managing_service.renew_user(user.id, user.login_id + '-u',
                                         user.name + '-u', user.is_admin, user.is_operator)
        session.commit()
        assert count == len(user_repository.get_users())
