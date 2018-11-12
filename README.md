# CWL4ReANA

Script's purpose is to to create "skeleton"-cwl files for ReANA (which need to be a adjusted a bit after creation, for example add execution command for each step). The files are

* input.yml
* workflow.cwl
* Appopriate cwl files for each step of the worklfow

The input parameters are

* name of the steps as the string `__name`, steps are separated with a comma
* your inputs file as the string `__in`, separate input files for different workflows with a comma, if input is other type than "File" documment it between two semicolons like `<name>:<type>:`
* output as the string `__out`, separate for different workflows with a comma
* your base command, i.e. `/bin/sh` as the string `__baseCo`

Fill in the input parameters at the beginning of the file `create_workflow.py`
