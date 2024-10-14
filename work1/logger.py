import csv
import datetime

class logger:
    def __init__(self, log_file, user):
        self.log_file = log_file
        self.user = user
    
    def createaction(self, action):
        with open(self.log_file, mode="a", newline='') as log_file:
            log = csv.writer(log_file)
            log.writerow([datetime.datetime.now(), self.user, action])