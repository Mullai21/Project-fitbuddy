from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import (
    get_db, save_user, save_plan, get_original_plan,
    update_plan, get_user, get_all_users, get_all_plans, delete_user, Plan
)
from app.schemas import UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate input via Pydantic
    try:
        user_input = UserInput(
            name=name, user_id=user_id, age=age, weight=weight,
            goal=goal, intensity=intensity
        )
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Invalid input. Please check your entries and try again."}
        )

    try:
        # Generate workout plan via Gemini Pro
        workout_plan = generate_workout_gemini(
            goal=user_input.goal,
            intensity=user_input.intensity,
            age=user_input.age,
            weight=user_input.weight
        )

        # Generate nutrition tip via Gemini Flash
        nutrition_tip = generate_nutrition_tip_with_flash(goal=user_input.goal)

        # Persist user and plan to database
        user_data = user_input.model_dump()
        save_user(db, user_data)
        save_plan(db, user_id=user_input.user_id, plan=workout_plan, tip=nutrition_tip)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user_data,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
            }
        )
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "An error occurred while generating your plan. Please try again."}
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate feedback input
    try:
        feedback_input = FeedbackRequest(user_id=user_id, feedback=feedback)
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Invalid feedback. Please provide at least 3 characters."}
        )

    # Fetch user and original plan
    user = get_user(db, user_id=feedback_input.user_id)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": f"User '{feedback_input.user_id}' not found. Please generate a plan first."}
        )

    original_plan = get_original_plan(db, user_id=feedback_input.user_id)
    if not original_plan:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "No existing plan found for this user. Please generate a plan first."}
        )

    try:
        # Generate updated plan via Gemini Pro
        updated_plan_text = update_workout_plan(
            original_plan=original_plan,
            feedback=feedback_input.feedback
        )

        # Persist the update (original is preserved)
        update_plan(db, user_id=feedback_input.user_id,
                    updated_plan=updated_plan_text, feedback=feedback_input.feedback)

        # Fetch nutrition tip for re-rendering
        plan_record = db.query(Plan).filter(Plan.user_id == feedback_input.user_id).first()
        nutrition_tip = plan_record.nutrition_tip if plan_record else ""

        user_dict = {
            "name": user.name,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity
        }

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user_dict,
                "workout_plan": original_plan,
                "updated_plan": updated_plan_text,
                "nutrition_tip": nutrition_tip,
                "feedback_success": True,
            }
        )
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "An error occurred while updating your plan. Please try again."}
        )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    plans = get_all_plans(db)

    # Index plans by user_id for quick lookup
    plan_dict = {p.user_id: p for p in plans}

    # Build a flat list of dicts for easy template access
    users_with_plans = []
    for u in users:
        plan = plan_dict.get(u.user_id)
        users_with_plans.append({
            "name": u.name,
            "user_id": u.user_id,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "original_plan": plan.original_plan if plan else "No plan generated",
            "updated_plan": plan.updated_plan if plan else None,
            "nutrition_tip": plan.nutrition_tip if plan else "",
            "feedback": plan.feedback if plan else None,
        })

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users_with_plans": users_with_plans}
    )


@router.post("/delete-user/{user_id}")
async def delete_user_route(user_id: str, request: Request, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)
