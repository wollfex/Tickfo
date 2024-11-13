import tkinter as tk
from tkinter import messagebox
import yfinance as yf
from datetime import datetime, timedelta


# Stock data retrieval function
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    try:
        # Basic stock info
        market_cap = info.get("marketCap")
        dividend_yield = info.get("dividendYield")
        dividend_yield = f"{dividend_yield * 100:.2f}%" if dividend_yield else "N/A"
        volume = info.get("volume")
        current_price = info.get("currentPrice")
        beta = info.get("beta")
        eps = info.get("trailingEps")
        pe_ratio = info.get("trailingPE")

        # Date calculations for historical prices
        today = datetime.now().date()
        dates = {
            "1_month": today - timedelta(days=30),
            "6_months": today - timedelta(days=182),
            "1_year": today - timedelta(days=365),
            "year_to_date": datetime(today.year, 1, 1).date()
        }

        # Historical prices
        historical_data = stock.history(period="1y")

        # Helper function to get price on the closest available date
        def get_price_on_date(target_date):
            # Convert target_date to naive datetime for comparison
            target_date = datetime.strptime(target_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

            # Find the closest date in historical_data.index by converting index to naive
            closest_date = min(historical_data.index,
                               key=lambda x: abs(x.to_pydatetime().replace(tzinfo=None) - target_date))
            price = historical_data.loc[closest_date, "Close"]
            return price

        # Retrieve historical prices
        price_1_month = get_price_on_date(dates["1_month"])
        price_6_months = get_price_on_date(dates["6_months"])
        price_ytd = get_price_on_date(dates["year_to_date"])
        price_1_year = get_price_on_date(dates["1_year"])

        # Format the result for display
        result = (
            f"Stock Data for {ticker.upper()}:\n"
            f"Market Cap: ${market_cap:,.2f}\n"
            f"Dividend Yield: {dividend_yield}\n"
            f"Volume: {volume}\n"
            f"Current Price: ${current_price}\n"
            f"Price 1 Month Ago: ${price_1_month:.2f}\n"
            f"Price 6 Months Ago: ${price_6_months:.2f}\n"
            f"Price YTD: ${price_ytd:.2f}\n"
            f"Price 1 Year Ago: ${price_1_year:.2f}\n"
            f"Beta: {beta}\n"
            f"Earnings Per Share (EPS): ${eps}\n"
            f"Price-to-Earnings Ratio (PE): {pe_ratio}"
        )
        return result

    except Exception as e:
        return f"Error retrieving data for {ticker}: {str(e)}"

# GUI
def analyze_stock():
    ticker = entry.get()
    if ticker:
        result = get_stock_data(ticker)
        messagebox.showinfo("Stock Analysis", result)
    else:
        messagebox.showwarning("Input Error", "Please enter a stock ticker.")


# Initialize GUI
window = tk.Tk()
window.title("Stock Market Analyzer")

# GUI elements
label = tk.Label(window, text="Enter Stock Ticker:")
label.pack(pady=5)

entry = tk.Entry(window)
entry.pack(pady=5)

button = tk.Button(window, text="Analyze", command=analyze_stock)
button.pack(pady=10)

window.mainloop()