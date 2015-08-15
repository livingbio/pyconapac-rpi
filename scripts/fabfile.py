from fabric.api import run, env,local, sudo,cd, parallel
from fabric.contrib import files
from fabric.operations import reboot
import re

## get all pi ips
def get_ips():
    result = local('nmap -sV -p 22 192.168.2.0/24', capture=True)
    ips = result.replace("\n", "@").split('Nmap scan report for ')
    ips = [ip.split('@')[0] for ip in ips if 'Debian 4+deb7u2' in ip]
    print ips
    try:
        ips.remove('192.168.2.80')
    except:
        pass
    return ips


env.user = "pi"
env.password = "raspberry"
env.hosts = list(set(get_ips() + get_ips()))


def update_cron():
    # override the crontab
    sudo('rm -rf /var/spool/cron/crontabs/*')
    sudo('echo "%s" > /var/spool/cron/crontabs/root' % open('./crontab').read())
    sudo('chmod 600 /var/spool/cron/crontabs/root')

    print '====================================================================='
    sudo("cat /var/spool/cron/crontabs/root")
    print '====================================================================='

def install_requirements():
    with open('./install') as ifile:
        for iline in ifile:
            sudo(iline)

@parallel
def setup():
    install_requirements()
    update_cron()
    reboot()
    print 'end'


