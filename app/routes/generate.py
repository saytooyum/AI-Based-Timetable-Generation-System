from fastapi import APIRouter
from solver.timetable_solver import generate_simple_timetable

router = APIRouter()

@router.get("/generate")
def generate():
    return {"timetable": generate_simple_timetable()}