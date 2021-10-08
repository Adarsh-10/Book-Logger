# import the Flask class from the flask module
from flask import Flask, render_template
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pytz

from helpers import apology, login_required

# create the application object
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    """show all the book reviews the user has created"""
    userInfo = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])

    buy2_table_info = db.execute("SELECT * FROM buy2 WHERE username=?", userInfo[0]["username"])

    book_titles = [] # string values
    book_authors = [] # string values
    book_ratings = [] # integer values
    book_summaries = [] # string values
    book_takeaways = [] # string values


    for i in range(0, len(buy2_table_info)):
        stock_info = lookup(buy2_table_info[i]["symbol"])

        companies.append(stock_info["name"])
        total_price = stock_info["price"]
        total_current_stock_value += total_price*buy2_table_info[i]["shares"]
        total_prices.append(usd(total_price*buy2_table_info[i]["shares"]))
        individual_prices.append(usd(stock_info["price"]))

    portfolio_value = float(userInfo[0]["cash"]) + total_current_stock_value

    return render_template("index.html", cash=usd(userInfo[0]["cash"]), info=buy2_table_info, companies=companies,
                           length=len(buy2_table_info), total_current_price=total_prices, individual_current_price=individual_prices, portfolio=usd(portfolio_value))

@app.route('/login')
def welcome():
    return render_template('login.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)