from django.test import TestCase
from CMAfile.forms import CMDocForm
from CMAfile.models import CMDoc


class CMDocFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = CMDocForm()
        self.assertIn('placeholder="Enter a name for your file"', form.as_p())
        self.assertIn('class="form-control form-control-lg"', form.as_p())
