from pydantic import BaseSettings

#TO CHECK ALL THE ENVIRONMENT VARIABLES ARE THERE
class Settings(BaseSettings):#checks local environment variablea (IN THE HOST)to see if the following variables are there
   database_hostname:str
   database_port:str
   database_password:str
   database_name:str
   database_username:str
   secret_key:str
   algorithm:str
   access_token_expire_minutes:int
  
   class Config:
       env_file=".env"


settings= Settings()


