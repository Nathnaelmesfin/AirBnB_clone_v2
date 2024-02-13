#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers.

Execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, sudo
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['54.90.48.122','52.86.192.93']

def do_pack():
    """Generates a tgz archive from the contents of the web_static folder."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(e)  # Added for debugging
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        sudo('mkdir -p {}{}/'.format(path, no_ext))
        sudo('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        sudo('rm /tmp/{}'.format(file_n))
        sudo('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        sudo('rm -rf {}{}/web_static'.format(path, no_ext))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as e:
        print(e)  # Added for debugging
        return False

def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
