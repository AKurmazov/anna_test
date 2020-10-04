# Task Manager

This project is a test assignment given by ANNA Financial Services


### Running Locally
The project uses Docker, so initially you have to build and run the image using docker-compose:
```
$ docker-compose up --build -d
```
Next, run the migrations by executing the following command:
```
$ docker-compose run web python manage.py migrate
```
Additionally, you can run tests a similar way:
```
$ docker-compose run web python manage.py test
```

### Authentication
The authentication is done via the Authorization header by providing a token. All mentioned body parameters are required
```
[POST] /api/accounts/register
[Body]  {
            username: <string>
            password: <string>
        }
[Comment] Creates a new user and returns the Authorization token


[POST] /api/account/login
[Body]  {
            username: <string>
            password: <string>
        }
[Comment] Authenticates an existing user and returns the Authorization token


[POST] /api/account/logout
[Headers] Authorization: Token <token>
[Comment] Terminates current session
```

### Task Manager 
The API offers endpoints for creating, retrieving, and updating tasks, and also for getting the history of changes of a task. A body parameter is required if not specified otherwise


```
[GET] /api/tasks/all
[Headers] Authorization: Token <token>
[Comment] Returns all current user's tasks


[POST] /api/tasks/create
[Body]  {
            name: <string>
            description: <string>
        }
[Headers] Authorization: Token <token>
[Comment] Creates a task with status 'New'


[GET] /api/tasks/<pk>
[Headers] Authorization: Token <token>
[Comment] Returns the task that has the provided primary key <pk>


[PUT] /api/tasks/<pk>
[Body]  {
            [optional] name: <string>                            
            [optional] description: <string>
            [optional] status: <New/Scheduled/In-Progress/Completed>
            [optional] scheduled_on: <date>
        }
[Headers] Authorization: Token <token>
[Comment] Updates the task that has the provided primapy key <pk>;
          At least one of the optional parameters should be provided;
          If status is changed to 'Scheduled' the very fist time,
          then the scheduled_on parameter should be provided
          
          
[GET] /api/tasks/<pk>/changes
[Headers] Authorization: Token <token>
[Comment] Returns the history of changes of the task that has the
          provided primary key <pk>
```









