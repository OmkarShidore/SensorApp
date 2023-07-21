# sensor

### Architecture Overview:
<img src="https://raw.githubusercontent.com/OmkarShidore/SensorApp/master/src/doc/sensor_app_architecture.jpg" alt="GitHub Logo" style="width: 800px;"/>


### Installation guide.
- Clone private repository 

```
git clone https://github.com/OmkarShidore/sensor.git
```

- Create virtual environment & install dependencies
```sh
cd path_to_repo
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

- Also create a debug launch config in VSCode, set the necessary env variables in it.
- run module src.routes to launch the FLask App.

### Quick links
| Description | Links |
| ------ | ------ |
| Postman API Collection | [Postman public workspace](https://www.postman.com/maintenance-pilot-26919508/workspace/sensor/overview)|
| User Sign Up | [Cognito sign up](https://sensordb.auth.ap-south-1.amazoncognito.com/signup?client_id=5ns6kjltmpiac9sgtqgiic42e7&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone&redirect_uri=https%3A%2F%2Fs1jpwfhil5.execute-api.ap-south-1.amazonaws.com%2F) |
| User Sign In| [Cognito sign in](https://sensordb.auth.ap-south-1.amazoncognito.com/login?client_id=5ns6kjltmpiac9sgtqgiic42e7&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone&redirect_uri=https%3A%2F%2Fs1jpwfhil5.execute-api.ap-south-1.amazonaws.com%2F)|