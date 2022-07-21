from forex_python.converter import CurrencyRates, CurrencyCodes
from unittest import TestCase
from app import app
from flask import session

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

currency = CurrencyRates()
code = CurrencyCodes()

class ViewTesting(TestCase):
    
    def test_home_view(self):
        """basic test logic for main home view."""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary">Convert</button>', html)

    def test_conversion_view(self):
        """basic test for conversion route (route that will be rendered once the form is submitted)."""
        with app.test_client() as client:
            res = client.get('/conversion')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary">Home</button>', html)

    def test_calculate_form(self):
        """basic test for calculate route once form is submitted. 
            NOTE: The forex API for Python uses live information based on CURRENT currency exchance rates, your result amount will need to be updated based on the calculation that is received whenever you ping the API in your terminal/app.
        """
        with app.test_client() as client:
            form_data = {'current-currency':'usd', 'new-currency':'jpy', 'amount':100}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>The result is: ¥ 13817.04</h1>", html)
    
    def test_calculate_form_usd_to_eur(self):
        """second basic form data test (from usd to eur)
            NOTE: The forex API for Python uses live information based on CURRENT currency exchance rates, your result amount will need to be updated based on the calculation that is received whenever you ping the API in your terminal/app.
        """
        with app.test_client() as client:
            form_data = {'current-currency':'usd', 'new-currency':'eur', 'amount':100}
            res = client.post('/calculate', data= form_data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>The result is: € 98.05</h1>", html)
            
    def test_blank_form_redirect_response(self):
        """function is testing for redirect status code and location."""
        with app.test_client() as client:
            form_data = {'current-currency':'', 'new-currency':'', 'amount': ''}
            res = client.post('/calculate', data=form_data)
            html = res.get_data(as_text=True)
            # NOTE: code below is testing to see if the blank form gets the redirect code and if the location is the same as the main route per the logic in app.py file.
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')

    def test_blank_form_redirect_view(self):
        """function is testing redirect view whenever a blank form is submitted."""

        # NOTE: Code below is testing to see if the actual view of the redirect (html code) is being seen and if the correct message is being displayed on the alert at the top of the page after a user is redirected.
        with app.test_client() as client:
            form_data = {'current-currency':'', 'new-currency':'', 'amount': ''}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)
            
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    ALL FIELDS MUST BE FILLED IN BEFORE SUBMITTING!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)
    
    def test_blank_from_curr_input(self):
        """function is testing the first input of the form in the main view route and verifying that the correct message is being seen if nothing is entered in but the rest of the fields are."""

        with app.test_client() as client:
            form_data = {'current-currency':'', 'new-currency':'jpy', 'amount': 1000}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    FIRST FIELD CANNOT BE BLANK!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)
    
    def test_blank_to_curr_input(self):
        """function is testing the second input of the form in the main view route and verifying that the correct message is being seen if nothing is entered under the second input area."""

        with app.test_client() as client:
            form_data = {'current-currency':'eur', 'new-currency':'', 'amount': 1000}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    SECOND FIELD CANNOT BE BLANK!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)

    def test_blank_amount_input(self):
        """function is testing the third input of the form in the main view route and verifying that the correct message is being seen if nothing is entered under the third input area."""

        with app.test_client() as client:
            form_data = {'current-currency':'eur', 'new-currency':'usd', 'amount':''}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    AMOUNT CANNOT BE BLANK!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)

    def test_invalid_amount(self):
        """function is testing value amount to verify that if a user enters a string instead of a number, they will be routed to the main page again and the main page will show the correct error message"""

        with app.test_client() as client:
            form_data = {'current-currency':'eur', 'new-currency':'usd', 'amount':'asdfasdf'}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    AMOUNT MUST BE A NUMBER!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)

    def test_invalid_from_curr(self):
        """function is testing invalid first currecy code input and making sure that the correct message is being seen after the user is routed back to the main page."""

        with app.test_client() as client:
            form_data = {'current-currency':'aaa', 'new-currency':'usd', 'amount': 100}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    INVALID CURRENCY CODE: AAA
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)

    def test_invalid_to_curr(self):
        """function is testing invalid second currecy code input and making sure that the correct message is being seen after the user is routed back to the main page."""

        with app.test_client() as client:
            form_data = {'current-currency':'usd', 'new-currency':'zzz', 'amount': 100}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    INVALID CURRENCY CODE: ZZZ
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)

    def test_invalid_currencies(self):
        """function is testing if both currecy code inputs are invalid and making sure that the correct message is being seen after the user is routed back to the main page."""

        with app.test_client() as client:
            form_data = {'current-currency':'aaa', 'new-currency':'zzz', 'amount': 100}
            res = client.post('/calculate', data=form_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    BOTH CURRENCY CODES INVALID: AAA, ZZZ
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""", html)

    def test_session_info(self):
        """function is testing to verify that all requried information is stored in the session object based on the form data that is passed through."""

        with app.test_client() as client:
            form_data = {'current-currency':'usd', 'new-currency':'jpy', 'amount':100}
            res = client.post('/calculate', data= form_data, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['result'], 13817.04)
            self.assertEqual(session['currency_sign'], '¥')