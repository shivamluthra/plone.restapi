# -*- coding: utf-8 -*-
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter


class ContentGet(Service):
    """Returns a serialized content object.
    """

    def reply(self):
        serializer = queryMultiAdapter((self.context, self.request),
                                       ISerializeToJson)

        if serializer is None:
            self.request.response.setStatus(501)
            return dict(error=dict(message='No serializer available.'))

        serialized_content = serializer()

        frame = self.request.form.get('frame')
        if frame == 'object':
            doc = self._frame_response_object(serialized_content)
        else:
            doc = serialized_content
        return doc

    def _frame_response_object(self, serialized_content):

        doc = {
            'fields': serialized_content,
        }

        context_url = self.context.absolute_url()

        doc['template'] = 'index'
        doc['versions'] = {'@id': '/'.join((context_url, '@versions/'))}
        doc['workflow'] = {'@id': '/'.join((context_url, '@workflow/'))}
        doc['actions'] = {'@id': '/'.join((context_url, '@actions/'))}

        doc['@id'] = serialized_content.pop('@id')
        doc['@type'] = serialized_content.pop('@type')

        return doc
