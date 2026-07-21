import logging
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

logger = logging.getLogger(__name__)

MOTIVO = 'ANULACION'

class MarangatuBot:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        
        selenium_url = os.environ.get('SELENIUM_URL')
        if selenium_url:
            options = webdriver.FirefoxOptions()
            self.bot = webdriver.Remote(command_executor=selenium_url, options=options)
            logger.info(f"Conectado a Selenium Remoto en {selenium_url}")
        else:
            self.bot = webdriver.Firefox()
            
        self.wait = WebDriverWait(self.bot, 20)  # Espera explícita de hasta 20 segundos

    def save_error_screenshot(self, name: str = 'error_marangatu.png'):
        try:
            self.bot.save_screenshot(name)
            logger.info(f"Captura de pantalla de error guardada como {name}")
        except Exception as e:
            logger.error(f"No se pudo tomar la captura de pantalla: {e}")

    def login(self) -> None:
        bot = self.bot
        bot.get('https://marangatu.set.gov.py/eset/login')

        try:
            user = self.wait.until(EC.presence_of_element_located((By.ID, 'usuario')))
            user.clear()
            user.send_keys(self.username)

            password = self.wait.until(EC.presence_of_element_located((By.ID, 'clave')))
            password.clear()
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
        except Exception as e:
            logger.error(f'Error en login de MarangatuBot: {e}')
            self.save_error_screenshot('error_login.png')
            bot.close()

    def click_presentation(self) -> None:
        bot = self.bot
        try:
            # Selector relativo buscando el botón/enlace de presentación
            btn_presentation = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(translate(text(), 'PRESENTACIÓN', 'presentación'), 'presentación') or contains(@class, 'presentation')] | /html/body/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/section[1]/div/div[1]/a[1]")))
            btn_presentation.click()
        except Exception as e:
            logger.error(f'Error en click_presentation: {e}')
            self.save_error_screenshot('error_presentation.png')

    def add_fields_to_declatate(self, form_num: str, year: str, month: str) -> None:
        bot = self.bot
        
        # Esperar a que la nueva pestaña exista si es necesario
        if len(bot.window_handles) > 1:
            bot.switch_to.window(bot.window_handles[1])

        try:
            obligation_place = self.wait.until(EC.presence_of_element_located((By.NAME, 'obligacion')))
            obligation_select = Select(obligation_place)
            obligation_select.select_by_value(form_num)

            year_place = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="periodo"]//select[1]')))
            month_place = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="periodo"]//select[2]')))

            year_select = Select(year_place)
            year_select.select_by_value(year)

            month_select = Select(month_place)
            month_select.select_by_value(month)

            form_data = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form//input[contains(@class, "form-control") or @type="text"] | /html/body/div/div/div[2]/div/div/div[2]/div/div/div/div/div/form/section[2]/div/div/div/div/input')))
            if form_data:
                open_declaration_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//form//button[contains(text(), "Abrir") or contains(text(), "Declarar")] | /html/body/div/div/div[2]/div/div/div[2]/div/div/div/div/div/form/div[4]/div/button')))
                open_declaration_btn.click()
                
        except Exception as e:
            logger.error(f'Error en add_fields_to_declatate: {e}')
            self.save_error_screenshot('error_fields.png')
            self.logout()

    def complete_form(self, sin_movimiento: bool = False) -> None:
        bot = self.bot
        try:
            if sin_movimiento:
                field_data = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="C10"]')))
                field_data.send_keys('0')
                field_data.send_keys(Keys.TAB)

                verify_enter_data = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="C150"]')))
                
                # Esperar a que el valor se actualice a '0'
                self.wait.until(lambda d: verify_enter_data.get_attribute('value') == '0')
                data = verify_enter_data.get_attribute('value')

                if data == '0':
                    present_declaration_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Formu"]//button[contains(text(), "Presentar") or contains(@class, "btn-primary")] | //*[@id="Formu"]/section/div/div/div[2]/button')))
                    present_declaration_btn.click()

                    # Click to cancel
                    cancel_presentation_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "modal")]//button[contains(text(), "Cancelar")] | /html/body/div[2]/div/div/div/div[3]/button[1]')))
                    cancel_presentation_btn.click()
            bot.close()
        except Exception as e:
            logger.error(f'Error en complete_form: {e}')
            self.save_error_screenshot('error_complete_form.png')
            bot.close()

    def first_windows(self) -> None:
        try:
            self.bot.switch_to.window(self.bot.window_handles[0])
            self.bot.refresh()
        except WebDriverException as e:
            logger.error(f"Error al cambiar de ventana: {e}")

    def logout(self) -> None:
        try:
            self.bot.switch_to.window(self.bot.window_handles[0])
            self.bot.get('https://marangatu.set.gov.py/eset/logout')
            self.bot.quit()
        except WebDriverException:
            self.bot.quit()


