# Functional test to provide assurance over User Story 2 - Persona A

# This user will:
# Login to the application.
# Open the crisis management chatbot.
# Input the type of crisis and relevant information.
# Request the application to guide them through the necessary steps to respond to the ongoing crisis.
# Running through the crisis response the user will supply a number of questions, confirmations and additional information to the application.
# The application will dynamically respond to this information to optimise the response activities and ensure every impact is considered and managed.


# Possible challenges:
# The uploaded crisis management documentation may not be able to provide a complete overview of the information required for the crisis response.
# If a crisis takes place over a number of days, the user will want their previous progress with the application to be saved in a state that can be quickly returned to.


from .base import FunctionalTest
from selenium.webdriver.common.by import By