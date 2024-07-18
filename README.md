# Geosensor HTTP Integration service

This service provides a HTTP-API to be used by a Chirpstack Application as HTTP-Integration.

Requests need to contain a Bearer-Token configured in 'config.py' 'AUTH_TOKEN'.

To run the service:
```bash
$ sudo docker compose up -d
```

To change configuration (e.g. database url) update 'config.py'.

## Request Format

The request data forwarded by Chirpstack is expected to be base64 encoded binary messages including a time followed by n sensor measurements:

Time format (7 bytes):

+--------------------+--------------------+-------------------+
| Field              | DType              | Description       |
+--------------------+--------------------+-------------------+
| year               | uint16 (2 bytes)   | year (e.g. 2024)  |
| month              | uint8  (1 byte)    | month (1-12)      |
| day                | uint8  (1 byte)    | day (1-31)        |
| hour               | uint8  (1 byte)    | hour (0-23)       |
| minute             | uint8  (1 byte)    | minute (0-59)     |
| second             | uint8  (1 byte)    | second (0-59)     |
+--------------------+--------------------+-------------------+

Sensor measurements format (9 bytes):

+--------------------+------------------------+---------------------------------------+
| Field              | DType                  | Description                           |
+--------------------+------------------------+---------------------------------------+
| sensor_id          | unsigned char (1 byte) | Unique ID of the soil-moisture sensor |
| water_content      | float  (4 bytes)       | soil moisture in percent              |
| temperature        | float  (4 bytes)       | soil temperature in celsius           |
+--------------------+------------------------+---------------------------------------+
