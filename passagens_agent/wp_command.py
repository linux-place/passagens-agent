import os
import pwd
import subprocess
import sys


class WpCommand:

    def __init__(self,user_name):

        pw_record = pwd.getpwnam(user_name)
        self.user_name      = pw_record.pw_name
        self.user_home_dir  = pw_record.pw_dir
        self.user_uid       = pw_record.pw_uid
        self.user_gid       = pw_record.pw_gid
        self.env = os.environ.copy()
        self.env[ 'HOME'     ]  = self.user_home_dir
        self.env[ 'LOGNAME'  ]  = self.user_name
        self.env[ 'PWD'      ]  = self.user_home_dir
        self.env[ 'USER'     ]  = self.user_name

    def run(self,command):
        wp_cmd=["/usr/bin/wp"] + command.split(" ")
        process = subprocess.Popen(
            wp_cmd, preexec_fn=self.demote(self.user_uid, self.user_gid), cwd=self.user_home_dir, env=self.env
        )
        result = process.wait()
    #report_ids('finished ' + str(args))
    #print 'result', result


    def demote(self, user_uid, user_gid):
        def result():
            os.setgid(user_gid)
            os.setuid(user_uid)
        return result