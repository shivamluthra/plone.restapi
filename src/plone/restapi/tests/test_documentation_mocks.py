# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
from plone.restapi.testing import RelativeSession
from plone.testing.z2 import Browser
from plone.uuid.interfaces import IMutableUUID

import json
import os
import unittest2 as unittest


REQUEST_HEADER_KEYS = [
    'accept'
]

RESPONSE_HEADER_KEYS = [
    'content-type',
    'allow',
]

base_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    '..',
    '..',
    'docs/source/_json'
)


def save_response_for_documentation(filename, response):
    f = open('{}/{}'.format(base_path, filename), 'w')
    request = response.request
    request_contents = '{} {}\n'.format(
        request.method,
        request.path_url,
    )

    for key, value in request.headers.items():
        if key.lower() in REQUEST_HEADER_KEYS:
            request_contents += '{}: {}\n'.format(key, value)

    if request.body:
        request_contents += '\n{}\n'.format(request.body)

    f.write(request_contents)
    f.write('\n')

    f.write('HTTP {} {}\n'.format(response.status_code, response.reason))
    for key, value in response.headers.items():
        if key.lower() in RESPONSE_HEADER_KEYS:
            f.write('{}: {}\n'.format(key.lower(), value))
    f.write('\n')
    f.write(response.content)
    f.close()


class TestTraversal(unittest.TestCase):

    layer = PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='front-page')
        self.document = self.portal['front-page']
        self.document.title = u"Welcome to Plone"
        self.document.description = \
            u"Congratulations! You have successfully installed Plone."
        self.document.text = RichTextValue(
            u"If you're seeing this instead of the web site you were " +
            u"expecting, the owner of this web site has just installed " +
            u"Plone. Do not contact the Plone Team or the Plone mailing " +
            u"lists about this.",
            'text/plain',
            'text/html'
        )
        self.document.creation_date = DateTime('2016-01-21T01:14:48+00:00')
        IMutableUUID(self.document).set('1f699ffa110e45afb1ba502f75f7ec33')
        self.document.reindexObject()
        self.document.modification_date = DateTime('2016-01-21T01:24:11+00:00')
        import transaction
        transaction.commit()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_documentation_theme(self):
        query = {'resource': '/style/main.css'}
        response = self.api_session.get('/@theme', params=query)
        save_response_for_documentation('theme.json', response)

    def test_documentation_components_navigation(self):
        response = self.api_session.get('/@components/navigation')
        save_response_for_documentation(
            'components_navigation.json', response)

    def test_documentation_components_breadcrumbs(self):
        response = self.api_session.get('/front-page/@components/breadcrumbs')
        save_response_for_documentation(
            'components_breadcrumbs.json', response)

    def test_documentation_actions(self):
        response = self.api_session.get('/@actions')
        save_response_for_documentation('actions.json', response)

    def test_documentation_frame_object(self):
        response = self.api_session.get(
            self.document.absolute_url() + '?frame=object')
        save_response_for_documentation('frame_object.json', response)

    def test_documentation_login(self):
        response = self.api_session.post('/@login', data=json.dumps({
            'username': 'admin',
            'password': 'admin'
        }))
        save_response_for_documentation('login.json', response)
