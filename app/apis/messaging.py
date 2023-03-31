from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.dantic.messaging import MessageDANT

router = APIRouter()

