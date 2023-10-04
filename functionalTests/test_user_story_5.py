# Functional test to provide assurance over User Story 5 - Persona C

# This user will:
# Upload a file
# Receive a breakdown of the file from the application outlining critical information
# Affirm if this information is correct; or, the user will be able to edit the breakdown of the files to accurately reflect their crisis management principles and practices.
# Receive confirmation that this breakdown is saved.
# Reopen this application specific format of the file.
# Make an additional change and resave the file.


# Possible challenges:
# The processing of the initial file uploads is critical to the success of the application as this information must be able to quickly and confidently support a user's crisis management practices.

from .base import FunctionalTest
from selenium.webdriver.common.by import By

