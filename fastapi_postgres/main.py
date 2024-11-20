import fastapi as _fastapi
from typing import TYPE_CHECKING, List
import schemas as _schemas
import sqlalchemy.orm as _orm
import services as _services


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


app = _fastapi.FastAPI()


@app.post("/api/contacts/", response_model=_schemas.Contact)
async def create_contact(
    contact: _schemas.CreateContact,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_contact(contact=contact, db=db)


@app.get("/api/contacts/", response_model=List[_schemas.Contact])
async def get_contacts(db: "Session" = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_contacts(db=db)


@app.get("/api/contacts/{contact_id}", response_model=_schemas.Contact)
async def get_contact(
    contact_id: int, db: "Session" = _fastapi.Depends(_services.get_db)
):
    return await _services.get_contact(contact_id=contact_id, db=db)
