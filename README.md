# [TengiNews Clone](https://tengri-news-clone.onrender.com/)


## Introduction
TengiNews Clone is a Django-based web application that replicates a news aggregator platform. It allows users to view news articles, create posts, subscribe to newsletters, and receive email notifications. The project utilizes `Django`, `PostgreSQL`, and `AWS` for its functionalities.

Live Demo [here](https://tengri-news-clone.onrender.com/)


## Main Features

#### Architecture Design:    
Design Pattern: Model-View-Template (MVT)
> Analyzed functional and non-functional requirements, defining core functions like viewing news, creating/editing posts, and managing subscriptions.
Designed database models (e.g `NewsPost`, `EmailConfirmation`) and logic for user-subscription management.

#### Technology and architecture choices:

>Used `Django` for web development due to its comprehensive toolset, including ORM, authentication, form handling, and subscription management.
Selected `PostgreSQL` for its reliability, performance, and extensibility.
Preferred html,css and bootstrap because it allows you to quickly and efficiently create a front-end and is also well integrated with Django

#### Development of functionality:    

> Developed Django models (`NewsPost`, `EmailConfirmation`, `Category`, `User`, `Subscription`) with defined fields, relationships, and methods.
Implemented custom forms (`PostForm`, `UserRegistrationForm`, `UserLoginForm`, `SubscriptionForm`) for data input and validation.
Utilized Django `CBF Generic Views` to manage news display and post creation.

#### Integration with external services
> Integrated `AWS S3` for uploading news-related images and files.
Used `SMTP` for email notifications to subscribers about new posts in their categories.



#### Unique approaches    
>Using Django Signals for subscriber notifications
Automatically send notifications to subscribers when a newpost is created using `Django Signals(post_save)`.

>Integration with `AWS S3` for storing media files
Store images and media files in AWS S3 for efficient media content management and retrieving media content by image_link(object url)

> Using Django Generic Views and forms for data management
Using `Django Generic Views` and creating custom forms to easily manage application data.

> Scheduling Tasks with APScheduler
Automation of repetitive tasks, for example, parsing of news from the site `tengrinews.kz from 1 to 8 pages every 5 minutes and thus constantly dynamically provide the latest news`, the use of `APScheduler` for regular data updates.


> Using `SMTP to send email notifications`
Send email notifications to subscribers about new posts using SMTP to actively inform users


#### Compromises and Challenges

1. `Simplified User Interface`:
    Challenge: Balancing design simplicity to prioritize essential features over aesthetics.
    Compromise: Opted for minimalist UI design to expedite development and focus on core functionalities.

2. `Session Based Authentication`:
    Challenge: Implementing authentication using Django's session-based system.
    Compromise: Chose session-based authentication for quick setup, acknowledging limitations compared to token-based methods.

3.  `Scheduler Jobs in Single Process`:
    Challenge: Managing scheduled tasks within one process without distributed queues.
    Compromise: Used Django's built-in task scheduling in one process to minimize complexity, despite scalability limitations.

4. `Storing Parsed News Data in .json Files`:
    Challenge: Using .json files instead of a database for parsed news data.
    Compromise: Chose .json storage for simplicity, despite scalability and queryability drawbacks compared to database


### Levels I've passed/done
**Level 1** - made the list of posts displayed, as well as the ability to click on a selected post and see the post details.

**Level 2** - made pagination on Our News and Parsed News pages.
I implemented search by title, filtering by categories and sorting by creating date.
 
**Level 3** - wrote a parser using request and bs4 that parses the first 8 pages of tengrinews.kz to parse the latest news.
I set up a cron job using django-apsheduler that runs the parser every 5 minutes and thus posts dynamically new news every 5 minutes every day.

**Bonus Task** - The Tengri News Clone application has been deployed and is now hosted on Render.com, utilizing a remote PostgreSQL database for data storage.

The live application can be accessed at https://tengri-news-clone.onrender.com/


### Tech Stack

> Backend 
> - Language: Python3.10
> - Framework: Django
> - Database: PostgreSQL
> - Email Service: Gmail SMTP
> - Task Scheduling: Django APScheduler
> - AWS Integration: AWS S3 for file storage
> - Parser: requests, Beautiful Soup


> Frontend
> - HTML/CSS: Bootstrap, Jinja templates


## Development Environment 

#### Installation (Linux)


```bash
git clone git@github.com:TemirlannK2004/Tengri-News-Clone.git

cd Tengri-News-Clone

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt 
```

#### Configuration
Before applying migrations, creating superusers or running the server, you must create env variables file.

For linux
```sh
touch .env 
```

#.env
```
SECRET_KEY=_some_secret_key
DB_URL_PROD=_remote_db_link 

#for local development use this!!!,not DB_URL_PROD
DB_NAME=_your_db_name
DB_USER=_your_db_user
DB_PASSWORD=_your_db_password
DB_HOST=_your_db_host
DB_PORT=_your_db_port

AWS_ACCESS_KEY=_your_s3bucket_access_key
AWS_SECRET_KEY=_your_s3bucket_secret_key
AWS_BUCKET_NAME=_your_s3bucket_name
AWS_REGION=_s3_bucket_region

EMAIL_HOST =_smtp-host
EMAIL_PORT =_smtp-port
EMAIL_USE_TLS =_True
EMAIL_HOST_USER =_host-user
EMAIL_HOST_PASSWORD =_host-password
```
Applying Migrations and Creating Superuser:
Once the database is configured, apply Django migrations to create the necessary database tables and create superuser:

```sh
python manage.py migrate
python manage.py createsuperuser
```
After setting up the database and applying migrations, start the Django development server:
```sh
python manage.py runserver
```
This command will run the server at http://127.0.0.1:8000/

Navigate to http://127.0.0.1:8000/admin/  for Accessing the Admin Interface




### Project file structure
```
├── manage.py
├── README.md
├── requirements.txt
├── news_service
│   ├── admin.py
│   ├── apps.py
│   ├── aws.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── parser.py
│   ├── scheduler.py
│   ├── templatetags
│   ├── urls.py
│   ├── utils
│   └── views.py
|
├── staticfiles(django-admin)
|
├── templates
│   ├── html
│   │   ├── base
│   │   │   └── base.html
│   │   ├── email
│   │   │   ├── confirmation_email.html
│   │   │   ├── notification_email.html
│   │   │   └── success_sign_up.html
│   │   ├── news
│   │   │   ├── create_post.html
│   │   │   ├── news_list.html
│   │   │   ├── parsed_news_details.html
│   │   │   ├── parsed_news.html
│   │   │   └── post_detail.html
│   │   └── users
│   │       ├── login.html
│   │       ├── register.html
│   │       └── subscriptions.html
|
├── tengrinews(core)
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│   
└── user_service
    ├── admin.py
    ├── apps.py
    ├── email.py
    ├── forms.py
    ├── __init__.py
    ├── migrations
    ├── models.py
    ├── signals.py
    ├── urls.py
    └──views.py

```

### Support

If you have some troubles with project setup, you can contact with me 

Email: *temirlan.kazhigerey@gmail.com* <br>
Telegram: *https://t.me/qwqwwwqwqw*

