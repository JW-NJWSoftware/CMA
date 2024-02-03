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


from django.test import Client
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from time import sleep

class ChatManagement(FunctionalTest):

    def test_can_view_files(self):
        # Register user
        self.browser.get(self.live_server_url + "/auth/register")
        
        self.browser.find_element(By.ID, "username").send_keys("testuser")
        self.browser.find_element(By.ID, "email").send_keys("testuser@example.com")
        self.browser.find_element(By.ID, "password1").send_keys("TestPassword123!")
        self.browser.find_element(By.ID, "password2").send_keys("TestPassword123!")
        self.browser.find_element(By.ID, "id_ToS").click()

        self.browser.find_element(By.NAME, "submit").click()


        #attempt to access files, should redirect to login
        self.browser.get(self.live_server_url + "/CMA")

        self.browser.find_element(By.ID, "id_username").send_keys("testuser")
        self.browser.find_element(By.ID, "id_password").send_keys("TestPassword123!")

        self.browser.find_element(By.NAME, "submit").click()

        self.browser.find_element(By.ID, "navbarChatsButton").click()
        textBox = self.browser.find_element(By.ID, "noChatsText")
        self.assertIn("No chats have been created.", textBox.text)

        self.browser.get(self.live_server_url + "/CMA/upload_file")
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - PIR")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\FYP - Testing Material\\LSMPIRMar2023.txt")
        self.browser.find_element(By.ID, "flexSwitchCheckChecked").click()
        self.browser.find_element(By.NAME, "submit").click()

        wait = WebDriverWait(self.browser, 180)
        wait.until(EC.visibility_of_element_located((By.NAME, "files_table")), "Files table not visible")

        self.browser.find_element(By.ID, "navbarChatsButton").click()

        self.browser.find_element(By.ID, "chat_name").send_keys("testChat")
        self.browser.find_element(By.ID, "createChatSubmit").click()

        contextTable = self.browser.find_element(By.ID, "contextTable")
        context_name_elements = contextTable.find_elements(By.NAME, "contextFileName")

        # List of expected file names
        expected_file_names = ["testFile - PIR"]

        # Check if each expected file name is present in the table
        for expected_name in expected_file_names:
            found = False
            for context_name_element in context_name_elements:
                if expected_name in context_name_element.text:
                    found = True
                    break
            self.assertTrue(found, f"Context name '{expected_name}' not found in the table.")
        
        self.browser.find_element(By.ID, "question_value").send_keys("What attack occured in this Post Incident Review?")
        self.browser.find_element(By.ID, "flexSwitchCheckChecked").click()
        self.browser.find_element(By.ID, "submitQuestion").click()

        wait = WebDriverWait(self.browser, 180)
        wait.until(EC.visibility_of_element_located((By.NAME, "question")), "Question not visible")

        answer_element = self.browser.find_element(By.NAME, "answer")
        self.assertIn("ransomware", answer_element.text)

        justification_element = self.browser.find_element(By.NAME, "justification")
        self.assertIsNotNone(justification_element.text)