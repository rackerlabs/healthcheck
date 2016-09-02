##Health Check As A Service
Health Check as a Service is an API and UI that reflects the health of a system by providing the
current and historical health as well as graphical views of health trends. It also provides the
ability to view multiple systems in one dashboard and to specify what is considered "healthy" with
thresholds of expected results passing.


##Prerequisites
* Docker or Docker Machine
* Docker Compose
* Node.js


##To Run
To run the service, you need to run the following commands.

```
$ cd ./ui
$ npm install
$ npm run build
$ cd ..
$ docker-compose build
$ docker-compose up
```

The API will be running on `http://localhost:5000` for Linux users and on port 5000 of the `docker-machine` ip address
for non-Linux users. The UI will be on port `http://localhost:5001` or port 5001 of the `docker-machine`.


####Examples for project, canary and result
The basic workflow of this service is to create a project, create "canaries" for that project, and create results
for the status of that canary. Any set of tests, processes, monitoring, etc. that determines the health of a system,
and is also known as a smoke test. Some example requests are:

Project
```
{
    "name" : "new project",
    "email": "test@rackspace.com",
    "description": "A canary service that will monitor, keep track, and trend of",
    "dependencies" : "projectX"
}
```

Canary
```
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
```

Result
```
{
    "status" : "pass",
    "failure_details" : ""
}
```
