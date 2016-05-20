# -*- coding: utf-8 -*-
from plone.restapi.services import Service
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
import jwt
import time


class Login(Service):

    # should be in keyring...
    secret = 'foobar'

    implements(IPublishTraverse)

    def reply(self):
        data = {
            'algorithm': 'HS256',
            'type': 'JWT',
            'username': 'admin',
            'fullname': 'Foo bar',
            'expires': time.time() + (60 * 60 * 12)  # 12 hour length?
        }
        return {
            'success': True,
            'token': jwt.encode(data, self.secret, algorithm='HS256')
        }


class Logout(Service):
    implements(IPublishTraverse)

    def reply(self):
        # doing nothing right now
        return {
            'success': True
        }
