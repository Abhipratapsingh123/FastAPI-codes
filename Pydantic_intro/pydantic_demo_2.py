from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated


# model validator allows to implement validation based on multiple field, but field_validator allows only to validate only one field
#computed-field is used to create a new field by using other fields like BMI from height and weight



class Patients(BaseModel):
    name:str
    email:Optional[EmailStr]=None
    age:int
    weight:float
    height:Optional[float]
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str] 
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')
        
        return value
    
    # for name field
    @field_validator('name')
    @classmethod
    def update_name(cls,value):
        return value.upper()
    
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients older than 60 must have an emergency contact")
        
        return model
    
    # computed fields
    
    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/self.height**2,2)
        return bmi

    
patient_info1 = {'name':"Abhi pratap singh","email":"abc@hdfc.com","age":21,'weight':75.2,'married':False,'allergies':['pollen','dust'],'contact_details':{'email':'abc@gmail.com','phone':'95545653'}}


patient_info2 = {'name':"Akshat","email":"ab@icici.com","age":70,'weight':70.2,'height':1.76,'married':False,'allergies':['pollen','dust','bugs'],'contact_details':{'email':'abc@gmail.com','phone':'95545653','emergency':'7587537534753'}}



patient1 = Patients(**patient_info2)
print(patient1)

def update_patient(patient:Patients):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.height)
    print("bmi",patient.calculate_bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)  
    print('inserted')
    
update_patient(patient1)

    