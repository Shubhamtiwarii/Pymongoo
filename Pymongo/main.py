from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import FastAPI,Request,HTTPException, status
from typing import List
from bson import ObjectId

mongo_url="mongodb+srv://shubhamtca1901098:G5Cw1W5zUKXclsbD@cluster0.u9b6whi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
conn=MongoClient(mongo_url)
#conn=MongoClient()
db=conn['student']
db_collection=db['student']



class Address(BaseModel):
    city: str
    country: str

class Students(BaseModel):
    name: str
    age: int
    address: Address


app = FastAPI()

#For Create
@app.post("/students",status_code=201)
def create_students(student:Students):
    # Insert student data into MongoDB
    inserted_student = db_collection.insert_one(student.dict())
    # Check if insertion was successful
    if inserted_student:
        return {"message": "Student created successfully", "id": str(inserted_student.inserted_id)}
        
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create student")
    

#For List
@app.get("/students", response_model=List[Students])
def list_students():
    students = []
    for student_data in db_collection.find():
        students.append(Students(**student_data))
    return students

#For Fetch
@app.get("/students/{id}", response_model=Students)

def fetch_students(id: str):
    id = ObjectId(id)
    student_data = db_collection.find_one({"_id": id})
    print(student_data)
    if student_data:
        return Students(**student_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    

#For Updated
@app.patch("/students/{id}", status_code=status.HTTP_200_OK)
def update_student(id: str, student: Students):
    id = ObjectId(id)
    update_fields = student.dict(exclude_unset=True)
    updated_student = db_collection.update_one({"_id": id}, {"$set": update_fields})
    if updated_student.modified_count > 0:
        return {"message": "Student updated successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

#For Delete
@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
def delete_student(id: str):
    id = ObjectId(id)
    deleted_student = db_collection.delete_one({"_id": id})
    if deleted_student.deleted_count > 0:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")