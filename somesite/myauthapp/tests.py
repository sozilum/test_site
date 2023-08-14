from django.urls import reverse_lazy, reverse
from django.test import TestCase
import json


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse_lazy('authapp:cookie-get'), HTTP_USER_AGENT = 'MOZILA')
        self.assertContains(response, "Cookie value")


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse_lazy('authapp:foo-bar'), HTTP_USER_AGENT = 'MOZILA')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json',)
        expected_data = {'foo': 'bar', 'spam':'eggs'}
        self.assertJSONEqual(response.content, expected_data)