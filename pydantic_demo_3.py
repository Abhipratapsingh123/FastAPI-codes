from pydantic import BaseModel

# exporting 

class Address(BaseModel):
    city:str
    state:str
    pincode:str
    
class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address
    
address_dict = {"city":"gurugram","state":"haryana","pincode":"122003"}

address1 = Address(**address_dict)

patient_dict = {"name":"Atharv","gender":"Male","age":"21","address":address1}

patient1 = Patient(**patient_dict)

print(patient1)

temp = patient1.model_dump()
temp = patient1.model_dump_json()
print(temp)
print(type(temp))

    