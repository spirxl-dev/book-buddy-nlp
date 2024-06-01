from fastapi import APIRouter

router = APIRouter()


@router.get("/recommendations")
def get_recommendations():
    # TODO: Logic to fetch personalised book recommendations
    pass
