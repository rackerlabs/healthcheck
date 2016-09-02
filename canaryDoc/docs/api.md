

## Create Project


POST    /projects

This operation makes a new project. Name and email fields cannot be empty, The unique id and name of the project is returned on success

The request and response data format is json.

This table shows the possible response codes for this operation:

| Response Code | Name          | Description      |
| ------------  | ------------- | ---------------- |
| 201           | Created       | Request succeeded|
| 405           | Bad Method    | Bad Method       |
 
 
**Request:**
 
 This table shows the body parameters for the request:
 
 Name                  | Type                   | Description 
------------           | -------------          | ------------
 project.name          | String                 | Project name. 
 project.email         | String                 | The email of the owner of the project
 project.description   | String (Optional)      | Short description about the project 
 project.dependencies  | Array (Optional)       | List of other projects that may depend on this project
 
 
 
 **Example Create project: JSON request**
       
        Content-Type: application/json
        Accept: application/json


        
        {
                "name" : "New Project",
                "email": "test@rackspace.com",
                "description": "A new project",
                "dependencies" : [ projectX, ProjectY, projectZ ]	
        }


**Response:**


 This table shows the body parameters for the response:
 
| Name                  | Type                   | Description            |
|------------           | -------------          | ------------           | 
| project.id            | Uuid                   | The ID of the project  |
| project.name          | String                 | The name of the project|



 **Example Create project: JSON response**

        Status Code: 201 Created
        Content-Type: application/json



        {
                "id" : 1,
                "name" : "New project"
        }






## Retrieve list of Projects




GET /projects

This operation retrieves a list of all projects. The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name          | Description      |
|------------  | ------------- | ---------------- |
| 200          | Success       | Request succeeded|
| 405          | Bad Method    | Bad Method       |
 
 
**Request:**
 
 This operation does not accept a request body
 
 
 
 **Example Retrieves list of projects: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        


**Response:**


 This table shows the body parameters for the response:
 
| Name                  | Type                   | Description                                           |
|------------           | -------------          | ------------                                          | 
| project.id            | Uuid                   | The ID of the project                                 |
| project.name          | String                 | The name of the project                               |
| project.email         | String                 | The email of the owner of the project                        |
| project.description   | String                 | Short description about the project                   | 
| project.dependencies  | Array                  | List of other projects that may depend on this project|


 **Example Retrieves list of projects: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       {
           "projects" : [
                    
                {
                    "name" : "New Project",
                    "email": "test@rackspace.com",
                    "description": "A new project",
                    "dependencies" : [projectX, ProjectY, projectZ],
                    "id" : 1
                },
    
                {
                    "name" : "A new project",
                    "email": "test@rackspace.com",
                    "description": "Another new project",
                    "dependencies" : [ projectX, ProjectY],
                    "id" : 2
                }
    
               ]

       }





## Retrieve a Project




GET /projects/{project_id}

This operation retrieves a project. The ID of the project is required. The request and response data format is json.


This table shows the possible response codes for this operation:

|Response Code | Name          | Description       |
|------------  | ------------- | ----------------  |
| 200          | Success       | Request succeeded |
| 404          | Not found     | Resource not found| 
| 405          | Bad Method    | Bad Method        |
 
 
**Request:**
  This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The Id of the project       |


This operation does not accept a request body
 
 
 **Example Retrieve a project: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        


**Response:**


 This table shows the body parameters for the response:
 
| Name                  | Type                   | Description            |
|------------           | -------------          | ------------           | 
| project.id            | Uuid                   | The ID of the project  |
| project.name          | String                 | The name of the project|
| project.email         | String                 | The email of the owner of the project
| project.description   | String                 | Short description about the project 
| project.dependencies  | Array                  | List of other projects that may depend on this project


 **Example Retrieve a project: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       {
               
                {
                    "name" : "New Project",
                    "email": "test@rackspace.com",
                    "description": "A new project",
                    "dependencies" : [projectX, ProjectY, projectZ],
                    "id" : 1
                }

       }



## Update a Project




PUT /projects/{project_id}

This operation updates one or more editable attributes of a project. All attributes can be edited. To edit the dependencies attribute, 
the whole array should be replaced. You can update any or all of the attributes in a single request.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name          | Description       |
|------------  | ------------- | ----------------  |
| 200          | Success       | Request succeeded |
| 404          | Not Found     | Resource Not found|
| 405          | Bad Method    | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project       |


 
 This table shows the body parameters for the request:
 
 Name                  | Type                   | Description 
