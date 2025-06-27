# application.py - Wrapper for AWS Elastic Beanstalk
from main import app

# Elastic Beanstalk busca 'application' como punto de entrada
application = app

if __name__ == "__main__":
    # Para desarrollo local
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8000)
