from scenario_controller import ScenarioController

from agent.prompt_agent import PromptAgent
from generator.comfyui import ComfyUIClient

from database.db import (
    initialize_database,
    save_image_metadata
)

from config import GEMINI_API_KEY


# ============================================
# Configuration
# ============================================

NUM_IMAGES = 10

COMFYUI_URL = "http://127.0.0.1:8188"

WORKFLOW_PATH = "workflows/flux2_klein_api.json"

MODEL_NAME = "FLUX.2 Klein 4B"


# ============================================
# Initialize components
# ============================================

initialize_database()

controller = ScenarioController()

agent = PromptAgent(GEMINI_API_KEY)

comfy = ComfyUIClient(
    server_url=COMFYUI_URL,
    workflow_path=WORKFLOW_PATH,
    output_dir="data/images"
)


# ============================================
# Generate dataset
# ============================================

for i in range(NUM_IMAGES):

    print("\n")
    print("=" * 60)
    print(f"GENERATING IMAGE {i + 1}/{NUM_IMAGES}")
    print("=" * 60)

    # ----------------------------------------
    # 1. Generate scenario
    # ----------------------------------------

    scenario = controller.generate_scenario()

    print("\nSCENARIO:")
    print(scenario.model_dump_json(indent=2))


    # ----------------------------------------
    # 2. Gemini generates image prompt
    # ----------------------------------------

    print("\nGenerating prompt with Gemini...")

    result = agent.generate_prompt(scenario)

    print("\nPOSITIVE PROMPT:")
    print(result.positive_prompt)

    print("\nSCENE:")
    print(result.scene_description)


    # ----------------------------------------
    # 3. Generate image with ComfyUI
    # ----------------------------------------

    print("\nGenerating image with ComfyUI...")

    generation = comfy.generate(
        prompt_text=result.positive_prompt,
        filename_prefix=f"synthetic_rgb_{i + 1:05d}"
    )


    # ----------------------------------------
    # 4. Save metadata to database
    # ----------------------------------------

    for image_path in generation["saved_images"]:

        image_id = save_image_metadata(
            scenario=scenario,
            generated_prompt=result,
            seed=generation["seed"],
            model=MODEL_NAME,
            image_path=image_path
        )

        print(f"\nDatabase record created: {image_id}")
        print(f"Image: {image_path}")


print("\n")
print("=" * 60)
print("DATASET GENERATION COMPLETE")
print("=" * 60)