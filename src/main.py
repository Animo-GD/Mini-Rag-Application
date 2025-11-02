from fastapi import FastAPI
from routes import routes,data




app = FastAPI()
app.include_router(routes.base_router)
app.include_router(data.data_router)

