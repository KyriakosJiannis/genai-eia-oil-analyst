from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from src.config_loader import load_config


class OpenaiAnalysis:
    def __init__(self, eia_report: str):
        # Load configuration settings
        config = load_config()
        self.eia_report = eia_report
        self.response_schemas = [
            ResponseSchema(
                name="rating",
                type="integer",
                description="Provide a bullish/bearish index for oil prices on a scale of 0 to 10, with 10 being the most bullish and 0 being the most bearish."
            ),
            ResponseSchema(
                name="analysis",
                type="string",
                description="Create a detailed summary analysis of the EIA report, highlighting the key findings. Follow this with a more detailed explanation of the bullish/bearish ratings in the next paragraph."
            )
        ]
        self.parser = StructuredOutputParser(response_schemas=self.response_schemas)
        self.format_instructions = self.parser.get_format_instructions()

        # Initialize ChatOpenAI with configurations from config.yaml
        self.llm = ChatOpenAI(
            temperature=config['openai']['temperature'],
            model=config['openai']['model']
        )

    def generate_prompt(self) -> str:
        # Generate a structured prompt for the LLM
        return f"""
        As an oil analyst, I would like to share the EIA weekly report with you. 
        Please provide a structured response in the following format:
        {self.format_instructions}

        The report is provided below:
        text: ```{self.eia_report}```

        Keep in mind the following points for your analysis:
        - Crude Oil Inventories has the highest importance in the report and should be weighted as 4.
        - Each of the other indicators should be weighted as 1.
        - An increase in inventories generally indicates a bearish outlook (oversupply), while a decrease indicates a bullish outlook (undersupply).
        - Emphasize the differences between forecasted and actual values, especially when the forecast expected a decrease and the actual result was an increase, and vice versa.
        - Be careful with interpreting the '-' symbols in your calculations

        Your response should include:
        1. A bullish/bearish index for oil prices on a scale of 0 to 10, with 10 being the most bullish and 0 being the most bearish.
        2. A detailed summary analysis of the EIA report, highlighting the key findings.
        3. A detailed explanation for the bullish/bearish rating, taking into account the weighted importance of each indicator.
        """

    def analyze_report(self) -> Dict[str, Any]:
        # Generate the prompt
        prompt = self.generate_prompt()
        try:
            # Get the response from the LLM
            response = self.llm.predict(prompt)
            # Parse the structured response
            parsed_response = self.parser.parse(response)
            return parsed_response
        except Exception as e:
            # Handle any errors that occur during the LLM prediction
            print(f"Error generating response from the language model: {e}")
            return {}