------------           | -------------          | ------------
 project.name          | String (Optional)      | Project name. 
 project.email         | String (Optional)      | The email of the owner of the project
 project.description   | String (Optional)      | Short description about the project 
 project.dependencies  | Array  (Optional)      | List of other projects that may depend on this project

 
 
 
 **Example update a project: JSON request**
       
        Content-Type: application/json
        Accept: application/json
       
       
        {
              "name" : "Health Check"
        }
        


**Response:**


 This table shows the body parameters for the response:
 
| Name                  | Type                   | Description            |
|------------           | -------------          | ------------           | 
| project.id            | Uuid                   | The ID of the project  |
| project.name          | String                 | The name of the project|
| project.email         | String                 | The email of the owner of the project
| project.description   | String                 | Short description about the project 
| project.dependencies  | Array                  | List of other projects that may depend on this project


 **Example update a project: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



        {
            "name" : "Health Check",
            "email": "test@rackspace.com",
            "description": "A new project",
            "dependencies" : [ projectX, ProjectY, projectZ ]
            "id" : 1
        }



## Delete a Project



DELETE /projects/{project_id}

This operation deletes a project. If the operation succeeds, it returns an HTTP 204 status code with no response body.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name                   | Description       |
|------------  | -------------          | ----------------  |
| 204          | Delete successful      | Request succeeded |
| 404          | Not Found              | Resource not found|
| 405          | Bad Method             | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|


This operation does not accept a request body


 **Example delete project: JSON request**
       
        Content-Type: application/json
        Accept: application/json
       

**Response:**


 **Example delete a project: JSON response**

        Status Code: 204 No Content
        Content-Type: application/json







## Create Canary


POST /projects/{project_id}/canary

This operation makes a new canary. The ID of the project that owns this canary is required and the canary object is returned on success.

The request and response data format is json.

This table shows the possible response codes for this operation:

| Response Code | Name          | Description      |
| ------------  | ------------- | ---------------- |
| 201           | Created       | Request succeeded|
| 405           | Bad Method    | Bad Method       |
 
 
**Request:**

This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|

 
 
The table below shows the body parameters for the request.
 
Criteria and meta_data fields are json arrays. Resolution can only be in hours or
days.

The criteria attribute should at least have the following fields: 

threshold: The percentage of results with a passing status that is the minimum requirement for a healthy system.

low_threshold : A value below the threshold to be used to decide a "yellow" health status.

resolution : Unit of time to break the a set of results into.

result_sample-size : Number of results to use when determining the health of the canary.
 
 Name                 | Type                   | Description 
------------          | -------------          | ------------
 canary.name          | String                 | Canary name. 
 canary.description   | String (Optional)      | Short description about the canary
 canary.meta_data     | Array (Optional)       | A JSON array of information about this canary
 canary.criteria      | Array                  | A JSON array of customizable criteria for this canary
 
 
 
 **Example Create canary: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        
        
        
         {
                "name" : "new canary",
                "description": "A test canary",
                "meta_data": {  
                    "region": "DFW"
                },
                "criteria" : {
                     "threshold" : 80,
                     "low_threshold" : 70
                     "result_sample_size": 10,
                     "resolution" : "5 hours"
                     
                 }
            }


        
        


**Response:**


 This table shows the body parameters for the response:
 
