# Functional test to provide assurance over User Story 4 - Persona C

# This user will:
# Connect to the application home page.
# Locate a create account function and access this.
# Input a username for their client and a temporary password.
# Login to their newly created account.
# Upload crisis documents received from their client.
# Receive confirmation that these files have been uploaded.
# At a later date, share the account details so the client can login to this account.
# They will then change the account password.


# Possible challenges:
# The user account details input may be invalid or in use by existing users.
# Incorrect files could be uploaded, either in irrelevant content or unacceptable formats


from .base import FunctionalTest
from selenium.webdriver.common.by import By