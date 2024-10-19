# ARBA Travel Backend

This is the backend for the ARBA Travel application, a social media-like platform where users can create posts, comment on posts, and interact with other users.

## Features

- User authentication (register, login, logout)
- Create, read, update, and delete posts
- Create, read, update, and delete comments on posts
- Image upload for posts

## Technologies Used

- Django
- Django Rest Framework
- SQLite (for development)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/moe-lok/arba_travel_project.git
   cd arba-travel-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

## Running the Server

To run the development server:

```
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

## API Endpoints

- User Registration: `POST /api/register/`
- User Login: `POST /api/login/`
- User Logout: `POST /api/logout/`
- List/Create Posts: `GET/POST /api/posts/`
- Retrieve/Update/Delete Post: `GET/PUT/DELETE /api/posts/<id>/`
- List/Create Comments: `GET/POST /api/posts/<post_id>/comments/`
- Retrieve/Update/Delete Comment: `GET/PUT/DELETE /api/comments/<id>/`

## Deployment

This project is deployed on an AWS EC2 instance. url of hosted app: http://3.132.154.208/

## Frontend Repository

The frontend for this project can be found at: [ARBA Travel Frontend](https://github.com/moe-lok/arba-travel-frontend)

## Note

This project was developed as part of a technical assessment for ARBA Travel. Some features may be incomplete or require further refinement.
