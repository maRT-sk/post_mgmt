## post_mgmt

This is a RESTFul API Service written in Python and created in Django.

### Requirements and installation

- Python 3.10
- install requirements.txt

Create a virtual environment (.env does not have to be created) and install packages from requirements.txt.

```
pip install -r .\requirements.txt
```

Start the initial migration that creates the first version of the app's tables. Run the development server.

```
python manage.py migrate
python manage.py runserver
```

### Usage

| Method | Route                                            | Description              |
|--------|:-------------------------------------------------|:-------------------------|
| POST   | api/posts/?title=Lorem&body=Ipsum&id=1&user_id=1 | create a new post        | 
| GET    | api/posts/                                       | get all posts            | 
| GET    | api/posts/?user_id=1                             | get all posts by user_id |
| GET    | api/posts/?id=1                                  | get post by post id      |
| GET    | api/posts/1                                      | get post by post id      |
| PATCH  | api/posts/1?title=Lorem&body=Ipsum               | edit an existing post    |
| DELETE | api/posts/1                                      | delete a post by id      |
| DELETE | api/posts/?id=1                                  | delete a post by id      |








