import json
import random

from django.test import TestCase
from django.urls import reverse

from .urls import router

PREFIX  = router.prefix
APP_NAME = router.app_name


class IndexViewTests(TestCase):
    URL = reverse(f'{APP_NAME}:index')

    def test_get_method(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['Content-Type'],
            'text/html; charset=utf-8',
        )
        self.assertIn(PREFIX, self.URL)

    # POST method not allowed
    def test_post_method(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 405)
        self.assertIn(PREFIX, self.URL)


class AsyncViewTests(TestCase):
    URL = reverse(f'{APP_NAME}:async')

    def test_get_method(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['Content-Type'],
            'application/json',
        )
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            json.dumps(
                {
                    'title': '__Async__ page',
                    'content': 'This is **async** view',
                }
            ),
        )
        self.assertIn(PREFIX, self.URL)

    # POST method not allowed
    def test_post_method(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 405)
        self.assertIn(PREFIX, self.URL)


class GenericTemplateViewTests(TestCase):
    URL = reverse(f'{APP_NAME}:generic_template')
    TEMPLATE_NAME = 'template.html'

    def test_get_method(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE_NAME)
        self.assertIn(PREFIX, self.URL)

    # POST method not allowed
    def test_post_method(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 405)
        self.assertIn(PREFIX, self.URL)


class GenericRedirectViewTests(TestCase):
    URL = reverse(f'{APP_NAME}:generic_redirect')
    SUCCESS_URL = reverse(f'{APP_NAME}:generic_form')

    def test_get_method(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], self.SUCCESS_URL)
        self.assertIn(PREFIX, self.URL)

    # POST method not allowed
    def test_post_method(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 405)
        self.assertIn(PREFIX, self.URL)


class GenericFormViewTests(TestCase):
    URL = reverse(f'{APP_NAME}:generic_form')
    TEMPLATE_NAME = 'form.html'

    NAME = 'vitaliy'
    SUCCESS_URL = reverse(
        viewname=f'{APP_NAME}:hello',
        args=(NAME,)
    )

    def test_get_method(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE_NAME)
        self.assertIn('form', response.context)
        self.assertIn(PREFIX, self.URL)

    def test_post_method(self):
        response = self.client.post(self.URL, data={'name': self.NAME})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], self.SUCCESS_URL)
        self.assertIn(PREFIX, self.URL)


class HelloViewTests(TestCase):
    NAME = ''.join(
        [
            chr(random.randint(65, 90)) for _ in range(random.randint(2, 20))
        ]
    ).capitalize()
    URL = reverse(
        viewname=f'{APP_NAME}:hello',
        args=(NAME.lower(),),
    )

    def test_get_method(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.NAME, response.content.decode('utf-8'))
        self.assertIn(PREFIX, self.URL)
