from pydantic import BaseModel
from typing import Literal


class Scenario(BaseModel):

    camera_type: Literal[
        "wide_rgb",
        "narrow_rgb"
    ]

    altitude_m: int

    viewpoint: Literal[
        "nadir",
        "near_nadir",
        "oblique"
    ]

    object_class: Literal[
        "military_tank",
        "artillery",
        "human_with_gun",
        "military_truck",
        "military_tent",
        "military_bridge"
    ]

    object_count: int

    object_size: Literal[
        "tiny",
        "small",
        "medium",
        "large"
    ]

    terrain: Literal[
        "agricultural",
        "suburban",
        "desert",
        "forest",
        "coastal",
        "mountainous"
    ]

    lighting: Literal[
        "day",
        "dawn",
        "dusk",
        "night"
    ]

    weather: Literal[
        "clear",
        "cloudy",
        "hazy",
        "rainy",
        "foggy"
    ]

    object_arrangement: Literal[
        "random",
        "clustered",
        "line",
        "road",
        "grid"
    ]

    occlusion: Literal[
        "none",
        "low",
        "medium",
        "high"
    ]

    image_quality: Literal[
        "clean",
        "motion_blur",
        "atmospheric_haze",
        "sensor_noise"
    ]

    scene_context: str


class GeneratedPrompt(BaseModel):

    positive_prompt: str

    negative_prompt: str

    scene_description: str

    expected_objects: int