| Name                 | Type                       | Description                                                      |
|------------          | -------------              | ------------                                                     |  
| canary.id            | Uuid                       | The ID of the canary                                             |
| canary.name          | String                     | The name of the canary                                           |
| canary.meta_data     | Array                      | A JSON array of information about this canary                    |
| canary.description   | String                     | Short description about the canary                               |
| canary.history       | Array                      | A JSON array of health ststus history of the canary              |
| canary.health        | String                     | Startign health status of a new canary (This will be GREEN)      |
| canary.criteria      | Array                      | A JSON array of customizable criteria for this canary            |
| canary.status        | String                     | Stating the state of the canary (This will start out as ACTIVE)  |
| canary.updated_at    | Datetime                   | A time showing when the canary was last updated (This will start out to be the time it was created | 
                                                        



 **Example Create canary: JSON response**

        Status Code: 201 Created
        Content-Type: application/json
    
        
        
        {
              "criteria": {
                "low_threshold": 70,
                "resolution": "5 hours",
                "result_sample_size": 10,
                "threshold": 80
              },
              "description": "A test canary",
              "health": "GREEN",
              "history": {
                "2016-09-02 14:40:29.146770": "GREEN"
              },
              "id": 1,
              "meta_data": {
                "region": "DFW"
              },
              "name": "new canary",
              "status": "ACTIVE",
              "updated_at": "Fri, 02 Sep 2016 14:40:29 GMT"
        }
        




## Retrieve list of Canaries




GET /projects/{project_id}/canary

This operation retrieves a list of all the canaries that belongs to a project. The project ID is required for this request.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name          | Description      |
|------------  | ------------- | ---------------- |
| 200          | Success       | Request succeeded|
| 405          | Bad Method    | Bad Method       |
 
 
**Request:**
 
 This operation does not accept a request body
 
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|

 
 
 **Example Retrieves list of canaries: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        


**Response:**


This table shows the body parameters for the response:
 
 
| Name                 | Type                       | Description                                                      |
|------------          | -------------              | ------------                                                     |  
| canary.id            | Uuid                       | The ID of the canary                                             |
| canary.name          | String                     | The name of the canary                                           |
| canary.meta_data     | Array                      | A JSON array of information about this canary                    |
| canary.description   | String                     | Short description about the canary                               |
| canary.history       | Array                      | A JSON array of health ststus history of the canary              |
| canary.health        | String                     | Startign health status of a new canary (This will be GREEN)      |
| canary.criteria      | Array                      | A JSON array of customizable criteria for this canary            |
| canary.status        | String                     | Stating the state of the canary (This will start out as ACTIVE)  |
| canary.updated_at    | Datetime                   | A time showing when the canary was last updated (This will start out to be the time it was created | 
                                 
                     
                                 
                                 
 **Example Retrieves list of canaries: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       {
           "canaries" : [
                    
             {
                  "criteria": {
                    "low_threshold": 70,
                    "resolution": "5 hours",
                    "result_sample_size": 10,
                    "threshold": 80
                  },
                  "description": "A test canary",
                  "health": "GREEN",
                  "history": {
                    "2016-09-02 14:40:29.146770": "GREEN"
                  },
                  "id": 1,
                  "meta_data": {
                    "region": "DFW"
                  },
                  "name": "new canary",
                  "status": "ACTIVE",
                  "updated_at": "Fri, 02 Sep 2016 14:40:29 GMT"
            },
            
            {
                  "criteria": {
                    "low_threshold": 70,
                    "resolution": "5 hours",
                    "result_sample_size": 10,
                    "threshold": 80
                  },
                  "description": "A test canary",
                  "health": "GREEN",
                  "history": {
                    "2016-09-02 14:40:29.146770": "GREEN"
                  },
                  "id": 2,
                  "meta_data": {
                    "region": "DFW"
                  },
                  "name": "new canary",
                  "status": "ACTIVE",
                  "updated_at": "Fri, 02 Sep 2016 14:40:29 GMT"
            }
        
        
    
           ]

       }



        
 

## Retrieve a Canary




GET /projects/{project_id}/canary/{canary_id}

This operation retrieves a canary. The ID of the project that owns the canary and the ID of the canary is required.
The request and response data format is json.


This table shows the possible response codes for this operation:

|Response Code | Name          | Description       |
|------------  | ------------- | ----------------  |
| 200          | Success       | Request succeeded |
| 404          | Not found     | Resource not found| 
| 405          | Bad Method    | Bad Method        |
 
 
**Request:**

 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|
|{canary_id}           | Uuid          | The ID of the canary |
 
 
This operation does not accept a request body
 
 
 
 **Example Retrieve a canary: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        


**Response:**


This table shows the body parameters for the response:
 
 
| Name                 | Type                       | Description                                                      |
|------------          | -------------              | ------------                                                     |  
| canary.id            | Uuid                       | The ID of the canary                                             |
| canary.name          | String                     | The name of the canary                                           |
| canary.meta_data     | Array                      | A JSON array of information about this canary                    |
| canary.description   | String                     | Short description about the canary                               |
| canary.history       | Array                      | A JSON array of health ststus history of the canary              |
| canary.health        | String                     | Startign health status of a new canary (This will be GREEN)      |
| canary.criteria      | Array                      | A JSON array of customizable criteria for this canary            |
| canary.status        | String                     | Stating the state of the canary (This will start out as ACTIVE)  |
| canary.updated_at    | Datetime                   | A time showing when the canary was last updated (This will start out to be the time it was created | 




 **Example Retrieve a canary: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       {
               
              "criteria": {
                "low_threshold": 70,
                "resolution": "5 hours",
                "result_sample_size": 10,
                "threshold": 80
              },
              "description": "A test canary",
              "health": "GREEN",
              "history": {
                "2016-09-02 14:40:29.146770": "GREEN"
              },
              "id": 1,
              "meta_data": {
                "region": "DFW"
              },
              "name": "new canary",
              "status": "ACTIVE",
              "updated_at": "Fri, 02 Sep 2016 14:40:29 GMT"

       }





## Update a Canary




PUT /projects/{project_id}/canary/{canary_id}

This operation updates one or more editable attributes of a canary. Only the following attributes can be updated:
Name, description, metadata, criteria and health. To edit the meta_data and criteria attributes, 
the whole array should be replaced. You can update any or all of the listed attributes in a single request.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name          | Description       |
|------------  | ------------- | ----------------  |
| 200          | Success       | Request succeeded |
| 404          | Not Found     | Resource Not found|
| 405          | Bad Method    | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|
|{canary_id}           | Uuid          | The ID of the canary |


 
 This table shows the body parameters for the request:
 
| Name                 | Type                       | Description                                                      |
|------------          | -------------              | ------------                                                     |  
| canary.name          | String                     | The name of the canary                                           |
| canary.meta_data     | Array                      | A JSON array of information about this canary                    |
| canary.description   | String                     | Short description about the canary                               |
| canary.health        | String                     | Starting health status of a new canary (This will be GREEN)      |
| canary.criteria      | Array                      | A JSON array of customizable criteria for this canary            |


 
 

 **Example update a canary: JSON request**
       
        Content-Type: application/json
        Accept: application/json
       
       
        {
              "name" : "test canary"
        }
        


**Response:**

This table shows the body parameters for the response:


| Name                 | Type                       | Description                                                      |
|------------          | -------------              | ------------                                                     |  
| canary.id            | Uuid                       | The ID of the canary                                             |
| canary.name          | String                     | The name of the canary                                           |
| canary.meta_data     | Array                      | A JSON array of information about this canary                    |
| canary.description   | String                     | Short description about the canary                               |
| canary.history       | Array                      | A JSON array of health ststus history of the canary              |
| canary.health        | String                     | Startign health status of a new canary (This will be GREEN)      |
| canary.criteria      | Array                      | A JSON array of customizable criteria for this canary            |
| canary.status        | String                     | Stating the state of the canary (This will start out as ACTIVE)  |
| canary.updated_at    | Datetime                   | A time showing when the canary was last updated (This will start out to be the time it was created | 



 **Example update a canary: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       
       {
               
              "criteria": {
                "low_threshold": 70,
                "resolution": "5 hours",
                "result_sample_size": 10,
                "threshold": 80
              },
              "description": "A test canary",
              "health": "GREEN",
              "history": {
                "2016-09-02 14:40:29.146770": "GREEN"
              },
              "id": 1,
              "meta_data": {
                "region": "DFW"
              },
              "name": "test canary",
              "status": "ACTIVE",
              "updated_at": "Fri, 02 Sep 2016 14:40:29 GMT"

       }



## Delete a Canary



DELETE /projects/{project_id}/canary/{canary_id}

This operation deletes a canary. On the first request, the canary is disabled. To completely delete the canary, make this request twice.
If the operation succeeds, it returns an HTTP 204 status code with no response body.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name                   | Description       |
|------------  | -------------          | ----------------  |
| 204          | Delete successful      | Request succeeded |
| 404          | Not Found              | Resource not found|
| 405          | Bad Method             | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|
|{canary_id}           | Uuid          | The ID of the canary |


This operation does not accept a request body


 **Example delete canary: JSON request**
       
        Content-Type: application/json
        Accept: application/json
       

**Response:**


 **Example delete a canary: JSON response**

        Status Code: 200 OK
        Content-Type: application/json
        
        
        {
            
            "Disabled 'test canary' "
        
        }
        
        
        
        OR
        
        
        Status Code: 204 No Content
        Content-Type: application/json
        
        



## Health trend of a Canary


GET /projects/{project_id}/canary/{canary_id}/trend

This operation provides at a glance view of the health trend of a canary. The following values are required for this request:

project_id - The ID of the project that owns the canary.

canary_id - The ID of the canary. 

interval - Time-based range of results to analyze. E.g., an interval of 7 days would encompass all the results created in the past 7 days.

resolution - Unit of time to break the interval into. This can only be in hour(s) or day(s) 

threshold - The percentage of results with a passing status that is the minimum requirement for a healthy system.

low_threshold - A value below the threshold to be used to decide a "yellow" health status.


This table shows the possible response codes for this operation:

|Response Code | Name                   | Description       |
|------------  | -------------          | ----------------  |
| 404          | Not Found              | Resource not found|
| 405          | Bad Method             | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|
|{canary_id}           | Uuid          | The ID of the canary |



        Content-Type: application/json
        Accept: application/json

This operation does not accept a request body and a graph showing the health trend is returned on success






## Get history graph of a Canary


GET /projects/{project_id}/canary/{canary_id}/history

This operation provides at a glance view of the health history of a canary. This history tells what times the canary health has changed 
from one value to the other.

project_id - The ID of the project that owns the canary.

canary_id - The ID of the canary. 



This table shows the possible response codes for this operation:

|Response Code | Name                   | Description       |
|------------  | -------------          | ----------------  |
| 404          | Not Found              | Resource not found|
| 405          | Bad Method             | Bad Method        |
 
 
**Request:**

 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project       |
|{canary_id}           | Uuid          | The ID of the canary        |


        Content-Type: application/json
        Accept: application/json


This operation does not accept a request body and a graph showing the canary history is returned on success




## Create Result


POST /projects/{project_id}/canary/{canary_id}/results

This operation makes a new result. The ID of the project that owns the canary and the ID of the canary that owns the result is required and the result object is returned on success.

The request and response data format is json.

This table shows the possible response codes for this operation:

| Response Code | Name          | Description      |
| ------------  | ------------- | ---------------- |
| 201           | Created       | Request succeeded|
| 405           | Bad Method    | Bad Method       |
 
 
**Request:**

 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project       |
|{canary_id}           | Uuid          | The ID of the canary        |
 
 
The table below shows the body parameters for the request:
 
 
 Name                    | Type                   | Description 
------------             | -------------          | ------------
 result.status           | String                 | A pass or fail value. 
 result.failure_details  | String (Optional)      | Details about the failure

 
 
 **Example Create result: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        
        
        
         {
                "status" : "pass",
                "failure_details": ""
                
         }


        
       
**Response:**


 This table shows the body parameters for the response:
 
| Name                      | Type                       | Description                                                      |
|------------               | -------------              | ------------                                                     |  
| result.id                 | Uuid                       | The ID of the result                                             |
| result.status             | String                     | The status of the result                                         |
| result.created_at         | Datetime                   | Time the result was created                                      |
| result.failure_details    | String                     | Details about the failure                                        |
                                                        



 **Example Create result: JSON response**

        Status Code: 201 Created
        Content-Type: application/json
    
        
       {
              "created_at": "2016-09-02 17:05:42.084721",
              "failure_details": "",
              "id": 1,
              "status": "pass"
       }
       
       
       
       
       
       
## Retrieve list of Results


GET /projects/{project_id}/canary/{canary_id}/results

This operation retrieves a list of all the results that belongs to a canary. The project ID, canary ID is required for this request.
It is possible to get limited number of results or interval range of results, if either of these parameters are specified. To get limited 
number of results, specify using the "limit" parameter and to get interval range of results, specify using the "interval" parameter.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name          | Description      |
|------------  | ------------- | ---------------- |
| 200          | Success       | Request succeeded|
| 405          | Bad Method    | Bad Method       |
 
 
**Request:**
 
 This operation does not accept a request body
 
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The Unique ID of the project|
|{canary_id}           | Uuid          | The unique ID of the canary |
 
 
 **Example Retrieves list of results: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        


**Response:**


This table shows the body parameters for the response:
 
  
| Name                      | Type                       | Description                                                      |
|------------               | -------------              | ------------                                                     |  
| result.id                 | Uuid                       | The ID of the result                                             |
| result.status             | String                     | The status of the result                                         |
| result.created_at         | Datetime                   | Time the result was created                                      |
| result.failure_details    | String                     | Details about the failure                                        |

                                 
                     
                                 
                                 
 **Example Retrieves list of results: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       {
           "results" : [
                    
             {
                  "created_at": "2016-09-02 17:05:42.084721",
                  "failure_details": "",
                  "id": 1,
                  "status": "pass"
             },
             
             {
              "created_at": "2016-09-02 17:05:42.084721",
              "failure_details": "",
              "id": 2,
              "status": "fail"
       
        
        
    
           ]

       }



        
## Retrieve a Result




GET /projects/{project_id}/canary/{canary_id}/results/{result_id}

This operation retrieves a result. The Id of the project that owns the canary, the ID of the canary and the ID of the result is required.
The request and response data format is json.


This table shows the possible response codes for this operation:

|Response Code | Name          | Description       |
|------------  | ------------- | ----------------  |
| 200          | Success       | Request succeeded |
| 404          | Not found     | Resource not found| 
| 405          | Bad Method    | Bad Method        |
 
 
**Request:**

 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description           |
| ------------         | ------------- | ------------          |
|{project_id}          | Uuid          | The  ID of the project|
|{canary_id}           | Uuid          | The  ID of the canary |
|{result_id}           | Uuid          | The  ID of the result |
 
 
This operation does not accept a request body
 
 
 
 **Example Retrieve a result: JSON request**
       
        Content-Type: application/json
        Accept: application/json
        


**Response:**


This table shows the body parameters for the response:
  
  
| Name                      | Type                       | Description                                                      |
|------------               | -------------              | ------------                                                     |  
| result.id                 | Uuid                       | The ID of the result                                             |
| result.status             | String                     | The status of the result                                         |
| result.created_at         | Datetime                   | Time the result was created                                      |
| result.failure_details    | String                     | Details about the failure                                        |



 **Example Retrieve a result: JSON response**

        Status Code: 200 OK
        Content-Type: application/json



       {
                  "created_at": "2016-09-02 17:05:42.084721",
                  "failure_details": "",
                  "id": 1,
                  "status": "pass"
       }






## Update a Result




PUT /projects/{project_id}/canary/{canary_id}/results/{result_id}

This operation updates one or more editable attributes of a result. You can update the status and failure_details attributes in a single request.
The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name          | Description       |
|------------  | ------------- | ----------------  |
| 200          | Success       | Request succeeded |
| 404          | Not Found     | Resource Not found|
| 405          | Bad Method    | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|
|{canary_id}           | Uuid          | The ID of the canary |
|{result_id}           | Uuid          | The ID of the result |


 
 This table shows the body parameters for the request:
 
 Name                    | Type                   | Description 
------------             | -------------          | ------------
 result.status           | String                 | A pass or fail value. 
 result.failure_details  | String (Optional)      | Details about the failure



 
 

 **Example update a result: JSON request**
       
        Content-Type: application/json
        Accept: application/json
       
       
        {
              "status" : "fail"
        }
        


**Response:**

 This table shows the body parameters for the response:

 
| Name                      | Type                       | Description                                                      |
|------------               | -------------              | ------------                                                     |  
| result.id                 | Uuid                       | The ID of the result                                             |
| result.status             | String                     | The status of the result                                         |
| result.created_at         | Datetime                   | Time the result was created                                      |
| result.failure_details    | String                     | Details about the failure                                        |
                                                        



 **Example update a result: JSON response**

        Status Code: 200 OK
        Content-Type: application/json


       
       {
              "created_at": "2016-09-02 17:05:42.084721",
              "failure_details": "",
              "id": 1,
              "status": "fail"
              
       }





## Delete a Result



DELETE /projects/{project_id}/canary/{canary_id}/results/{result_id}

This operation deletes a result. The request and response data format is json.

This table shows the possible response codes for this operation:

|Response Code | Name                   | Description       |
|------------  | -------------          | ----------------  |
| 204          | Delete successful      | Request succeeded |
| 404          | Not Found              | Resource not found|
| 405          | Bad Method             | Bad Method        |
 
 
**Request:**
  
 This table shows the URI parameters for the request:
 
| Name                 | Type          | Description                 |
| ------------         | ------------- | ------------                |
|{project_id}          | Uuid          | The ID of the project|
|{canary_id}           | Uuid          | The ID of the canary |
|{result_id}           | Uuid          | The ID of the result |


This operation does not accept a request body


 **Example delete result: JSON request**
       
        Content-Type: application/json
        Accept: application/json
       

**Response:**


 **Example delete result: JSON response**

        Status Code: 204 No Content
        Content-Type: application/json
        

        
        

