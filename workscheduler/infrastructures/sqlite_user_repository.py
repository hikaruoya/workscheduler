# -*- coding: utf-8 -*-

from domains.models.operator import Operator
from domains.models.user import User
from domains.models.role import Role
from domains.models.user_repository import UserRepository
from infrastructures.sqlite_repository import SqliteRepository


class SqliteUserRepository(SqliteRepository, UserRepository):
    def __init__(self, connect_string: str):
        super().__init__(connect_string)
    
    def get_user(self, identify: int) -> User:
        user = self._select('select id, login_id, password, name, role from users where id == ? order by id asc',
                            identify)
        if not user:
            return None
        role = self.get_role(user[0]["role"])
        return User(user[0]["id"], user[0]['login_id'], user[0]['password'], user[0]['name'], role)
    
    def get_users(self) -> [User]:
        users = self._select('select id, login_id, password, name, role from users order by id asc')
        roles = self.get_roles()
        
        def find_role(role_id):
            return next(filter(lambda x: x.id == role_id, roles), None)
        return [User(x['id'], x['login_id'], x['password'], x['name'], find_role(x['role'])) for x in users]
    
    def append_user(self, login_id: str, password: str, name: str, role: int):
        with self.con.get_db() as db:
            db.execute('insert into users (login_id, password, name, role) values (?, ?, ?, ?)',
                       [login_id, password, name, role])
            db.commit()
    
    def get_operators(self) -> [Operator]:
        raise NotImplementedError

    def get_role(self, identity: int) -> Role:
        role = self._select('select id, name, is_admin from roles where id == ? order by id asc',
                            identity)
        return Role(role[0]['id'], role[0]['name'], role[0]['is_admin']) if role else None

    def get_roles(self) -> [Role]:
        roles = self._select('select id, name, is_admin from roles order by id asc')
        return [Role(x['id'], x['name'], x['is_admin']) for x in roles]
    
    def append_role(self, name: str, is_admin: bool):
        with self.con.get_db() as db:
            db.execute('insert into roles (name, is_admin) values (?, ?)',
                       [name, is_admin])
            db.commit()
    
    def get_skills(self):
        raise NotImplementedError
