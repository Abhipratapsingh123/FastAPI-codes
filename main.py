from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional


app = FastAPI()


# function to load patient's data
def load_data():
    with open('Data\patients.json','r') as f:
        data = json.load(f)
        
    return data

def save_data(data):
    with open('Data\patients.json','w') as f:
        json.dump(data,f)
    


@app.get('/')
def hello():
    return {"message":"Patients management system"}

@app.get('/about')
def about():
    return {'message':"A fully functional API  to manage patient's record"}

@app.get('/view')
def view():
    data = load_data()
    return data

# specific patient load_data

@app.get('/view/{patient_id}')
def view_specific(patient_id:str = Path(...,description='Id of the patient',example='P001')):
    #laod all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')


# use of query parameter


@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Sort on the basis of height,weight or BMI'),order:str=Query('asc',description='sort in asc or desc order')):
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select from between asc and desc')
    
    data = load_data()
    sort_order = True if order =='desc' else False
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data


## post request
# steps --> user send data --> validate data --> add to existing data

# Pydantic model for input data validation
class Patient(BaseModel):   
    id:Annotated[str,Field(...,description="Id of the patient",examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description="City where the patint is living")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient in mtrs")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in kg")]
    
    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi = round(self.weight/self.height**2,2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.calculate_bmi < 18.5:
            return 'UnderWeight'
        elif self.calculate_bmi < 25:
            return "Normal"
        elif self.calculate_bmi < 30:
            return "Normal"
        else:
            return "Obese"
        
        
@app.post('/create')
def create_patient(patient:Patient):
    # load existing data
    data = load_data()
    
    # check whether the new patient already in the data or not
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    #convert pydantic model into python dictionary and create new key,value pair
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # dump into existing data by converting to json format
    
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})
    
    

## PUT request to update existing data
## sreps --> New pydantic model--> Validatedata and put new data in existing data
    
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]
    
# endpoint

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]
    
    #first convert the patient_update into a dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        existing_patient_info[key]= value
        
    # we also have to update bmi and verdit so we have to make a pydantic object first
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    # pydantic obj -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    
    data[patient_id]= existing_patient_info
    
    # save data
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':"Patient updated"})


## deleting end point
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':"Patient's data deleted"})

    

    
    




