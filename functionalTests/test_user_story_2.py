# Functional test to provide assurance over User Story 2 - Persona A

# This user will:
# Login to the application.
# Open the crisis management chatbot.
# Input the type of crisis and relevant information.
# Request the application to guide them through the necessary steps to respond to the ongoing crisis.
# Running through the crisis response the user will supply a number of questions, confirmations and additional information to the application.

# Possible challenges:
# The uploaded crisis management documentation may not be able to provide a complete overview of the information required for the crisis response.
# If a crisis takes place over a number of days, the user will want their previous progress with the application to be saved in a state that can be quickly returned to.


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
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - Framework")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\FYP - Testing Material\\LSMCrisisManagementFramework.txt")
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
        expected_file_names = ["testFile - Framework"]

        # Check if each expected file name is present in the table
        for expected_name in expected_file_names:
            found = False
            for context_name_element in context_name_elements:
                if expected_name in context_name_element.text:
                    found = True
                    break
            self.assertTrue(found, f"Context name '{expected_name}' not found in the table.")
        
        self.browser.find_element(By.ID, "question_value").send_keys("A ransomware attack has occured at a supplier for LSM. The communications team need to be stood up to handle internal communications to warn employees not to answer emails from the supplier. Who is responsible for this?")
        self.browser.find_element(By.ID, "flexSwitchCheckChecked").click()
        self.browser.find_element(By.ID, "submitQuestion").click()

        wait = WebDriverWait(self.browser, 180)
        wait.until(EC.visibility_of_element_located((By.NAME, "question")), "Question not visible")

        answer_element = self.browser.find_element(By.NAME, "answer")
        self.assertIsNotNone(answer_element.text)

        justification_element = self.browser.find_element(By.NAME, "justification")
        self.assertIsNotNone(justification_element.text)