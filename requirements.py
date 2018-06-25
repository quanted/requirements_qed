import os
import sys
import json
import subprocess
from subprocess import PIPE

def run_requirements(env):
    with open("requirements.txt") as f_requirements:
        lines = []
        for line in f_requirements:
            lines.append(line)


    with open("requirements.log","w") as f_log:

        cmd = "conda env list --json"
        result = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
        (outp, err) = result.communicate()
        soutp = outp.decode('utf8')
        serr = err.decode('utf8')
        data = json.loads(soutp)
        pip_path = ""
        envs = data["envs"]
        for env_path in envs:
            if env in env_path.lower():
                pip_path = env_path
                pip_path = os.path.join(pip_path, "scripts", "pip")
                break


        #conda install pip in the env
        cmd_conda = "conda install -y --json -n {} {}"
        cmd = cmd_conda.format(env, "pip")
        if execute_cmd(cmd, f_log) == False:
            log_msg(f_log, "Unable to install pip in "+ env)
            log_msg(f_log, "Exiting")
            return


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
            cmd = cmd_pip.format(pip_path, line)            
            if execute_cmd(cmd, f_log) == True:
                continue




            #log_msg(f_log, "Attempting: conda install -y --json -n " + env + " " + line)
            #f_log.write("Attempting conda install: " + line)
            #f_log.flush()
            #result = subprocess.Popen("conda install -y --json -n " + env + " " + line, stdout=PIPE, stderr=PIPE)
            #(outp, err) = result.communicate()
            #outp = result.stdout.read()
            #soutp = outp.decode('utf8')
            #serr = err.decode('utf8') 
            #print(soutp)
            #if "error" in soutp.lower() or "fail" in soutp.lower():
            #    log_msg(f_log, "Failure: " +  "conda install -y --json -n " + env + " " + line)
            #    log_msg(f_log, "Attempting: conda install -y --json -c conda-forge -n " + env + " " + line)
            #    result = subprocess.Popen("conda install -y -c conda-forge -n " + env + " " + line, stdout=PIPE, stderr=PIPE)
            #    (outp, err) = result.communicate()
            #    soutp = outp.decode('utf8')
            #    serr = err.decode('utf8') 
            #    print(soutp)
            #    if "error" in soutp.lower() or "fail" in soutp.lower():
            #        log_msg(f_log, "Failure: conda install -y --json -c conda-forge -n " + env + " " + line) 
            #        result.terminate()  
            #        log_msg(f_log, "Attempting: pip install " + line)                
            #        result = subprocess.Popen("pip install "+ line, stdout=PIPE, stderr=PIPE)
            #        (outp, err) = result.communicate()
            #        soutp = outp.decode('utf8')
            #        serr = err.decode('utf8') 
            #        print(soutp)
            #        if "error" in soutp.lower() or "fail" in soutp.lower():
            #            log_msg(f_log, "Failure:  pip install " + line)
            #            result.terminate()           
            #        else:
            #            log_msg(f_log, "Success:  pip install " + line)
            #    else:
            #        log_msg(f_log, "Success: conda install -c conda-forge " + line)              
            #else:
            #    log_msg(f_log, "Success: " +  "conda install -y --json " + line)


#Execute command and return true for success and false for failure
def execute_cmd(cmd, f):
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
    run_requirements("py36")