## Requirements
1. [Git](https://git-scm.com/)
2. [Python3.6](https://www.python.org/) or newer.

## Installation and running
1. Clone repository `git clone git@github.com:gradam/static_code_analyzer_web.git`
2. Move to the cloned directory `cd static_code_analyzer`
3. Install required packages `pip install -r requirements.txt`
4. Run `python src/manage.py runserver`
5. Open new terminal in the same location
6. Run `python src/manage.py process_tasks --sleep 1`

## Adding new analyzers
1. Go to file src/utils/analyzers.py
2. In class `Analyzers` add your analyzer name (further referred to as _MY_CUSTOM_ANALYZER_) to `ALL` and `CHOICES` eg:
``` python
ALL = ('flake8', 'pylint', 'MY_CUSTOM_ANALYZER')
CHOICES = (('flake8', 'flake8'), ('pylint', 'pylint'), ('MY_CUSTOM_ANALYZER','MY_CUSTOM_ANALYZER'))
```
3. In the same class create method with name `use_MY_CUSTOM_ANALYZER`. Two arguments will be passed to this function:
    * `files` - List of paths to files to analyze eg: 
    `['/tmp/tt23123/my-project/utils/utils.py', '/tmp/tt23123/my-project/another.py']`
    * `ignore` - Currently is always an empty list.
    
    This function should return data in the following format:
    ```
    [
        [{
            'file': relative_file_path,  # Eg. utils/utils.py
            'position': position_information  # Eg. 58:12 or line 58 character 12
            'massage': massage_from_analyzer  # Eg. E501 line too long (89 > 79 characters)
         }, ...],
        additional_massage  # Eg. Your code has been rated at 2/10. If none pass an empty string. 
    ]
    ```
4. That's it. You are ready to go.

## Running tests
Couple of very simple tests were created just to ensure that views are loading properly.

To run tests, run this command:
`pytest src/`


## Known issues
1. Not perfect responsive design. On smaller screens texts are a bit small.
2. Because of nature of this project it is using sqlite as a database which can't support a high level of concurrency. 
Which leads to `django.db.utils.OperationalError: database is locked` if you try to run more then 1 project simultaneously.
It can be fixed by switching to another database backend (eg. Postgresql or MySql) or switching from `django-background-tasks` to `celery` with eg. Redis backend.
I've went with django-background-tasks and sqlite because I wanted for this project to depend only on pip packages and GIT.
3. This is not at all production ready
    * Debug is set to True
    * Email account is not set up. (It just prints out the content to console atm.)
    * CORS are not properly set up
    * And much more
4. Number of tests is way to low. Currently they only checks if web pages are loading properly.
5. There is no authentication system so everyone can add/delete projects, subscribers, etc.
6. Page requires manual refresh to see if analysis had finished running.
7. Currently there is no easy way of configurating tools used to analyse the code (eg. pylint)
8. Does not check the correctness of the urls.
9. Lack of proper error handling.
