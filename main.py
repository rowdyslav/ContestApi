import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui import prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent

from database.models import Student

app = FastAPI()


async def get_users():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/students/list/") as response:
            students_dict = await response.json()
            students = [
                Student.model_validate(student) for student in students_dict["students"]
            ]
            return students


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    users = await get_users()
    print(users)
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text="Users", level=2),  # renders `<h2>Users</h2>`
                c.Table(
                    data=users,
                    # define two columns for the table
                    columns=[
                        # the first is the users, name rendered as a link to their profile
                        DisplayLookup(
                            field="name", on_click=GoToEvent(url="/user/{id}/")
                        ),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field="surname"),
                    ],
                ),
            ]
        ),
    ]


@app.get(
    "api/students/{student_id}/",
    response_model=FastUI,
    response_model_exclude_none=True,
)
async def user_profile(student_id: str) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """
    try:
        user = next(u for u in await get_users() if u.id == student_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        c.Page(
            components=[
                c.Heading(text=user.name, level=2),
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Details(data=user),
            ]
        ),
    ]


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
