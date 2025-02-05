import base64
import struct
from datetime import datetime
import logging

def decode(s: str) -> dict:
    """Decodes sensor data from base64-encoded binary payload

    Args:
        s: Payload

    Returns:
        A dict with keys "time" (contains send time) and "sensors" (contains dict of individual sensor results)
    """
    b = base64.b64decode(s)
    year = struct.unpack_from('H', b, 0)[0]
    month = struct.unpack_from('B', b, 2)[0]
    day = struct.unpack_from('B', b, 3)[0]
    hour = struct.unpack_from('B', b, 4)[0]
    minute = struct.unpack_from('B', b, 5)[0]
    second = struct.unpack_from('B', b, 6)[0]
    if year < 0 or month < 0 or month > 12 or day < 0 or day > 31 or hour < 0 or hour > 23 or minute < 0 or minute > 59 or second < 0 or second > 59:
        raise ValueError("Invalid time")
    time = datetime(year, month, day, hour, minute, second)
    data = {
        "time": time,
        "sensors": {}
    }
    num_sensors = int((len(b) - 7) / 9)
    for i in range(num_sensors):
        addr = struct.unpack_from('c', b, 7 + 9*i)[0]
        water = struct.unpack_from('f', b, 7 + 9*i + 1)[0]
        temp = struct.unpack_from('f', b, 7 + 9*i + 5)[0]
        # check for invalid values
        if water < 0.0 or water > 100.0 or temp < -50.0 or temp > 100.0:
            logging.error("Invalid sensor data received. Skipping this sensor...")
            continue
        data["sensors"][str(addr, "utf-8")] = {
            "water_content": water,
            "temperature": temp,
        }
    return data

def str_to_time(time_str: str) -> datetime:
    """Decodes receive time from chirpstack time string

    Args:
        time_str: Time as recieved from chirpstack

    Returns:
        Recieve time
    """
    year = int(time_str[:4])
    month = int(time_str[5:7])
    day = int(time_str[8:10])
    hour = int(time_str[11:13])
    minute = int(time_str[14:16])
    second = int(time_str[17:19])
    return datetime(year, month, day, hour, minute, second)
