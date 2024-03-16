import os
import threading

import uvicorn

from app.main import app
from utils.producer import generate_messages
from utils.consumer import start_consumer


if __name__ == "__main__":

    a = threading.Thread(target=start_consumer, daemon=True)
    a.start()

    generate_messages()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("SOCIAL_PORT")),
    )
