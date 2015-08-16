from fabric.api import run, env,local, sudo,cd, parallel, put
from fabric.contrib import files
from fabric.operations import reboot
import re

## get all pi ips
def get_ips(subnet):
    result = local('nmap -sV -p 22 %s/24' % subnet, capture=True)
    ips = result.replace("\n", "@").split('Nmap scan report for ')
    ips = [ip.split('@')[0] for ip in ips if 'Debian 4+deb7u2' in ip]

    return ips

env.hosts = get_ips(env.subnet)
print 'scaned hosts', env.hosts
env.user = "pi"
env.password = "raspberry"

def update_cron():

    # override the crontab
    sudo('rm -rf /var/spool/cron/crontabs/*')
    put('./crontab', '/var/spool/cron/crontabs/root', use_sudo=True, mode=0600)
    # sudo('echo "%s" > /var/spool/cron/crontabs/root' % open('./crontab').read())
    # sudo('chmod 600 /var/spool/cron/crontabs/root')

    print '====================================================================='
    sudo("cat /var/spool/cron/crontabs/root")
    print '====================================================================='

def install_requirements():
    with open('./install.sh') as ifile:
        for iline in ifile:
            sudo(iline)

def update_network():
    put('./interfaces', '/etc/network/interfaces', use_sudo=True, mode=644)
    # sudo('echo "%s" > /etc/network/interfaces' % open('./interfaces').read())
    # sudo('chmod 644 /etc/network/interfaces')
    put('./wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf', use_sudo=True, mode=600)

    put('./8192cu.conf', '/etc/modprobe.d/8192cu.conf', use_sudo=True)
    # sudo('dhclient wlan0')
    # sudo(r'echo "%s" > /etc/wpa_supplicant/wpa_supplicant.conf' % open('./wpa_supplicant.conf').read())
    # sudo('chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf')

@parallel
def setup():
    # install_requirements()
    update_cron()
    update_network()
    reboot()

def check():
    pass
