from pydantic import BaseModel,EmailStr,Field
from typing import List,Dict,Optional,Annotated

class Patients(BaseModel):
    name:Annotated[str,Field(max_length=50,title='Name of the patient',description='Give the name of the patient within 50 characters',examples=['Abhi','pratap'])]
    email:Optional[EmailStr]=None
    age:int = Field(gt=0,lt=120)
    weight:Annotated[float,Field(gt=0,strict=True)]
    married:bool=False
    allergies:Optional[List[str]]=Field(max_length=5)
    contact_details:Dict[str,str]
    
patient_info = {'name':"Abhi pratap singh","age":21,'weight':75.2,'married':False,'allergies':['pollen','dust'],'contact_details':{'email':'abc@gmail.com','phone':'95545653'}}

Patient1 = Patients(**patient_info)

def insert_patient(patient:Patients):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)  
    print('inserted')
      
insert_patient(Patient1)