# Forex-Converter

## Table of Contents

* [Overview](#overview)
* [Running Application](#running-application)
* [Flow](#flow)
* [Routes](#routes)
* [Technologies](#technology-stack)
* [Tests](#tests)
* [Misc](#misc)

---

## Overview:

This project was part of a series of assignments for Springboard's Software Engineering course which checked how our skills were developing with the technologies were being taught which at this time was `Python`, and `Flask`.

Along with these technologies, were also introduced to making external `API` servers to display data received on a few static frontend pages. One of these pages will be the main landing zone where users can enter an `integer` (number) along with two `currency codes` to calculate (the currency to convert from and the currency to convert to).

The main logic of the application is done on the server side by taking the data submitted from the form and making the conversion by using the `forex-python` module.

- __NOTE:__ The docs for the library used can be found [here](https://forex-python.readthedocs.io/en/latest/usage.html).

![Main View](/imgs/main_view.png)

* [Back to Top](#table-of-contents)

---

## Running Application:

Considering that this application is a flask application and the templates were all setup using `Jinja2`, this application is not available for viewing through GitHub's site hosting.

- Yes, I am aware that I can use Heroku or other site hosting platforms but considering this is a light static frontend, I have left instructions to run this application on your local machine.

- If you have ideas for how I can run the application through GH please feel free to give me a ping!

- For those that are more tech savy, you can run the application by following these easy steps:

    1. Clone this repo (the green button at the top right).
    
    1. Once cloned, you will need to create a `venv` folder which can be done by using command: `python3 -m venv venv`.
    
    1. You can start the `venv` folder created by using command: `source venv/bin/activate`.

    1. Final setup step is to install the dependencies under the `requirements.txt` file which can be done by running command: `pip install -r requirements.txt`

    1. Once all the dependencies are installed, you can run the application using the `flask run` command and this should work just fine since the main application file is called `app.py` which is what `Flask` is looking for.

    1. The application will be under `localhost:5000`

* [Back to Top](#table-of-contents)

---

## Flow:

- Once you've arrived on the main page, you will see three input fields:

    - `Converting From`
    - `Converting To`
    - `Amount`

- `Converting From` input is the currency code that you want to convert from.

- `Converting To` input is the currency that you are changing to.

__NOTE:__ The application uses currency codes which really aren't common knowledge but have no fear! I have provided a list of currency codes [here](https://www.iban.com/currency-codes)!

- If you're using the link above, the code the appliation is expecting is the three letter `Code` column for each country listed.

- `Amount` is the number amount that you want convert. 

    - __NOTE:__ This field MUST be a number otherwise you're going to see a lovely little error at the top of the screen.
![Number Error](/imgs/converter-error-1.png)

- As you can see from the image above, the alerts are dismissable! massive shoutout to [Bootstrap 5](https://getbootstrap.com/docs/5.1/getting-started/introduction/)!

- If the conversion is successful, the users will be routed to the `/conversion` route and the user will see the view below.
    ![Conversion View](/imgs/converter-success.png)

- If the user clicks on the `Home` button, they will be returned to the home view to convert another amount or currency code.

* [Back to Top](#table-of-contents)

---

## Routes:

- The project currently has three routes with one of the routes being a `POST` method that is activated through the form that is submitted.

    - `/` (home)
    - `/conversion`
    - `/calculate`

- `/` (home) route is the main view that contains the main input form that users will be entering the data under.

- `/conversion` route will display the results from the currency conversion after the calculations have been completed.

- `/calcualte` route is NOT a route for the application that contains any view however, this is the route that sends the form data to the backend via `POST` method. Route is responsible for processing the currency calculations and returning the results or reflecting an error if any invalid data passed in or the currency codes are unavailable for conversion.

* [Back to Top](#table-of-contents)

---

## Technology Stack:

- Frontend

    - `HTML` / `Jinja2`
    - `Bootstrap 5`

- Backend

    - `Python` / `Flask`
    - `forex-python`

* [Back to Top](#table-of-contents)

---

## Tests:

- The main tests that we were required to write for the application are listed under the `test.py` file.

    - __NOTE!__ The tests written all have the CURRENT results for currency conversions so if you run this file there is a high likelyhood that some tests will fail __THIS IS EXPECTED__ because the `forex-python` module is using a live external API that is getting updated frequently as the exchange rates change. If this is the case for you, you can update the new updated values in the failed tests or comment those tests out.

- To run the tests, you can use command `python3 -m unittest test.py`.

    - __WARNING!__ These tests can take time to run so don't freak out mmkay? I've been told that running integration/ unit tests with Python's unittest module tends to take time the more tests are included in the file. Feel free to split up your versions as you see fit but please reference the file structure in the docs for new test files that you may create.

* [Back to Top](#table-of-contents)

---

## Misc

- Have fun using this app! If you want to reach out via LinkedIn or see what I am up to away from the desk, you can view the social links below.

    - [LinkedIn](https://www.linkedin.com/in/diegoquintanilla/)
    - [Instagram](https://www.instagram.com/mrquintanillaforreal/)

* [Back to Top](#table-of-contents)