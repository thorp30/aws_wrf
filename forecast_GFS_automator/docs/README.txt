To get the forecast to run through a cronjob, an edited version of the ~/.bashrc (~/.bashrc_conda) has been created to activate the (base) environment. This is required because using a crontab is considered non interactive running, thus ~/.bashrc is not sourced. Therefore we have to force the reading of our edited script. Steps taken from here: 

https://stackoverflow.com/questions/36365801/run-a-crontab-job-using-an-anaconda-env
