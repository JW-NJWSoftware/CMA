from django.test import TestCase
from django.http import HttpRequest
from CMAfile.models import CMDoc


class FileHomePageViewTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/CMAfile/")
        self.assertTemplateUsed(response, "CMAfile_home.html")
