import json
import time
import uuid
from pathlib import Path

import requests


class ComfyUIClient:

    def __init__(
        self,
        server_url="http://127.0.0.1:8188",
        workflow_path="workflows/flux2_klein_api.json",
        output_dir="data/images"
    ):
        self.server_url = server_url.rstrip("/")
        self.workflow_path = Path(workflow_path)
        self.output_dir = Path(output_dir)

        # Create our project image folder
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_workflow(self):
        with open(self.workflow_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate(
        self,
        prompt_text,
        seed=None,
        filename_prefix="synthetic_rgb"
    ):

        workflow = self.load_workflow()

        # --------------------------------
        # Update prompt
        # --------------------------------
        workflow["12"]["inputs"]["text"] = prompt_text

        # --------------------------------
        # Update seed
        # --------------------------------
        if seed is None:
            seed = uuid.uuid4().int % (2**63)

        workflow["19"]["inputs"]["noise_seed"] = seed

        # --------------------------------
        # Update ComfyUI filename prefix
        # --------------------------------
        workflow["22"]["inputs"]["filename_prefix"] = filename_prefix

        # --------------------------------
        # Submit workflow
        # --------------------------------
        client_id = str(uuid.uuid4())

        payload = {
            "prompt": workflow,
            "client_id": client_id
        }

        response = requests.post(
            f"{self.server_url}/prompt",
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        prompt_id = result["prompt_id"]

        print(f"ComfyUI prompt submitted: {prompt_id}")
        print(f"Seed: {seed}")

        # --------------------------------
        # Wait for generation
        # --------------------------------
        while True:

            history_response = requests.get(
                f"{self.server_url}/history/{prompt_id}",
                timeout=30
            )

            history_response.raise_for_status()

            history = history_response.json()

            if prompt_id in history:

                job = history[prompt_id]

                if "outputs" in job:

                    print("Generation completed.")

                    outputs = job["outputs"]

                    # --------------------------------
                    # Download generated images
                    # --------------------------------
                    saved_images = []

                    for node_id, node_output in outputs.items():

                        if "images" not in node_output:
                            continue

                        for image in node_output["images"]:

                            filename = image["filename"]
                            subfolder = image.get("subfolder", "")
                            folder_type = image.get("type", "output")

                            # Get image from ComfyUI
                            params = {
                                "filename": filename,
                                "subfolder": subfolder,
                                "type": folder_type
                            }

                            image_response = requests.get(
                                f"{self.server_url}/view",
                                params=params,
                                timeout=60
                            )

                            image_response.raise_for_status()

                            # --------------------------------
                            # Save into our project
                            # --------------------------------
                            save_path = self.output_dir / filename

                            with open(save_path, "wb") as f:
                                f.write(image_response.content)

                            saved_images.append(str(save_path))

                            print(f"Image saved: {save_path}")

                    return {
                        "prompt_id": prompt_id,
                        "seed": seed,
                        "outputs": outputs,
                        "saved_images": saved_images
                    }

            time.sleep(1)