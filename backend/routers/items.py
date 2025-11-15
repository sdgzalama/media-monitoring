from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["Media Items"])

@router.get("/")
def get_items():
    return {"message": "List of media items"}
