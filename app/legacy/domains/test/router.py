from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.legacy.db.models import User, Base, Cote, Message
from app.legacy.utils.testing_helper import TestingHelper

router = APIRouter()


@router.post("/setup")
def setup_tables(test_helper: TestingHelper = Depends()):
    models = [
        User,
        Cote,
        Message,
    ]
    test_helper.generate_tables(base=Base, models=models)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={
            "detail": f"{[model.__tablename__ for model in models]} have been created successfully!"
        }
    )
