import os
import pandas as pd
from datetime import datetime, timedelta
from src.config_loader import load_config
from src.openai_analysis import OpenaiAnalysis
from src.economic_calendar import EconomicCalendar

# Define the base path for your project
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

config = load_config()
HTML_PATH = os.path.join(BASE_PATH, config['paths']['html_files'])
USE_FAKE_DATA = config['investing_data']['use_fake']
USE_FAKE_AI_API = config['openai_data']['use_fake']


def read_html_file(filename):
    """
    Reads the content of an HTML file.

    :param filename: The name of the HTML file.
    :type filename: str
    :return: The content of the HTML file.
    :rtype: str
    :raises RuntimeError: If there is an error reading the file.
    """
    try:
        full_path = os.path.join(HTML_PATH, filename)
        with open(full_path, 'r') as f:
            return f.read()
    except Exception as error:
        raise RuntimeError(f"Error reading HTML file {filename}: {error}")


def is_today(date):
    """Check if the given date is today"""
    return date.date() == datetime.today().date()


def generate_fake_eia_report():
    """Generates a fake EIA report DataFrame for development purposes."""

    data = {
        'event': [
            'Crude Oil Inventories',
            'EIA Refinery Crude Runs (WoW)',
            'Crude Oil Imports',
            'Cushing Crude Oil Inventories',
            'Distillate Fuel Production',
            'EIA Weekly Distillates Stocks',
            'Gasoline production',
            'Heating Oil Stockpiles',
            'EIA Weekly Refinery Utilization Rates (WoW)',
            'Gasoline Inventories'
        ],
        'actual': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'forecast': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'previous': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    return pd.DataFrame(data)


def fetch_eia_report(report_date):
    """
    Fetches the EIA report data for the given report date.
    :param report_date: The date for which the EIA report is to be fetched.
    :return: DataFrame containing the EIA report data or None if no data is available.
    """
    date_to_check = datetime.combine(report_date, datetime.min.time())

    if is_today(date_to_check):
        from_date_str = None
        to_date_str = None
    else:
        from_date_str = report_date.strftime("%d/%m/%Y")
        to_date_str = (report_date + timedelta(days=1)).strftime("%d/%m/%Y")  # set up +1 day

    try:
        if USE_FAKE_DATA:
            eia_report = generate_fake_eia_report()  # For development purposes
        else:
            eia_report = EconomicCalendar.get_data(from_date_str, to_date_str)

        if eia_report.empty:
            raise ValueError("No data available for the selected date.")
    except Exception as error:
        raise RuntimeError(f"Error fetching EIA report data: {error}")
    return eia_report


def fetch_ai_analysis(eia_report):
    """
    Fetches AI analysis for the EIA report.

    :param eia_report: The EIA report DataFrame.
    :type eia_report: pd.DataFrame
    :return: Dictionary containing the rating and analysis.
    :rtype: dict
    """
    try:
        eia_string = eia_report.to_string(index=False, header=True)

        if USE_FAKE_AI_API:
            result = {
                'rating': 6,
                'analysis': ('The EIA weekly report shows a mixed picture for the oil market. '
                             'While there was a build in Crude Oil Inventories, the increase was less than expected, '
                             'which could be seen as mildly bullish. Crude Oil Imports also increased slightly, which '
                             'could indicate potential demand. Cushing Crude Oil Inventories showed a build, which may '
                             'have a bearish impact. Distillate Fuel Production increased slightly, but EIA Weekly '
                             'Distillates Stocks saw a larger build, potentially bearish. Heating Oil Stockpiles '
                             'increased, which could be bearish. On a positive note, EIA Weekly Refinery Utilization '
                             'Rates decreased, potentially indicating increased demand. Gasoline Inventories saw a '
                             'build, but again, less than expected, which could be seen as mildly bullish overall.')
            }
        else:
            analyzer = OpenaiAnalysis(eia_string)
            result = analyzer.analyze_report()

    except Exception as error:
        raise RuntimeError(f"Error fetching AI analysis: {error}")

    return result


def bar_chart(rating):
    """
    Creates a bar chart based on the rating.
    """
    try:
        rating_bar_html = read_html_file("rating_bar.html")
        rating_bar_html = rating_bar_html.replace("{rating}", str(rating))
        rating_position = rating * 10
        rating_bar_html = rating_bar_html.replace("{rating_position}", str(rating_position))
    except Exception as error:
        raise RuntimeError(f"Error creating bar chart: {error}")

    return rating_bar_html
