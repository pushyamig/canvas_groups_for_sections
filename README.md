# Canvas Groups by Section:

## Description:
 
To better support Instructors of Large Courses in Canvas,  given a CourseId we should be able create groups in Canvas based on their course sections. This will allow them to: 

1. Share select resources with a section 
2. Discussions available to specific section 
3. Content Pages with a specific section 
4. Conference with a specific section 

This utility is written in python and takes `:course_id`, `:group_category_name` from the property file and creates a group category with the name provided in the property file. We will get all the sections and users
in the course and create one group for each section and add all the users in each section to the corresponding group. The group name will be identical to the section name
 

### Running the script without OpenShift

1. Python version > = 2.7.10 is required.
2. Install pip from https://pip.pypa.io/en/latest/installing/#install-pip to download some of the python module that are outside of standard python library.
3. To install the required modules for the utility do `pip install -r requirements.txt` 
    * To install modules to a user specific directory then do `pip install --user -r requirements.txt` and also set the environment variable as `PYTHONUSERBASE=/path/to/download/modules`.
    * To download modules to default users home directory as part of Python system path just do `pip install --user -r requirements.txt`. 
4. To run outside of OpenShift set the variables in `config.yaml` and `security.yaml` as show in the template under `config/config.yaml`, `config/security.yaml` and could be placed out side of source code.
5. Logging configurations are in `logging.yaml` the file can be present out side of the source code. The logs can be logged to console or to file. Use the template provided in the `config/logging.yaml` and add
    appropriate path to log file. The log get appended to `log/cgs.log` by default. 
#### Run Directions 

1. The `run.sh` is used for running the utility and is checked in to the source code. A default configuration is provided to get going once your are set up. You can run this utility as  `./run.sh`
2. The process may take long time for many sections in a course so it is good idea to run it in the background so that it continues after logging out from a machine. So use below while running on Linux servers.

    `nohup ./run.sh > /path-to-file/logFile.log &` 

### Running the script in OpenShift Locally

1. Download the [OpenShift CDK](http://developers.redhat.com/products/cdk/get-started/#tab-macLinux) follow along the CDK installation guidelines. 
   Also need to register with the RedHat's developer network.
2. Once the vagrant is up and running log in to the local OpenShift `https://10.1.2.2:8443/console/` and login as user : openshift-dev with password: devel. This is already configured user.
3. Install the OpenShift CLI, more info can be found from https://10.1.2.2:8443/console/about  or can be easily be downloaded from [here](https://oriole.dsc.umich.edu/openshift/) and put executable in your path.
4. To interact with the OpenShift instance from command line you need to login from command line. Go to https://10.1.2.2:8443/console/about for details.
5. Once logged in from command line you can create new build as `oc new-build --name=CGS-Test https://github.com/tl-its-umich-edu/canvas_groups_for_sections`. This will create the new build under the OS default sample project.
6. Go to the build `CGS-Test`(created from above) from the web instance edit the build configuration and set the image configuration to `Build From: Docker Image Link` and set it to `docker.io/ubuntu:16.04` and start the build.
   This build will download all the dependencies that is needed as mentioned in the `Dockerfile` and create a Docker image.
7. Once the build is successful, then in OS Web Console Go to Browse -> ImageStreams get the Docker image name for the build. For example `177.80.423.633:5000/sample-project/CGS-Test`
8. Projects secure properties are placed in Openshift. The sample template for it is `secrets.yaml`. The filename can be anything as you wish. 
   The `data` values in the file must be Base64 encoded. OS will decode it before the application uses. [More info](http://kubernetes.io/docs/user-guide/secrets/walkthrough/)  
    * `oc create -f secrets.yaml` will put the properties in OS. 
    * `oc replace -f secrets.yaml` if any modification to properties
    * `oc delete -f secrets.yaml` to delete properties.
9. From the GitHub repo get the `pod-batch.yaml` place the docker image name from step 7 in the `image` attribute`, 
   add appropriate for the values for the course id and category name and point to the correct secrets value. [More info](http://kubernetes.io/docs/user-guide/pods/multi-container/)
    * run the script as `oc create -f pod-batch.yaml`. This will be create a Pod say 'Pod1'as specified in the `pod-batch.yaml` file.
    * `oc logs -f pod/pod1` to tail the logs for `pod1`
    * `oc log pod1` to look at the logs when pod done running
    
    




