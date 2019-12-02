# Flask postgres api example


## API use
---

#### POST user
```
curl -X POST -F 'email=some@email.com' -F 'password=something' https://flask-pg-api.herokuapp.com/
```

#### GET form page from browser
```
curl -X GET https://flask-pg-api.herokuapp.com/
```

#### GET user from db
```
curl -X GET https://flask-pg-api.herokuapp.com/user/<user_id>
```

#### POST update user 
```
curl -X POST -F 'email=some@email.com' -F 'password=something' https://flask-pg-api.herokuapp.com/user/<user_id>
```
where ```<user_id>``` is f.e. 1



## Development
---
#### create python virtual environment to separate dev packages from system
```
python3 -m venv virtual_env
```

#### activate virtual environment
```
source virtual_env/bin/activate
```

#### install dependencies
```
pip install -r requirements.txt
```

#### Export flask env var:
```
export FLASK_APP=run.py
```

#### Run flask app
```
flask run
```
