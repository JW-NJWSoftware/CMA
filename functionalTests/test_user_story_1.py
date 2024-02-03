# Functional test to provide assurance over User Story 1 - Persona A

# This user will:
# Open the URL for their files page.
# Be presented with their previously uploaded files.
# Select a file to gain a detailed view of it.
# Open a second file.
# Download the second file and sign out of the application.

# Possible challenges:
# The user may not be signed in so directly accessing the file page should redirect them to login.
# If required to login, any mistakes should be caught and explained to the user.

from django.test import Client
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
import time
from time import sleep

class FileManagement(FunctionalTest):

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

        self.browser.get(self.live_server_url + "/CMA")
        textBox = self.browser.find_element(By.ID, "noFilesText")
        self.assertIn("No files have been uploaded.", textBox.text)

        self.browser.get(self.live_server_url + "/CMA/upload_file")
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - testDoc")
        self.browser.find_element(By.ID, "id_desc").send_keys("This is an example description for the testDoc.")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\TestDocument.txt")
        self.browser.find_element(By.NAME, "submit").click()

        self.browser.get(self.live_server_url + "/CMA/upload_file")
        self.browser.find_element(By.ID, "id_fileName").send_keys("testFile - Framework")
        self.browser.find_element(By.ID, "id_file").send_keys("C:\\Users\\Jake\\Desktop\\FYP - Testing Material\\LSM - Crisis Management Framework.pdf")
        self.browser.find_element(By.NAME, "submit").click()

        self.browser.get(self.live_server_url + "/CMA")
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

        self.browser.get(self.live_server_url + "/CMA")
        self.browser.find_element(By.ID, "fileObjectID_testFile - Framework").click()

        downloadButton = self.browser.find_element(By.ID, "submitDownload")
        self.browser.execute_script("arguments[0].scrollIntoView();", downloadButton)
        downloadButton.click()

        wait = WebDriverWait(self.browser, 10)

        download_path = "C:\\Users\\Jake\\Downloads"
        file_name = "LSM_-_Crisis_Management_Framework.pdf"
        downloaded_file_path = os.path.join(download_path, file_name)

        wait.until(lambda x: os.path.exists(downloaded_file_path), "File download timeout")

        self.assertTrue(os.path.exists(downloaded_file_path), "File not found in the expected location")

        os.remove(downloaded_file_path)

        