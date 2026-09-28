import time
from google import genai
from google.genai import types

from .schema import Scenario, GeneratedPrompt


class PromptAgent:

    def __init__(self, api_key: str):

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.8-flash"

    def generate_prompt(
        self,
        scenario: Scenario
    ) -> GeneratedPrompt:

        system_instruction = """
You are an expert synthetic aerial RGB dataset prompt generator.

Convert the structured scenario into a precise
photorealistic image-generation prompt.

Rules:
1. Preserve every requested scenario value.
2. Preserve the requested object count.
3. Preserve the requested viewpoint.
4. Preserve the requested altitude.
5. Preserve terrain, lighting and weather.
6. Make objects visually distinguishable.
7. Describe realistic aerial perspective and scale.
8. Do not introduce unnecessary objects.
9. Optimize the prompt for photorealistic RGB image generation.
"""

        user_prompt = f"""
Generate an image-generation prompt for this scenario:

{scenario.model_dump_json(indent=2)}
"""

        for attempt in range(5):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[
                        system_instruction,
                        user_prompt
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=GeneratedPrompt,
                        temperature=0.7,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(
                            disable=True
                        )
                    )
                )

                return GeneratedPrompt.model_validate_json(
                    response.text
                )

            except Exception as e:

                if "503" not in str(e):
                    raise

                if attempt == 4:
                    raise

                wait_time = 5 * (2 ** attempt)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)