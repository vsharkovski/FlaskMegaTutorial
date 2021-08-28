# My Microblog

A simple blog site written in Flask. The tutorial being followed was *The New And Improved Flask Mega-Tutorial* by Miguel Grinberg.

I have made small changes in some places.

## Setting up the project
1. Create a virtual environment at the project's base directory
2. Install the required dependencies with the command
`pip install -r requirements.txt`
3. Create an .env file (needed for site security, sending emails, and translating posts)

### .env files 
The application needs an `.env` file to configure things such as the database URI, email server, email address of the admin, and the Microsoft Translator API key.

Sample `.env` files:

```env
SECRET_KEY=a-really-long-and-unique-key-nobody-knows
MAIL_SERVER=localhost
MAIL_PORT=25
MS_TRANSLATOR_KEY=my-translator-api-key
```

```env
SECRET_KEY=a-really-long-and-unique-key-nobody-knows
MAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=my-gmail-account@gmail.com
MAIL_PASSWORD=my-gmail-password
MAIL_ADMIN_ADDRESS=my-gmail-account@gmail.com
MS_TRANSLATOR_KEY=my-translator-api-key
```

## Running the server
1. Activate the virtual environment
2. Use the command `flask run`
