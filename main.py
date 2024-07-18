from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.requests import Request
import uvicorn
import uvicorn.config
import uvicorn.logging
import logging
from typing import Annotated, cast

import config
from services.database import init_database
from helpers.log_formatter import ColorFormatter
from helpers.decoder import decode, str_to_time
from filters.token import get_token
from models.sensor import SensorData
from services.database import AsyncSession, get_db_session

app = FastAPI()

# configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize services on startup
async def startup_event():
    logging.info("Start loading database...")
    await init_database()
app.add_event_handler("startup", startup_event)

# create event-api endpoint
@app.post("/")
async def event_api(
        req: Request,
        db: Annotated[AsyncSession, Depends(get_db_session)],
        token: Annotated[str, Depends(get_token)],
    ):
    typ = req.query_params["event"]
    logging.info(f"Request received of event {typ}")
    if typ == "up":
        logging.info("Processing up event...")
        up = await req.json()
        device_id = up["deviceInfo"]["deviceName"]
        time_receive = str_to_time(up["time"])
        try:
            data = decode(up["data"])
        except ValueError as e:
            logging.error(f"Decoding error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload")
        time_send = data["time"]
        try:
            for sensor_id, values in data["sensors"].items():
                water = values["water_content"]
                temp = values["temperature"]
                logging.debug(f"Adding sensor-data entry: {device_id}, {sensor_id}, {time_send}, {time_receive}, {water}, {temp}")
                data = SensorData(
                    device_id=device_id,
                    sensor_id=sensor_id,
                    time_send=time_send,
                    time_receive=time_receive,
                    water_content=water,
                    temperature=temp
                )
                db.add(data)
            await db.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
            logging.info("Failed to add sensor-data entries. Rolling back...")
            await db.rollback()
        logging.info("Finished processing event!")
    return {}

if __name__ == '__main__':
    # configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter())
    logger.addHandler(handler)
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(levelprefix)s %(asctime)s - %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    log_config["formatters"]["default"]["fmt"] = "%(levelprefix)s %(asctime)s - %(message)s"

    # run the service
    uvicorn.run("main:app", host=config.API_HOST, port=config.API_PORT, log_config=log_config)
