import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui import prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent

from api.database.models import Student

app = FastAPI()


async def get_students():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/students/list/") as response:
            students_dict = await response.json()
            students = [
                Student.model_validate(student) for student in students_dict["students"]
            ]
            return students


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def students_table() -> list[AnyComponent]:
    """
    Show a table of four students, `/api` is the endpoint the frontend will connect to
    when a student visits `/` to fetch components to render.
    """
    students = await get_students()
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text="Students", level=2),  # renders `<h2>Students</h2>`
                c.Table(
                    data=students,
                    # define two columns for the table
                    columns=[
                        # the first is the students, name rendered as a link to their profile
                        DisplayLookup(
                            field="name", on_click=GoToEvent(url="/student/{id}/")
                        ),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field="surname"),
                    ],
                ),
            ]
        ),
    ]


@app.get(
    "/api/student/{student_id}/",
    response_model=FastUI,
    response_model_exclude_none=True,
)
async def student_profile(student_id: str) -> list[AnyComponent]:
    """
    Student profile page, the frontend will fetch this when the student visits `/student/{id}/`.
    """
    print(1)
    try:
        student = next(u for u in await get_students() if u.id == student_id)
        print(student)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Student not found")
    return [
        c.Page(
            components=[
                c.Heading(text=student.name, level=2),
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Details(data=student),
            ]
        ),
    ]


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
