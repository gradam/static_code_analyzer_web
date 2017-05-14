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
