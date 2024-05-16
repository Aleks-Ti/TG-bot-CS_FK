import logging
import os


async def delete_image_in_system(file_path: str):
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as err:
        logging.exception(f"Error delet file: {err}")
        raise err
