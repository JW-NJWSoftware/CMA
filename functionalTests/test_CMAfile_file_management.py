from .base import FunctionalTest
from selenium.webdriver.common.by import By
import time


class FileManagement(FunctionalTest):

    def test_can_upload_a_file(self):
        # Client A has recently heard of the new CMA
        # Client A decides to visit the site and try to store their Crisis documentation

        # They go to the homepage of the app
        self.browser.get(self.live_server_url + "/CMA")

        # They notice the page title and header mention the name of the CMA
        self.assertIn("Crisis Management Assistant", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Crisis Management Assistant", header_text)

        # They are invited to upload a file to store their documentation
        submit_button = self.browser.find_element(By.NAME, "submit")
        self.assertIn("Upload", submit_button.text)

        # They enter a file into the file selector box
        file_selection = self.browser.find_element(By.ID, "id_file")
        file_selection.send_keys("C:\\Users\\Jake\\Desktop\\TestDocument.txt")

        # They enter a name for the file
        self.browser.find_element(By.ID, "id_fileName").send_keys("Test Document Name")

        # They press the submit button
        submit_button.click()

        # The server then shows the file as uploaded
        self.wait_for_file_upload('Test Document Name')
