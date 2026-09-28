import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("data/synthetic_rgb.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,

            camera_type TEXT,
            altitude_m INTEGER,
            viewpoint TEXT,

            object_class TEXT,
            object_count INTEGER,
            object_size TEXT,

            terrain TEXT,
            lighting TEXT,
            weather TEXT,

            object_arrangement TEXT,
            occlusion TEXT,
            image_quality TEXT,

            scene_context TEXT,

            positive_prompt TEXT,
            negative_prompt TEXT,
            scene_description TEXT,

            expected_objects INTEGER,

            seed INTEGER,
            model TEXT,

            image_path TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_image_metadata(
    scenario,
    generated_prompt,
    seed,
    model,
    image_path
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO images (
            camera_type,
            altitude_m,
            viewpoint,
            object_class,
            object_count,
            object_size,
            terrain,
            lighting,
            weather,
            object_arrangement,
            occlusion,
            image_quality,
            scene_context,
            positive_prompt,
            negative_prompt,
            scene_description,
            expected_objects,
            seed,
            model,
            image_path,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        scenario.camera_type,
        scenario.altitude_m,
        scenario.viewpoint,

        scenario.object_class,
        scenario.object_count,
        scenario.object_size,

        scenario.terrain,
        scenario.lighting,
        scenario.weather,

        scenario.object_arrangement,
        scenario.occlusion,
        scenario.image_quality,

        scenario.scene_context,

        generated_prompt.positive_prompt,
        generated_prompt.negative_prompt,
        generated_prompt.scene_description,

        generated_prompt.expected_objects,

        seed,
        model,

        image_path,

        datetime.now().isoformat()
    ))

    image_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return image_id