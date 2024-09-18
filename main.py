from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, book_routes

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(book_routes.router, prefix="/books", tags=["books"])