class SendAnulados(MarangatuBot):

    def open_page_anulados(self) -> None:
        bot = self.bot
        try:
            # Reemplazo de XPath absolutos por selectores más relativos o combinados
            btn_facturacion = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Facturación')] | /html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[15]/div"))
            )
            btn_facturacion.click()

            solicitudes_xpath = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Solicitudes')] | /html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[1]")))
            solicitudes_xpath.click()

            preimpresos = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Preimpresos')] | /html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[3]/div")))
            preimpresos.click()

            baja_pre = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Baja de')] | /html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[4]/div/div")))
            baja_pre.click()
            
            if len(bot.window_handles) > 1:
                bot.switch_to.window(bot.window_handles[1])

        except Exception as e:
            logger.error(f'Error en open_page_anulados: {e}')
            self.save_error_screenshot('error_open_anulados.png')
            self.logout()

    def timbrado_input(self, numero_timbrado: str) -> None:
        bot = self.bot
        try:
            timbrado_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'form-control')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/section[1]/div[2]/div[1]/input")))
            timbrado_input.clear()
            timbrado_input.send_keys(numero_timbrado)
            timbrado_input.send_keys(Keys.TAB)

            nex_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Siguiente')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/section[2]/div/div[2]/button")))
            nex_button.click()
        except Exception as e:
            logger.error(f'Error en timbrado_input: {e}')
            self.save_error_screenshot('error_timbrado.png')
            self.logout()

    def input_reason_and_date(self, date: str) -> None:
        bot = self.bot
        try:
            reason_select_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'form-control')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div[2]/div[1]/select")))
            reason_select = Select(reason_select_element)
            reason_select.select_by_value(MOTIVO)

            date_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'date')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div[2]/div[2]/div/input")))
            date_element.clear()
            date_element.send_keys(date)
            date_element.send_keys(Keys.TAB)

            nex_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Siguiente')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/section/div/div[2]/button")))
            nex_button.click()

        except Exception as e:
            logger.error(f'Error en input_reason_and_date: {e}')
            self.save_error_screenshot('error_reason.png')
            self.logout()

    def document_data_input(self, document_number_range: str) -> None:
        bot = self.bot
        try:
            range_number_element_one = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr/td[3]/div/div[1]/input | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div/div[1]/input")))
            range_number_element_one.clear()
            range_number_element_one.send_keys(document_number_range)

            range_number_element_two = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr/td[3]/div/div[2]/input | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div/div[2]/input")))
            range_number_element_two.clear()
            range_number_element_two.send_keys(document_number_range)
            range_number_element_two.send_keys(Keys.TAB)

            try:
                second_input = WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr/td[3]/div[2] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div[2]")))
                nex_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Siguiente')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/section/div/div[2]/button")))
                nex_button.click()
            except TimeoutException:
                logger.warning('No se encontró el elemento second_input, continuando flujo...')

        except Exception as e:
            logger.error(f'Error en document_data_input: {e}')
            self.save_error_screenshot('error_document_data.png')
            self.logout()

    def send_request(self):
        bot = self.bot
        try:
            # Verify document_anulado
            setlogo_img_reference = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'logo')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/div/div/div/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/p[1]/font/img")))

            # Click the finalizar button
            finally_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Finalizar')] | /html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/section/div/div[2]/button")))
            finally_button.click()

            alert_modal = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal')] | /html/body/div[2]/div/div/div/div[1]")))
            
            send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'modal')]//button[contains(text(), 'Aceptar') or contains(text(), 'Enviar')] | /html/body/div[2]/div/div/div/div[3]/button[2]")))
            send_button.click()

            try:
                setlogo_img_finally_reference = WebDriverWait(bot, 20).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'logo')] | /html/body/div/div/div/div[2]/div/div/div/div[2]/div/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/p[1]/font/img")))
            except TimeoutException:
                logger.warning('No se pudo validar el logo final')
                
        except Exception as e:
            logger.error(f'Error en send_request: {e}')
            self.save_error_screenshot('error_send_request.png')
            self.logout()

    def screen_anulado(self, ruc: str, document_number: str) -> None:
        bot = self.bot
        try:
            # Localizar el elemento que quieres capturar
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'container')] | /html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div/div")))
            
            os.makedirs('archives/anulados', exist_ok=True)
            elemento.screenshot(f'archives/anulados/baja_{ruc}_{document_number}.png')
        except Exception as e:
            logger.error(f'Error al capturar pantalla de anulado: {e}')
