import os
import subprocess

directory =input("Which type of file would you like to clean ? Please enter \'IPMA\' or \'ARTICLES\'. \n")+'/INPUTS/'
p1 = subprocess.Popen(["ls", directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(output, err) = p1.communicate()
filenames = []
for i in output.decode('utf-8').split('\n'):
    print(i)
    if (i!=i.replace(' ','_')):
        os.system("mv {}{} {}{}".format(directory, i.replace(' ','\ '), directory, i.replace(' ','_')))
