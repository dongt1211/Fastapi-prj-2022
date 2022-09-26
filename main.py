from fastapi import Depends, FastAPI, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Predict Gender By Vietnamese Name")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Insert name in database table
## Insert name from keyboard
@app.post("/names/", tags=["Create"])
def create_name_from_keyboard(names: set[str] = Query(), db: Session = Depends(get_db)):
    for person_name in names.copy():
        db_name = crud.get_name_by_name(db, name=person_name)
        if db_name or person_name == "":
            names.remove(person_name)

    return crud.create_result(db=db, results=crud.predict_names(names))


## Insert name from file txt
@app.post("/Uploadfile/", tags = ["Create"])
def create_name_from_file_txt(file: UploadFile = File(default=None), db: Session = Depends(get_db)):
    # Read file and save data in names
    names = set()
    if file and file.filename.endswith('.txt'):
        f = open(file.filename, "rb")
        for x in f:
            names.add(x.decode("utf-8").rstrip())
    else:
        raise HTTPException(status_code=400, detail="Not type of file for processing")
    # Insert name in db
    for person_name in names.copy():
        db_name = crud.get_name_by_name(db, name=person_name)
        if db_name or person_name == "":
            names.remove(person_name)
    return crud.create_result(db=db, results=crud.predict_names(names))


# Get_names_from_table
@app.get("/names/", tags=["Read"])
def read_names(skip_name: int = 0, number_of_names: int = 100, db: Session = Depends(get_db)):
    people = crud.get_names(db, skip=skip_name, limit=number_of_names)
    return people


# Find name by id
@app.get("/names/{name_id}", tags=["Read"])
def read_name_by_id(name_id: int, db: Session = Depends(get_db)):
    db_name = crud.get_name_by_id(db, name_id=name_id)
    if db_name is None:
        raise HTTPException(status_code=404, detail="ID not found")
    return db_name


# Delete name from table by name
@app.delete("/dltnames/{person_name}", tags=["Delete"])
def delete_name_by_name(person_name: str, db: Session = Depends(get_db)):
    name_to_delete = crud.get_name_by_name(db, name=person_name)
    if name_to_delete is None:
        raise HTTPException(status_code=404, detail="Name not found")
    db.delete(name_to_delete)
    db.commit()
    return name_to_delete


# Delete name from table by ID
@app.delete("/IDS/{ID}", tags=["Delete"])
def delete_name_by_id(ID: int, db: Session = Depends(get_db)):
    name_to_delete = crud.get_name_by_id(db, name_id=ID)
    if name_to_delete is None:
        raise HTTPException(status_code=404, detail="ID not found")
    db.delete(name_to_delete)
    db.commit()
    return name_to_delete



