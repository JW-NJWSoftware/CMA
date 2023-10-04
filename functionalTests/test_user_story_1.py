# Functional test to provide assurance over User Story 1 - Persona A

# This user will:
# Open the URL for their files page.
# Be presented with their previously uploaded files.
# Select a file to gain a detailed view of it.
# Press the download button to retrieve a local copy of the file.
# Open a second file.
# Download the second file and sign out of the application.

# Possible challenges:
# The user may not be signed in so directly accessing the file page should redirect them to login.
# If required to login, any mistakes should be caught and explained to the user.

from .base import FunctionalTest
from selenium.webdriver.common.by import By

class FileManagement(FunctionalTest):

    def test_can_view_files(self):
        pass