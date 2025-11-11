from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None,alias="_id")
    project_id:str = Field(...,min_length=1)

    @validator("project_id")
    def validate_projectId(cls,value):
        if not value.isalnum():
            raise ValueError("Project Id must be alpha numeric!")
        return value
    
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indecies(cls):
        return [{
            "key":[
                ("project_id",1)
            ],
            "name":"project_id_index_1",
            "unique":True

         }
            
        ]
