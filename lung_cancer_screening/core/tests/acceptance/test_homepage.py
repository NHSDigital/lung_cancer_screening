from django.test import TestCase, Client

class TestHomepage(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_displays_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello world")
