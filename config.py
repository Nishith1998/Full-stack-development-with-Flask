import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string" 
    
    MONGODB_SETTINGS = {'db' : 'UTA_Enrollment' }
        # 'host' : 'mongodb://locolhost:27017/UTA_Enrollment'
    