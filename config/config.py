import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://BackEndAppDev:DEVBACKEND@clusterappdev.yllqdiq.mongodb.net/?retryWrites=true&w=majority")