import uvicorn
from server.main import app
# from MQTT import pub
import asyncio



if __name__ == "__main__":
    uvicorn.run(app, host="192.168.7.127", port=8005)
   
