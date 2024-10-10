### Description:

Сервис создан в рамкая обучения ЯП. Сервис django_app основан на Django

### How to use:

#### Clone the repo:

    git clone git@github.com:BloodFan/new_admin_panel_sprint_2.git
    

#### Before running add your superuser email/password/username in .env file

    .\new_admin_panel_sprint_2\docker_compose\simple_project\docker\dev\env\.env
    or
    .\new_admin_panel_sprint_2\docker_compose\simple_project\docker\prod\env\.env

    SUPERUSER_EMAIL=example@email.com
    SUPERUSER_PASSWORD=secretp@ssword
    SUPERUSER_USERNAME=example@test.com 


#### run docker-compose.yml for development using:

    docker compose up --build

##### Server will bind 8000 port. You can get access to server by browser [http://localhost:8000](http://localhost:8000)

##### This project implements API documentation using Swagger and Django Spectacular. [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

