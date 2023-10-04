# Functional test to provide assurance over User Story 3 - Persona B

# This user will:
# Login to the application.
# Open the crisis management chatbot.
# Input the type of crisis and relevant information.
# Input a decision with a question to the chatbot around verifying the accuracy of said decision.
# Be presented with a confirmation of the decision and the relevant reference to their uploaded crisis management documents to provide evidence for the decision.


# Possible challenges:
# The user account may be a member of a group of accounts that is not the account used to originally upload documents.
# The decision made may be correct or incorrect and the application should demonstrate a capability to distinguish and demonstrate this.


from .base import FunctionalTest
from selenium.webdriver.common.by import By