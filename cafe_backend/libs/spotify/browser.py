import os
import time
from sys import platform
from selenium.webdriver import Chrome, ChromeOptions
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotVisibleException)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import ui
import selenium.webdriver.support.expected_conditions as EC
from django.conf import settings


SPOTIFY_LOGIN_PATH = 'https://accounts.spotify.com/en/login/'


class SpotifyBrowser():
    def __init__(self, *args, **kwargs):
        self.start_browser()
        self.login()

    def start_browser(self):
        if platform != 'win32' and not settings.DEBUG:
            self.display = Display(visible=0, size=(1200, 900))
            self.display.start()

        if platform == 'darwin':
            chromedriver = os.path.join(
                settings.BASE_DIR, 'storage/chromedriver_mac')
        elif platform == 'win32':
            chromedriver = os.path.join(
                settings.BASE_DIR, 'storage/chromedriver.exe')
        else:
            chromedriver = os.path.join(
                settings.BASE_DIR, 'storage/chromedriver_linux')

        options = ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1200,900")
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--js-flags="--max_old_space_size=4096"')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        try:
            self.driver = Chrome(chromedriver, chrome_options=options)
        except Exception as e:
            if self.driver:
                self.driver.quit()
            raise NotImplementedError(str(e))

    def open(self, url, wait=1):
        self.driver.get(url)
        time.sleep(wait)

    def login(self):
        # username = settings.SPOTIFY_USERNAME
        # password = settings.SPOTIFY_PASSWORD
        self.open(SPOTIFY_LOGIN_PATH)

        username = self.driver.find_element_by_id('login-username')
        password = self.driver.find_element_by_id('login-password')
        login_button = self.driver.find_element_by_id('login-button')

        username.send_keys(settings.SPOTIFY_USERNAME)
        password.send_keys(settings.SPOTIFY_PASSWORD)
        login_button.click()

    def wait_for_elements(self, selectors, by=By.CSS_SELECTOR):
        wait = ui.WebDriverWait(self.driver, 10)
        for selector in selectors:
            try:
                wait.until(EC.visibility_of_element_located((by, selector)))
            except Exception as e:
                print(str(e))
                return False
        return True

    def add_music_to_playlist(self, music_url):
        PLAYLIST_DROPDOWN_BUTTON =\
            'ol.tracklist div.react-contextmenu-wrapper \
                li.tracklist-row--active button div'
        ADD_TO_PLAYLIST_ITEM =\
            '.react-contextmenu.react-contextmenu--visible \
            div.react-contextmenu-item'
        FIRST_PLAYLIST_ITEM = 'div.dialog div.GlueDropTarget div.media-object'
        self.open(music_url)
        actions = ActionChains(self.driver)

        self.wait_for_elements([
            'ol.tracklist div.react-contextmenu-wrapper \
                li.tracklist-row--active'
        ])
        # time.sleep(10)
        active_line = self.driver.find_element_by_css_selector(
            'ol.tracklist div.react-contextmenu-wrapper li.tracklist-row--active')
        actions.move_to_element(active_line).perform()

        self.wait_for_elements([PLAYLIST_DROPDOWN_BUTTON])
        self.driver.find_element_by_css_selector(
            'ol.tracklist div.react-contextmenu-wrapper li.tracklist-row--active button div').click()

        # time.sleep(1)
        self.wait_for_elements([ADD_TO_PLAYLIST_ITEM])
        self.driver.find_elements_by_css_selector(
            ADD_TO_PLAYLIST_ITEM)[2].click()

        # time.sleep(1)
        self.wait_for_elements([FIRST_PLAYLIST_ITEM])
        self.driver.find_element_by_css_selector(FIRST_PLAYLIST_ITEM).click()

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
