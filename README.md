##Health Check As A Service
A service that provides health check and monitoring for a canary. Anything can be a canary.

##To Run
1.The service currently uses redis set up on a docker machine, port 192.168.99.100.(If necessary, adjust the port in the file)

2.Run "celery --app=app.worker.tasks worker" to spin up the celery worker.

3.Finally, run manage.py to start the app.

####Examples for project, canary and result

    Project
                {
                    "name" : "new project",
                    "email": "test@rackspace.com",
                    "description": "A canary service that will monitor, keep track, and trend of",
                    "dependencies" : "projectX"	            
                 }
    
    
    Canary
              {
                    "name" : "new canary",
                    "description": "Tests that API responds with correct status code for test cases",
                    "meta_data": {  "region": "Austin"
                    },
                    "criteria" : {
                         "resolution" : "1 hours",
			             "threshold" : 80,
			             "result_sample_size": 10
			         }
                }
                
     Result
                {
                    "status" : "pass",
                    "failure_details" : ""
                    
    
      
    
    
    
    
    
    
    
    
    
    
    