import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
    return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Locator for the Test Select Comfort
    call_a_taxi_button = (By.XPATH, "//div[@class='results-text']//button[@type='button']")
    type_picker = (By.CLASS_NAME, 'type-picker')
    tariff_picker = (By.CLASS_NAME, 'tariff-picker')
    comfort_card = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")

    # Locators for phone test
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_number_input = (By.ID, 'phone')
    # phone_number_next_button = (By.XPATH, "//button[@class = 'button full' and text()='Siguiente']")
    phone_number_next_button = (By.CSS_SELECTOR, ".button.full")
    phone_number_code = (By.ID, 'code')
    phone_number_code_confirm_button = (By.XPATH, "//button[@class = 'button full' and text()='Confirmar']")

    # Locators for credit card test
    # credit_card_button = (By.XPATH, "//div[@class='pp-button filled']")
    credit_card_button = (By.CSS_SELECTOR, ".pp-button")
    credit_card_add_selector = (By.XPATH, "//div[@class ='pp-row disabled']")
    credit_card_number = (By.ID, 'number')
    credit_card_code = (By.XPATH, "//div[@class='card-code-input']/input")
    credit_card_add_button = (By.XPATH, "//button[@class='button full' and text()='Agregar']")
    credit_card_form_close_button = (By.XPATH, "//div[@class = 'head' and text()='Método de pago']/parent::div//button")
    credit_card_label_payment_method = (By.CLASS_NAME, 'pp-value-text')

    #Locators for comment to driver test
    comment_to_driver_input = (By.ID, 'comment')

    #Locators for select blanked and napkin test
    select_blanked_and_napkin_toogle = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']")

    select_blanked_and_napkin_toggle_for_info = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']//input")

    # Locators for setting two ice_cream test
    two_ice_cream_couter_plus_button = (By.XPATH, "//div[text()='Helado']//following-sibling::div//div[@class='counter-plus']")

    ice_cream_counter = (By.XPATH, "//div[text()='Helado']//following-sibling::div//div[@class='counter-value']")

    #Locators for taxi modal test
    button_request_taxi = (By.CLASS_NAME, 'smart-button')

    modal = (By.XPATH, "//div[@class='order shown']")
    modal_title = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, adress_to):
        self.set_from(address_from)
        self.set_to(adress_to)

    #Functions related to the Test Select Comfort
    def click_call_a_taxi_button(self):
        self.driver.find_element(*self.call_a_taxi_button).click()

    def click_comfort_tarif_card(self):
        self.driver.find_element(*self.comfort_card).click()

    def get_selected_tarif_card(self):
        return self.driver.find_element(*self.comfort_card).text

    #Function related to the phone test
    def click_phone_number(self):#
        self.driver.find_element(*self.phone_number_button).click()

    def set_phone_number(self):
        self.driver.find_element(*self.phone_number_input).send_keys(data.phone_number)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_button).text

    def click_phone_next_button(self):
        self.driver.find_element(*self.phone_number_next_button).click()

    def set_phone_number_code(self, new_code):
        self.driver.find_element(*self.phone_number_code).send_keys(new_code)

    def click_phone_confirm_button(self):
        self.driver.find_element(*self.phone_number_code_confirm_button).click()

    # Functions for the credit card test
    def click_credit_card_button(self):
        self.driver.find_element(*self.credit_card_button).click()

    def click_credit_card_add_selector(self):
        self.driver.find_element(*self.credit_card_add_selector).click()

    def set_credit_card_number(self):
        self.driver.find_element(*self.credit_card_number).send_keys(data.card_number)

    def set_credit_card_code(self):
        self.driver.find_element(*self.credit_card_code).send_keys(data.card_code)
        self.driver.find_element(*self.credit_card_code).send_keys(Keys.TAB)

    def click_credit_card_add_button(self):
        self.driver.find_element(*self.credit_card_add_button).click()

    def click_credit_card_form_close_button(self):
        self.driver.find_element(*self.credit_card_form_close_button).click()

    def get_credit_card_label_payment_method(self):
        return self.driver.find_element(*self.credit_card_label_payment_method).text

    #Functions related to the test for comment to driver
    def set_comment_to_driver(self):
        self.driver.find_element(*self.comment_to_driver_input).send_keys(data.message_for_driver)

    def get_comment_to_driver(self):
        return self.driver.find_element(*self.comment_to_driver_input).get_property('value')

    #Functions related to the test for selecting blanket and napkin
    def click_blanked_and_napkin_option(self):
        self.driver.find_element(*self.select_blanked_and_napkin_toogle).click()

    def get_is_blanked_and_napkin_active(self):
        return self.driver.find_element(*self.select_blanked_and_napkin_toggle_for_info).is_selected()

    #Functions related to the two ice cream test
    def rolldown(self, down_clicks):
        for i in range(down_clicks):
            self.driver.find_element(*self.tariff_picker).send_keys(Keys.ARROW_DOWN)

    def click_ice_cream_counter_plus(self):
        self.driver.find_element(*self.two_ice_cream_couter_plus_button).click()
        self.driver.find_element(*self.two_ice_cream_couter_plus_button).click()

    def get_ice_cream_counter(self):
        return self.driver.find_element(*self.ice_cream_counter).text

    # Functions related to the modal taxi test
    def click_request_taxi_button(self):
        self.driver.find_element(*self.button_request_taxi).click()

    def get_modal_text(self):
        return self.driver.find_element(*self.modal_title).text

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        # from selenium.webdriver import DesiredCapabilities
        # capabilities = DesiredCapabilities.CHROME
        # capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        # cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.ID, "from"))
        )
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.ID, "to"))
        )
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        # routes_page.wait_element_to_be_clickable(routes_page.tariff_picker)
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(routes_page.type_picker))
        routes_page.click_call_a_taxi_button()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(routes_page.tariff_picker))
        routes_page.click_comfort_tarif_card()
        selected_tarif = routes_page.get_selected_tarif_card()
        assert "Comfort" == selected_tarif, "The tarif selected is not comfort"

    def test_set_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)

        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(routes_page.phone_number_button))
        routes_page.click_phone_number()

        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(routes_page.phone_number_input))
        routes_page.set_phone_number()
        routes_page.click_phone_next_button()

        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(routes_page.phone_number_code))
        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_number_code(code)

        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(routes_page.phone_number_code_confirm_button))
        routes_page.click_phone_confirm_button()

        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(routes_page.phone_number_button))
        assert data.phone_number == routes_page.get_phone_number(), "Phone number does not match"

    def test_set_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)

        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(routes_page.credit_card_button))
        routes_page.click_credit_card_button()

        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(routes_page.credit_card_add_selector))
        routes_page.click_credit_card_add_selector()

        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(routes_page.credit_card_number))
        routes_page.set_credit_card_number()
        routes_page.set_credit_card_code()

        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(routes_page.credit_card_add_button))
        routes_page.click_credit_card_add_button()

        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(routes_page.credit_card_form_close_button))

        routes_page.click_credit_card_form_close_button()

        assert "Tarjeta" == routes_page.get_credit_card_label_payment_method(), "Tarjeta has not been selected"

    def test_comment_to_driver(self):
        routes_page = UrbanRoutesPage(self.driver)

        WebDriverWait(self.driver,3).until(expected_conditions.element_to_be_clickable(routes_page.comment_to_driver_input))
        routes_page.set_comment_to_driver()
        time.sleep(1)
        assert data.message_for_driver == routes_page.get_comment_to_driver()

    def test_select_blanket_and_napkin(self):
        routes_page = UrbanRoutesPage(self.driver)

        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(routes_page.select_blanked_and_napkin_toogle))
        routes_page.click_blanked_and_napkin_option()

        assert True == routes_page.get_is_blanked_and_napkin_active()

    def test_set_two_icecream(self):
        routes_page = UrbanRoutesPage(self.driver)

        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(routes_page.two_ice_cream_couter_plus_button))

        routes_page.rolldown(6)

        routes_page.click_ice_cream_counter_plus()

        assert routes_page.get_ice_cream_counter() == '2'

    def test_modal_taxi_appears(self):
        routes_page = UrbanRoutesPage(self.driver)

        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(routes_page.button_request_taxi))
        routes_page.click_request_taxi_button()

        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(routes_page.modal))

        assert ("Buscar automóvil") == routes_page.get_modal_text(), "modal did not open"
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
