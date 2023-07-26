
## Project Overview
The Django-based Hackernews application has been designed to regularly collect information from the Hackernews API asynchronously using Celery. Additionally, the application includes pages that allow users to view the gathered data while also providing filtering options for more efficient data retrieval.

## Demo
![Demo 1](demo/hackernewsapp_home.png)
![Demo 2](demo/hackernewapp_result.png)
![Demo 3](demo/hackernewsapp_details.png)



## Getting Started

### Requirements

**Python3.10 and above**
To install python, please follow the documentation on the official site.

**Redis**

Install Redis

### Setup
**Clone the repository**
```
git clone <repository-url>
cd your-react-app
npm install
npm start
```

**Setup virtual environment**

Set up virtual enviroment and install requirements using python-venv.
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**Environment Variables**
Create a `.env` file to store the enviroment variables. They are listed below;
```
$ touch .env
$ echo SECRET_KEY
$ echo DEBUG
```
| Env Var | Description |
|---------|-------------|
|`SECRET_KEY`| Generate a secret key for your application with Djecrety[https://djecrety.ir/]|
| `DEBUG` |Set local development, set to `TRUE`. For production, set to `FALSE`|

**Migrate Database**

Because the application uses sqlite, you can run the following command and the `db.sqlite` file will be create automatically.

```python manage.py migrate```

## Running The application

Start the Redis Server:

```redis-server```

Start the Celery Server:

```celery -A hackernews worker -l info```

Run Django App

```python manage.py runserver```

### Usage
By default, there is no data on the databas, as a result, pages will return empty values. You can run the tasks found in `news/tasks.py` to populate historic data.
```
$ python manage.py shell
$ from news import tasks
$ tasks.get_history.delay() -> sends to celery worker to get previous data (up to 500 $ previous posts)
$ tasks.getlatest.delay()
```
At any point, you can run these functions to get the most recent data from hacker news api.


## Features
| Feature | Description |
|------------|------------|
| Hacker News Display | Views recent posts from Hacker News |
| Add Custom News | Integrate custom news info independent of hacker news |
| Filter | Perform Filter on display pages |

## Technologies Used
List the key technologies, libraries, and frameworks used in your project.
* Django
* Celery
* HTML, CSS & Vanilla Javascript


**Contributing**
* Implement Celery Auto Scheduler to run news tasks functions perodically.