# Django Project

## Setup Instructions

### 1. Create `.env` File

Create a `.env` file in the root of the project and add the following content:


SECRET_KEY=django-insecure-yu7huy0+jmlk9ele73de$k9et5#s$819p-$aoo$4r936a)js$i
DEBUG=True
SERVER='dev'
ALLOWED_HOSTS='*'
POSTGRES_ENGINE=postgresql
POSTGRES_USER=db_user
POSTGRES_PASSWORD=postgres_db
POSTGRES_DB=postgres_db
PG_HOST=localhost
PG_PORT=5432
DOMAIN=localhost
SIGNING_KEY=jnBSC5cSi-ieb3pL0kT4gfjSxr67msD5ecO1cpRwz5b3Ug_SbElc46fbMOAQ5G0l17qMHLfX-pOCvdOFKrCxyA



### 2. Update Database Credentials
Modify the .env file with your PostgreSQL details:

POSTGRES_USER

POSTGRES_PASSWORD

POSTGRES_DB

PG_HOST

PG_PORT

### 3. Install Dependencies

pip install -r requirements.txt


#### 4. Apply Migrations

python manage.py makemigrations
python manage.py migrate


### 5. Run the Server

python manage.py runserver


### 6. Access the Application

http://127.0.0.1:8000/

