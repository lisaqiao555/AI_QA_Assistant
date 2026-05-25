import json

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database import engine, SessionLocal
from models import Base, Requirement, TestCase
from openai_service import generate_test_cases


Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    db = SessionLocal()

    requirements = db.query(Requirement).order_by(
        Requirement.id.desc()
    ).all()

    for req in requirements:
        count = db.query(TestCase).filter(
            TestCase.requirement_id == req.id
        ).count()

        req.has_test_cases = count > 0

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "requirements": requirements
        }
    )


@app.post("/add-requirement")
def add_requirement(
    title: str = Form(...),
    module: str = Form(...),
    description: str = Form(...)
):
    db = SessionLocal()

    requirement = Requirement(
        title=title,
        module=module,
        description=description
    )

    db.add(requirement)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )


@app.post("/generate-testcases/{requirement_id}")
def generate_testcases(requirement_id: int):
    db = SessionLocal()

    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id
    ).first()

    if requirement is None:
        db.close()
        return RedirectResponse(
            url="/",
            status_code=303
        )

    # Optional: delete old test cases before regenerating
    db.query(TestCase).filter(
        TestCase.requirement_id == requirement_id
    ).delete()

    ai_result = generate_test_cases(requirement.description)

    test_cases = json.loads(ai_result)

    for tc in test_cases:
        new_tc = TestCase(
            requirement_id=requirement.id,
            test_case_id=tc.get("test_case_id"),
            title=tc.get("title"),
            priority=tc.get("priority"),
            precondition=tc.get("precondition"),
            steps=tc.get("steps"),
            expected_result=tc.get("expected_result")
        )

        db.add(new_tc)

    db.commit()
    db.close()

    return RedirectResponse(
        url=f"/testcases/{requirement_id}",
        status_code=303
    )


@app.get("/testcases/{requirement_id}")
def view_testcases(request: Request, requirement_id: int):
    db = SessionLocal()

    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id
    ).first()

    test_cases = db.query(TestCase).filter(
        TestCase.requirement_id == requirement_id
    ).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="testcases.html",
        context={
            "requirement": requirement,
            "test_cases": test_cases
        }
    )