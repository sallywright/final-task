## Get started.

1. Create .env file in the /recipes directory and insert database connection parameters. (Use the .env.example for guidance)
2. Create venv with the `python3 -m venv venv` command.
3. Activate virtual envionment with the `source venv/bin/activate` command.
4. Install the necessary packages with the following command: `pip install -r requirements.txt`
5. Run `python manage.py tailwind install` and `python manage.py tailwind start` commands to generate static files.
6. You might need to apply/create migrations, therefore run the following commands:
   `python manage.py makemigrations`
   `python manage.py migrate`

7. Run the django application with `python manage.py runserver`
8. Head to the `http://127.0.0.1:8000/register/` and register into the website.
9. Use the website to create notes, categories.
10. Use the `http://127.0.0.1:8000/note/list` to view your personal (user-specific) notes.
11. Use the search bar to filter notes by their title.
12. You can manipulate any note data (except id). Also, delete and create notes.
13. Use the `http://127.0.0.1:8000/category/list` to view all categories. 
14. You can manipulate any category data (except id). Also, delete and create categories.
15. You can freely re-assign any note from category to category, or even use None, if you wish not to assign a note to a category.

## Notes.

1. Tailwind css framework is being used for the front-end styling if any changes need to be done, run the `python manage.py tailwind start` command.
2. All of the CSS is being stored in the `/theme/static/` directory.
3. Core is the main Django project directory, utils is the app, that is being used to store models, migrations ant etc.
4. The website does not have a functioning admin website.
5. MySQL server has to be installed on the computer.
6. NodeJS has to be installed on the computer.
7. notes database has to be created.

## Things that could be improved.

1. Category filter was not implemented.
2. Some of the Django templates could have been re-used for example: sidenav.
3. There could be more error handling, error pages could be created.
5. Could have added a Logout button. Although, user logout is available in the `http://127.0.0.1:8000/logout/` endpoint.
