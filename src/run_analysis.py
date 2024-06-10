# src/run_analysis.py
from datetime import datetime
from src.config_loader import load_config
from src.setup import initialize_environment
from src.utils import fetch_eia_report, fetch_ai_analysis, bar_chart


def perform_analysis(config):
    # Access OpenAI settings
    openai_model = config['openai']['model']
    max_tokens = config['openai']['max_tokens']
    temperature = config['openai']['temperature']

    # Access paths
    raw_data_path = config['paths']['raw_data']
    processed_data_path = config['paths']['processed_data']
    html_files_path = config['paths']['html_files']

    # Access features
    enable_data_analysis = config['features']['enable_data_analysis']
    enable_logging = config['features']['enable_logging']

    # Access investing and OpenAI data settings
    use_fake_investing_data = config['investing_data']['use_fake']
    use_fake_openai_data = config['openai_data']['use_fake']

    # Access API key if available
    api_key = config.get('api', {}).get('openai_key')

    # Your analysis code here
    if enable_data_analysis:
        # Perform data analysis
        pass

    return True  # Indicate success for test purposes


def main():
    # Initialize the environment
    initialize_environment()

    config = load_config()
    perform_analysis(config)

    # Define the report date
    report_date_str = "05-06-2024"
    report_date = datetime.strptime(report_date_str, "%d-%m-%Y")

    # Fetch the EIA report
    eia_report = fetch_eia_report(report_date)
    print(eia_report)

    # Fetch the AI analysis
    analysis = fetch_ai_analysis(eia_report)
    print(analysis)

    # Create a bar chart based on the rating
    rating_html = bar_chart(analysis['rating'])
    print(rating_html)


if __name__ == "__main__":
    main()
