import unittest
from unittest.mock import patch, MagicMock
from services.marangatu_scraper.marangatu import MarangatuBot, SendAnulados
from selenium.common.exceptions import TimeoutException

@patch('services.marangatu_scraper.marangatu.webdriver.Firefox')
class TestMarangatuScraper(unittest.TestCase):

    def test_login_success(self, mock_firefox):
        mock_browser = mock_firefox.return_value
        mock_user_input = MagicMock()
        mock_password_input = MagicMock()
        
        with patch('services.marangatu_scraper.marangatu.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            mock_wait_instance.until.side_effect = [mock_user_input, mock_password_input]
            
            bot = MarangatuBot(username='12345', password='password123')
            bot.bot = mock_browser
            bot.login()
            
            mock_browser.get.assert_called_with('https://marangatu.set.gov.py/eset/login')
            mock_user_input.send_keys.assert_called_with('12345')
            mock_password_input.send_keys.assert_any_call('password123')

    def test_login_timeout_creates_screenshot(self, mock_firefox):
        mock_browser = mock_firefox.return_value
        with patch('services.marangatu_scraper.marangatu.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            mock_wait_instance.until.side_effect = TimeoutException("Element not found")
            
            bot = MarangatuBot(username='12345', password='password123')
            bot.bot = mock_browser

            with patch.object(bot, 'save_error_screenshot') as mock_screenshot:
                bot.login()
                mock_screenshot.assert_called_with('error_login.png')
                mock_browser.close.assert_called_once()

@patch('services.marangatu_scraper.marangatu.webdriver.Firefox')
class TestSendAnulados(unittest.TestCase):

    def test_timbrado_input(self, mock_firefox):
        mock_browser = mock_firefox.return_value
        mock_input = MagicMock()
        mock_button = MagicMock()
        
        with patch('services.marangatu_scraper.marangatu.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            mock_wait_instance.until.side_effect = [mock_input, mock_button]
            
            bot = SendAnulados(username='12345', password='password123')
            bot.bot = mock_browser
            bot.timbrado_input('12345678')
            
            mock_input.send_keys.assert_any_call('12345678')
            mock_button.click.assert_called_once()

    def test_timbrado_input_failure(self, mock_firefox):
        mock_browser = mock_firefox.return_value
        with patch('services.marangatu_scraper.marangatu.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            mock_wait_instance.until.side_effect = Exception("General error")
            
            bot = SendAnulados(username='12345', password='password123')
            bot.bot = mock_browser

            with patch.object(bot, 'save_error_screenshot') as mock_screenshot:
                with patch.object(bot, 'logout') as mock_logout:
                    bot.timbrado_input('12345678')
                    mock_screenshot.assert_called_with('error_timbrado.png')
                    mock_logout.assert_called_once()

if __name__ == '__main__':
    unittest.main()
