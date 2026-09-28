import random

from agent.schema import Scenario


class ScenarioController:

    def __init__(self):
        self.camera_types = [
            "wide_rgb",
            "narrow_rgb"
        ]

        self.altitudes = [
            500,
            750,
            1000,
            1250,
            1500
        ]

        self.viewpoints = [
            "nadir",
            "near_nadir",
            "oblique"
        ]

        self.object_classes = [
            "military_tank",
            "artillery",
            "human_with_gun",
            "military_truck",
            "military_tent",
            "military_bridge"
        ]

        self.terrains = [
            "agricultural",
            "suburban",
            "desert",
            "forest",
            "mountainous"
        ]

        self.lighting = [
            "day",
            "dawn",
            "dusk",
            "night"
        ]

        self.weather = [
            "clear",
            "cloudy",
            "hazy",
            "rainy",
            "foggy"
        ]

        self.arrangements = [
            "random",
            "clustered",
            "line",
            "road",
            "grid"
        ]

        self.occlusions = [
            "none",
            "low",
            "medium",
            "high"
        ]

        self.image_quality = [
            "clean",
            "motion_blur",
            "atmospheric_haze",
            "sensor_noise"
        ]

    def generate_scenario(self):

        camera_type = random.choice(self.camera_types)

        # --------------------------------
        # Camera-dependent altitude
        # --------------------------------

        if camera_type == "wide_rgb":
            altitude = random.choice([
                750,
                1000,
                1250,
                1500
            ])

        else:
            altitude = random.choice([
                300,
                500,
                750,
                1000
            ])

        viewpoint = random.choice(self.viewpoints)

        object_class = random.choice(self.object_classes)

        # --------------------------------
        # Object count
        # --------------------------------

        object_count = random.randint(1, 4)

        # --------------------------------
        # Object size
        # --------------------------------

        if altitude >= 1250:
            object_size = random.choice([
                "tiny",
                "small"
            ])

        elif altitude >= 750:
            object_size = random.choice([
                "small",
                "medium"
            ])

        else:
            object_size = random.choice([
                "medium",
                "large"
            ])

        terrain = random.choice(self.terrains)

        lighting = random.choice(self.lighting)

        weather = random.choice(self.weather)

        # --------------------------------
        # Object arrangement
        # --------------------------------

        if object_class in [
           "military_tank",
            "artillery",
            "human_with_gun",
            "military_truck",
        ]:
            arrangement = random.choice([
                "random",
                "clustered",
                "line",
                "road"
            ])

        elif object_class == "military_bridge":
            arrangement = random.choice([
                "random",
            ])

        else:
            arrangement = random.choice([
                "random",
                "clustered",
                "line"
            ])

        occlusion = random.choice(self.occlusions)

        image_quality = random.choice(self.image_quality)

        # --------------------------------
        # Scene context
        # --------------------------------

        contexts = [
            "rural road intersection",
            "open agricultural field",
            "urban street",
            "suburban neighborhood",
            "industrial area",
            "coastal settlement",
            "mountain road",
            "forest clearing",
            "desert road",
            "highway"
        ]

        scene_context = random.choice(contexts)

        return Scenario(
            camera_type=camera_type,
            altitude_m=altitude,
            viewpoint=viewpoint,
            object_class=object_class,
            object_count=object_count,
            object_size=object_size,
            terrain=terrain,
            lighting=lighting,
            weather=weather,
            object_arrangement=arrangement,
            occlusion=occlusion,
            image_quality=image_quality,
            scene_context=scene_context
        )