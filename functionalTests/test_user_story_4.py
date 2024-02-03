# Functional test to provide assurance over User Story 4 - Persona C

# This user will:
# Connect to the application home page.
# Locate a create account function and access this.
# Input a username for their client and a temporary password.
# Login to their newly created account.
# Upload crisis documents received from their client.
# Confirm that these files have been uploaded.
# At a later date, share the account details so the client can login to this account.
# They will then change the account password.


# Possible challenges:
# The user account details input may be invalid or in use by existing users.
# Incorrect files could be uploaded, either in irrelevant content or unacceptable formats


from django.test import Client
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
import time
from time import sleep

class FileManagement(FunctionalTest):
    def setUp(self):
        # Assuming you have initialized your webdriver
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def test_can_view_files(self):
        # Register user
        self.browser.get(self.live_server_url + "/")

        self.browser.find_element(By.ID, "signinButton").click()
        self.browser.find_element(By.ID, "registerLink").click()
        
        self.browser.find_element(By.ID, "username").send_keys("testuser")
        self.browser.find_element(By.ID, "email").send_keys("testuser@example.com")
        self.browser.find_element(By.ID, "password1").send_keys("TempTestPassword123")
        self.browser.find_element(By.ID, "password2").send_keys("TempTestPassword123")
        self.browser.find_element(By.ID, "id_ToS").click()

        self.browser.find_element(By.NAME, "submit").click()

        self.browser.find_element(By.ID, "id_username").send_keys("testuser")
        self.browser.find_element(By.ID, "id_password").send_keys("TempTestPassword123")

        self.browser.find_element(By.NAME, "submit").click()

        self.browser.find_element(By.ID, "navbarFilesButton").click()

        self.browser.find_element(By.ID, "uploadFileButton").click()
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - testDoc")
        self.browser.find_element(By.ID, "id_desc").send_keys("This is an example description for the testDoc.")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\TestDocument.txt")
        self.browser.find_element(By.NAME, "submit").click()

        self.browser.find_element(By.ID, "uploadFileButton").click()
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - Framework")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\FYP - Testing Material\\LSM - Crisis Management Framework.pdf")
        self.browser.find_element(By.NAME, "submit").click()

        filesTable = self.browser.find_element(By.NAME, "files_table")
        file_name_elements = filesTable.find_elements(By.XPATH, "//td//p[@class='fw-bold mb-1']")

        # List of expected file names
        expected_file_names = ["testFile - Framework", "testFile - testDoc"]

        # Check if each expected file name is present in the table
        for expected_name in expected_file_names:
            found = False
            for file_name_element in file_name_elements:
                if expected_name in file_name_element.text:
                    found = True
                    break
            self.assertTrue(found, f"File name '{expected_name}' not found in the table.")

        self.browser.find_element(By.ID, "fileObjectID_testFile - testDoc").click()

        desc = self.browser.find_element(By.NAME, "fileDesc")
        self.assertIn("This is an example description for the testDoc.", desc.text)

        self.browser.find_element(By.ID, "fileViewSwitch").click()

        embed_element = self.browser.find_element(By.TAG_NAME, "embed")

        # Assert that the <embed> element is present on the page
        self.assertIsNotNone(embed_element, "Embed element not found on the page")

        self.browser.find_element(By.ID, "usernameSpan").click()
        self.browser.find_element(By.ID, "navbarProfileButton").click()
        self.browser.find_element(By.ID, "id_old_password").send_keys("TempTestPassword123")
        self.browser.find_element(By.ID, "id_new_password1").send_keys("TestPassword123")
        self.browser.find_element(By.ID, "id_new_password2").send_keys("TestPassword123")
        self.browser.find_element(By.NAME, "change_password").click()

        self.browser.find_element(By.ID, "usernameSpan").click()
        self.browser.find_element(By.ID, "navbarSignoutButton").click()
        self.browser.find_element(By.NAME, "submit").click()

        self.browser.find_element(By.ID, "signinButton").click()

        self.browser.find_element(By.ID, "id_username").send_keys("testuser")
        self.browser.find_element(By.ID, "id_password").send_keys("TestPassword123")

        self.browser.find_element(By.NAME, "submit").click()

        self.browser.find_element(By.ID, "navbarFilesButton").click()

        filesTable = self.browser.find_element(By.NAME, "files_table")
        file_name_elements = filesTable.find_elements(By.XPATH, "//td//p[@class='fw-bold mb-1']")

        # List of expected file names
        expected_file_names = ["testFile - Framework", "testFile - testDoc"]

        # Check if each expected file name is present in the table
        for expected_name in expected_file_names:
            found = False
            for file_name_element in file_name_elements:
                if expected_name in file_name_element.text:
                    found = True
                    break
            self.assertTrue(found, f"File name '{expected_name}' not found in the table.")


        
