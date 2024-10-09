from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui import prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from pydantic import BaseModel, ConfigDict, EmailStr, Field

app = FastAPI()


# class Student(BaseModel):
#     id: int = Field()
#     name: str = Field(...)
#     dob: date = Field(...)

#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,
#     )


# users = [
#     Student(id=1, name="John", dob=date(1990, 1, 1)),
#     Student(id=2, name="Jack", dob=date(1991, 1, 1)),
#     Student(id=3, name="Jill", dob=date(1992, 1, 1)),
#     Student(id=4, name="Jane", dob=date(1993, 1, 1)),
# ]


from api.database.annotations import PyObjectId
from api.database.models import Student

users = [
    Student(
        _id="66fe78b733afdb2c5807406c",
        username="rowdyslav",
        name="Sergey",
        surname="Goretov",
        email="rowdyslav@gmail.com",
    ),
]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text="Students", level=2),  # renders `<h2>Students</h2>`
                c.Table(
                    data=users,
                    # define two columns for the table
                    columns=[
                        # the first is the users, name rendered as a link to their profile
                        DisplayLookup(
                            field="username", on_click=GoToEvent(url="/user/{id}/")
                        ),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field="dob", mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]


@app.get(
    "/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True
)
def user_profile(user_id: str) -> list[AnyComponent]:
    """
    Student profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """
    print(users)
    try:
        user = next(u for u in users if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Student not found")
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
