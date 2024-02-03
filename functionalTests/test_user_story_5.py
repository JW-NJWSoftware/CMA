# Functional test to provide assurance over User Story 5 - Persona C

# This user will:
# Upload a file
# Receive a breakdown of the file from the application outlining critical information

# Possible challenges:
# The processing of the initial file uploads is critical to the success of the application as this information must be able to quickly and confidently support a user's crisis management practices.

from django.test import Client
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from time import sleep

class FileSummary(FunctionalTest):

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

        self.browser.get(self.live_server_url + "/CMA/upload_file")
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - Framework")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\FYP - Testing Material\\LSM - Crisis Management Framework.pdf")
        self.browser.find_element(By.ID, "flexSwitchCheckChecked").click()
        self.browser.find_element(By.NAME, "submit").click()

        wait = WebDriverWait(self.browser, 180)
        wait.until(EC.visibility_of_element_located((By.NAME, "files_table")), "Files table not visible")

        filesTable = self.browser.find_element(By.NAME, "files_table")
        file_name_elements = filesTable.find_elements(By.XPATH, "//td//p[@class='fw-bold mb-1']")

        # List of expected file names
        expected_file_names = ["testFile - Framework"]

        # Check if each expected file name is present in the table
        for expected_name in expected_file_names:
            found = False
            for file_name_element in file_name_elements:
                if expected_name in file_name_element.text:
                    found = True
                    break
            self.assertTrue(found, f"File name '{expected_name}' not found in the table.")

        self.browser.find_element(By.ID, "fileObjectID_testFile - Framework").click()

        fileSummary = self.browser.find_element(By.ID, "fileSummary")
        self.assertIsNotNone(fileSummary.text)


