from fastapi import FastAPI,Path,HTTPException,Query
import json


app = FastAPI()


# function to load patient's data
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        
    return data
    


@app.get('/')
def hello():
    return {"message":"Patients management system"}

@app.get('/about')
def about():
    return {'message':"A fully functional API  to manage parients record"}

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
    

    
    




