# healthcheck

To run

If a database is set up, run the manage.py file with,
DEV_DATABASE_URL='postgresql://DB_username:DB_password@localhost:DB_port/DB_name' "  where DB_name is the
name of the database.
For instance: DEV_DATABASE_URL='postgresql://user234:password@localhost:5432/canaryDB' python manage.py

If there is no database set up, currently it will default to using
"sqlite:///' + os.path.join(basedir, 'data-dev.sqlite)"


Routes syntax is: http://127.0.0.1:5000/api/"resource_name"

An example for a new project:

  {
                    "name" : "new",
                    "email": "test@rackspace.com",
                    "description": "A canary service that will monitor, keep track, and trend of",
                    "dependencies" : "projectX"	            
    }
    
    
An example to post a new canary:
               {
                    "name" : "canary1",
                    "description": "OnMetal canary, tweet tweet",
                    "data" : { 
                        "region" : "Hong Kong"
                    },
                    "criteria": {
                        "cr1": "pass all tests",
                        "short_trend" : "5 hours",
                        "long_trend" : "3 days"
                    }
                }