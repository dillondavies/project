import subprocess
import os
import json

class FSCrawlerWrapper():

    CRAWLER_JOB_DIR = 'C:\\Users\\Dillon Davies\\.fscrawler\\'
    CRAWLER_BAT = 'C:\\Users\\Dillon Davies\\Downloads\\fscrawler-2.4\\fscrawler-2.4\\bin'

    def create_job(name, url):

        job_dir = CRAWLER_JOB_DIR+name
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)
        
        with open("fs_job_template.json", "r") as jsonFile:
            data = json.load(jsonFile)

        # TODO: must ensure that name is a single token name that has not been utilised before
        data['name'] = name
        data['fs']['url'] = url

        with open(job_dir+"/_settings.json", "w") as jsonFile:
            json.dump(data, jsonFile)


    def run_job(name):

        # TODO: opening as shell is potential vulnerability if the name variable passed to it is not controlled

        # the --loop 1 argument sets the crawler to execute once, rather than monitoring
        p = subprocess.Popen([CRAWLER_BAT,name, '--loop', '1'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT); print('fscrawler finished')
        # returns stdout, stderr (byte stream)
        # stdout, stderr = p.communicate()
        return p.communicate()
