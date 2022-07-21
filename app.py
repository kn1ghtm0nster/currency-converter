from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

currency = CurrencyRates()
code = CurrencyCodes()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOTALLYSECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
# toolbar = DebugToolbarExtension(app)


currency_list = []

for item in code._currency_data:
    currency_list.append(item['cc'])

# NOTE: float testing function from SO Post -> https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int
def is_float(value):
  try:
    float(value)
    return True
  except:
    return False

@app.route('/')
def home_view():
    """displays the home page which contains form for users to fill out and submit"""
    return render_template('main.html')

@app.route('/conversion')
def conversion_view():
    """returns the finalized converted amount."""
    return render_template('conversion.html')

@app.route('/calculate', methods=['POST'])
def results_view():
    """displays the result from form entered on home page"""
        # NOTE: FORM DATA 
    from_curr = request.form['current-currency'].upper()
    to_curr = request.form['new-currency'].upper()
    amount = request.form['amount']
    
    try:
        # NOTE: currency symbol for requested converted currency.
        symbol = code.get_symbol(to_curr)

        # NOTE: storing session data to view in conversion route once form is submitted.
        session['currency_sign'] = symbol

        # NOTE: logic check to flash a message depending on which fields on the form are filled in or not.
        if not from_curr and not to_curr and not amount:
            flash('ALL FIELDS MUST BE FILLED IN BEFORE SUBMITTING!', 'danger')
            return redirect('/')
        elif not from_curr:
            flash('FIRST FIELD CANNOT BE BLANK!', 'danger')
            return redirect('/')
        elif not to_curr:
            flash('SECOND FIELD CANNOT BE BLANK!', 'danger')
            return redirect('/')
        elif not amount:
            flash('AMOUNT CANNOT BE BLANK!', 'danger')
            return redirect('/')
        

        # NOTE: flash user a message if the amount input section is NOT a number/float and then routing them back to the home page.
        if is_float(amount) == False:
            flash('AMOUNT MUST BE A NUMBER!', 'danger')
            return redirect('/')
        
        # NOTE: flash error message if either of the form currency values are not in the global currency list defined at top of file.
        if from_curr not in currency_list and to_curr not in currency_list:
            flash(f'BOTH CURRENCY CODES INVALID: {from_curr}, {to_curr}', 'danger')
            return redirect('/')
        elif from_curr not in currency_list:
            flash(f'INVALID CURRENCY CODE: {from_curr}', 'danger')
            return redirect('/')
        elif to_curr not in currency_list:
            flash(f'INVALID CURRENCY CODE: {to_curr}', 'danger')
            return redirect('/')
        else:
            result = round(currency.convert(from_curr, to_curr, float(amount)), 2)
            # NOTE: setting session to contain the result value so that it can be accessed on the frontend.
            session['result'] = result
            flash('CONVERSION SUCCESSFUL!', 'success')
            return redirect('/conversion')

    except RatesNotAvailableError:
        flash('First or Second currency codes are unavailable at this time.', 'danger')
        return redirect('/')