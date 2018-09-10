# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from domains.models.operator import Operator
from domains.models.user import User


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, identify: int) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_users(self) -> [User]:
        raise NotImplementedError
    
    @abstractmethod
    def get_operators(self) -> [Operator]:
        raise NotImplementedError

    @abstractmethod
    def append_user(self, login_id: str, password: str, name: str, role: int):
        raise NotImplementedError

    @abstractmethod
    def get_role(self, identity: int):
        raise NotImplementedError

    @abstractmethod
    def get_roles(self):
        raise NotImplementedError

    @abstractmethod
    def get_skills(self):
        raise NotImplementedError
