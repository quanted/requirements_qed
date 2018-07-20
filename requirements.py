import os
import sys
import json
import subprocess
from subprocess import PIPE

#Usage
#Create a new conda environment or activate an existing one
#conda create --name myenv
#conda activate myenv
#run this script in the folder with the requirements.txt file


#set this variable to reflect your conda install
conda_path = "C:\\Users\\KWOLFE\\AppData\\Local\\Continuum\\anaconda3\\Scripts"

#set to environment you want to create
env = "qed"

def run_requirements(env):
    with open("requirements.txt") as f_requirements:
        lines = []
        for line in f_requirements:
            #string out comments
            loc = line.find("#")
            if loc > 1:
                line = line[0:loc].strip()
            lines.append(line)


    with open("requirements.log","w") as f_log:

        #Check to see if the environment exists
        #cmd = "conda env list --json"
        #cmd = os.path.join(conda_path, cmd)
        #result = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
        #(outp, err) = result.communicate()
        #soutp = outp.decode('utf8')
        #serr = err.decode('utf8')
        #print(serr)
        #data = json.loads(soutp)
        
        #If the environment exists, get the pip path
        #pip_path = ""
        #env_exists = False
        #envs = data["envs"]
        #for env_path in envs:
        #    if env in env_path.lower():
        #        pip_path = env_path
        #        env_exists = True
        #        pip_path = os.path.join(pip_path, "scripts", "pip")
        #        break

        #if env_exists == False:
        #    cmd = "conda create --name " + env
        #    execute_cmd(cmd, f_log)


        #conda install pip in the env
        #dont need to do this
        #cmd_conda = "conda install -y --json -n {} {}"
        #cmd = cmd_conda.format(env, "pip")
        #if execute_cmd(cmd, f_log) == False:
        #    log_msg(f_log, "Unable to install pip in "+ env)
        #    log_msg(f_log, "Exiting")
        #    return


        for line in lines:
            #try standard conda install first
            cmd_conda = "conda install -y --json -n {} {}"
            cmd = cmd_conda.format(env, line)
            if execute_cmd(cmd, f_log) == True:
                continue

            #try conda install from conda forge
            cmd_conda = "conda install -y --json -c conda-forge -n {} {}"
            cmd = cmd_conda.format(env, line)
            if execute_cmd(cmd, f_log) == True:
                continue

            #try pip install - make sure use pip from env            
            cmd_pip = "{} install {}"
            cmd = cmd_pip.format("pip,exe", line)            
            if execute_cmd(cmd, f_log) == True:
                continue


#Execute command and return true for success and false for failure
def execute_cmd(cmd, f):
    #cmd = os.path.join(conda_path, cmd)
    log_msg(f, "Attempting: " + cmd)
    result = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    (outp, err) = result.communicate()
    soutp = outp.decode('utf8')
    serr = err.decode('utf8') 
    if "error" in soutp.lower() or "fail" in soutp.lower():
        log_msg(f, "Failure: " + cmd)
        return False
    else:
        log_msg(f, "Success: " + cmd)
        return True



def log_msg(f, msg):
    f.write(msg)
    f.flush()
    print(msg)


if __name__ == "__main__":
    run_requirements(env)