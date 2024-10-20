import json


def get_timestamp_str(json_file_name):
    try:
        with open(json_file_name, "r") as file:
            data = json.load(file)
            taken_timestamp = data["photoTakenTime"]["timestamp"]
            if taken_timestamp is None:
                raise KeyError("timestamp not found in JSON data")

            return taken_timestamp

    except (FileNotFoundError, IOError) as e:
        raise Exception(
            f"Error occurred while opening or reading JSON file: {e}"
        )
    except json.JSONDecodeError as e:
        raise Exception(f"Error occurred while parsing JSON: {e}")


def format_timestamp(timestamp_str):
    try:
        timestamp_int = int(timestamp_str)
    except:
        raise ValueError(
            f"Timestamp '{timestamp_str}'"
            "cannot be interpreted as an integer."
        )
    if timestamp_int < 0:
        raise ValueError("Timestamp is too small.")

    if timestamp_int > 4294967295:
        raise ValueError("Timestamp is too big.")

    return timestamp_int


def get_timestamp_from_json(json_file_name):
    return format_timestamp(get_timestamp_str(json_file_name))
