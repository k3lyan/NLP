import sys
import subprocess 

# GET THE TITLES OF THE MAILS HAVING METADATA (='metamails') FROM THE HEADERS TITLE 
with subprocess.Popen(['ls', '../HEADERS/header'], stdout=subprocess.PIPE) as proc:
    metamail_list = proc.stdout.read().decode('utf-8').split('\n')[:-1]

# CREATE THE DIRECTORY WHERE WILL BE STOCKED THE METAMAILS
subprocess.Popen(['mkdir', 'meta_mails'])

# COPY THE METAMAILS TO THIS DIRECTORY
for index, title in enumerate(metamail_list):
    subprocess.Popen(['cp', '../MAILS/emailUnique/{}'.format(title), './meta_mails/{}'.format(title)])

# STOCK THE ABSOLUTE PATHS OF THE METAMAILS IN A FILE
subprocess.Popen(['./metapaths.sh'])


