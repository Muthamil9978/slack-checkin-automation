from fastapi import APIRouter

yes = APIRouter(tags = ['user det'])

@yes.get("/")
def read_root():
    return {"Hello": "World"}