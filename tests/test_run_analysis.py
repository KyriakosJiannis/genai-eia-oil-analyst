import pytest
import warnings
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.run_analysis import main, perform_analysis

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="investpy")


@pytest.fixture
def mock_config():
    return {
        'openai': {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 150,
            'temperature': 0.7,
            'top_p': 1.0,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        },
        'paths': {
            'raw_data': 'data/raw/',
            'processed_data': 'data/processed/',
            'html_files': 'html/'
        },
        'features': {
            'enable_data_analysis': True,
            'enable_logging': False
        },
        'investing_data': {
            'use_fake': False
        },
        'openai_data': {
            'use_fake': False
        },
        'api': {
            'openai_key': 'fake_api_key'
        }
    }


@patch('src.run_analysis.load_config')
@patch('src.run_analysis.fetch_eia_report')
@patch('src.run_analysis.fetch_ai_analysis')
@patch('src.run_analysis.bar_chart')
@patch('src.run_analysis.initialize_environment')
def test_main(mock_initialize_environment, mock_bar_chart, mock_fetch_ai_analysis, mock_fetch_eia_report,
              mock_load_config, mock_config):
    # Mock the configuration and other dependencies
    mock_load_config.return_value = mock_config
    mock_fetch_eia_report.return_value = MagicMock()
    mock_fetch_ai_analysis.return_value = {'rating': 6, 'analysis': 'Test analysis'}
    mock_bar_chart.return_value = '<div>Bar Chart</div>'

    # Define the report date
    report_date_str = "05-06-2024"
    report_date = datetime.strptime(report_date_str, "%d-%m-%Y")

    # Call the main function
    main()

    # Check that the functions were called
    mock_initialize_environment.assert_called_once()
    mock_load_config.assert_called_once()
    mock_fetch_eia_report.assert_called_once_with(report_date)
    mock_fetch_ai_analysis.assert_called_once()
    mock_bar_chart.assert_called_once_with(6)


def test_perform_analysis(mock_config):
    result = perform_analysis(mock_config)
    assert result == True


if __name__ == '__main__':
    pytest.main()
