# Canvas Groups by Section:

## Description:
 
To better support Instructors of Large Courses in Canvas,  given a CourseId we should be able create groups in Canvas based on their course sections. This will allow them to: 

1. Share select resources with a section 
2. Discussions available to specific section 
3. Content Pages with a specific section 
4. Conference with a specific section 

This utility is written in python and takes `:course_id`, `:group_category_name` from the property file and creates a group category with the name provided in the property file. We will get all the sections and users
in the course and create one group for each section and add all the users in each section to the corresponding group. The group name will be identical to the section name
 
## Requirements 

1. Python version > = 2.7.10 is required.
2. Install pip from https://pip.pypa.io/en/latest/installing/#install-pip to download some of the python module that are outside of standard python library.
3. To install the required modules for the utility do `pip install -r requirements.txt` 
    * To install modules to a user specific directory then do `pip install --user -r requirements.txt` and also set the environment variable as `PYTHONUSERBASE=/path/to/download/modules`.
    * To download modules to default users home directory as part of Python system path just do `pip install --user -r requirements.txt`. 
4. Add appropriate properties to the `config.yaml` as show in the template under `config/config.yaml` and could be placed out side of source code.
5. Logging configurations are in `logging.yaml` the file can be present out side of the source code. The logs can be logged to console or to file. Use the template provided in the `config/logging.yaml` and add
    appropriate path to log file. The log get appended to `log/cgs.log` by default. Recommended keep log file out side of the utility
## Run Directions 

1. The `run.sh` is used for running the utility and is checked in to the source code. A default configuration is provided to get going once your are set up. You can run this utility as  `./run.sh`
2. The process may take long time for many sections in a course so it is good idea to run it in the background so that it continues after logging out from a machine. So use below while running on Linux servers.

    `nohup ./run.sh > /path-to-file/logFile.log &` 


