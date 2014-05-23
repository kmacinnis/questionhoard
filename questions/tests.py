from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest


from zother.views import main_page
# from handling import condense_list_of_dicts


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, main_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = main_page(request)
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title> Massive Question Hoard | Main Page</title>',
                response.content)
        self.assertTrue(response.content.endswith(b'</html>'))








# Handling Tests

def test_condense_list_of_dicts():
    pass

