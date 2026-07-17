from sqlmodel import SQLModel, Session , select 
from sqlalchemy.exc import OperationalError
from database import engine , get_session
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from models import Course 

app = FastAPI()
@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database connected Successfully")
    except OperationalError as e:
        print("Database connection Failed", e)

@app.get("/")
def home():
    return {"Message": "Complete"}

#Create
@app.post("/course")
def create_course(course: Course, session: Session = Depends(get_session)):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


#Get all 
@app.get("/course")
def get_courses(session: Session= Depends(get_session)):
    return session.exec(select(Course)).all() 


#Filter with Query Parameter
@app.get("/course/expensive")
def get_courses(min_fee:int , session: Session= Depends(get_session)):
    course = session.exec(select(Course).where(Course.Course_fee >= min_fee)).all()
    if not course :
        raise HTTPException (status_code=404, detail="Not found")
    return course

#Filter with Query Parameter
@app.get("/course/active")
def get_active(session: Session= Depends(get_session)):
    course = session.exec(select(Course).where(Course.is_active==True)).all()
    if not course :
        raise HTTPException (status_code=404, detail="Not found")
    return course

#Get one 
@app.get("/course/{course_id}")
def get_course(course_id: int, session: Session= Depends(get_session)):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course 

#Update 
@app.put("/course/{course_id}")
def update_course(course_id:int, updated: Course, session: Session= Depends(get_session)):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.Course_Name = updated.Course_Name
    course.duration_weak = updated.duration_weak
    course.Course_fee = updated.Course_fee
    session.add(course)
    session.commit()
    session.refresh(course)
    return {
        "Message": "Course Updated",
        "Data": course
    }

#Delete
@app.delete("/course/{course_id}")
def delete_course(course_id: int, session: Session= Depends(get_session)):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    session.delete(course)
    session.commit()
    return {"Message": "Course Deleted Successfully",
            "Data": course}





