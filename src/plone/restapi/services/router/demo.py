# -*- coding: utf-8 -*-
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from plone.rest.interfaces import IServiceRouter
from plone.rest.service import ServiceRouter
from plone.rest.service import IRouteInfo
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from zope.component.hooks import getSite
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse

DEFAULT_SEARCH_RESULTS_LIMIT = 25


class IDemoRouter(IServiceRouter):

    pass


class DemoRouter(ServiceRouter):

    implements(IDemoRouter)


class DemoGet(Service):
    '''Demo getter for a user info'''

    doc = 'Return the user info'
    def reply(self):
        return {'parameters': IRouteInfo(self.request).parameters()}


class DemoList(Service):

    doc = 'List users'

    def reply(self):
        return {'users': {'@id': 'users/foo/info'}}
