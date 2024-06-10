import investpy as inv


class EconomicCalendar:
    # Fixed class attributes for countries and event list
    COUNTRIES = ['united states']
    EVENTS = [
        'Crude Oil Inventories',
        'EIA Refinery Crude Runs (WoW)',
        'Crude Oil Imports',
        'Cushing Crude Oil Inventories',
        'Distillate Fuel Production',
        'EIA Weekly Distillates Stocks',
        'Gasoline production',
        'Heating Oil Stockpiles',
        'EIA Weekly Refinery Utilization Rates (WoW)',
        'Gasoline Inventories',
    ]

    @staticmethod
    def get_data(from_date=None, to_date=None):
        """
        Retrieves economic calendar data for specified date range and filter by predefined events.

        :param from_date: The start date for the data retrieval.
        :param to_date: The end date for the data retrieval.
        :return: Filtered DataFrame containing relevant economic events.
        """
        # Retrieve economic calendar data
        dt = inv.economic_calendar(countries=EconomicCalendar.COUNTRIES, from_date=from_date, to_date=to_date)
        # Filter the data (doesnt work in Api once)
        filtered_data = dt.loc[dt['event'].isin(EconomicCalendar.EVENTS), ['event', 'actual', 'forecast', 'previous']]
        return filtered_data
