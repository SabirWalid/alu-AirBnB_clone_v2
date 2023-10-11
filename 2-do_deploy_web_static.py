#!/usr/bin/python3
"""Fabric script that distributes an archive to a web servers"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

env.hosts = ['54.167.15.9', '54.162.155.171']
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""

    now = datetime.now()
    date = now.strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    local("mkdir -p versions")
    local("tar -cvzf {} web_static".format(filename))
    if os.path.exists(filename):
        return filename
    return None


def do_deploy(archive_path):
    """distributes an archive to a web servers"""

    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        filename = archive_path.split("/")[-1]
        name = filename.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(name), timeout=10)
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            filename, name), timeout=10)
        run("rm /tmp/{}".format(filename), timeout=10)
        run("cp -rf /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(name, name), timeout=10)
        run("rm -rf /data/web_static/releases/{}/web_static".format(name), timeout=10)
        run("rm -rf /data/web_static/current", timeout=10)
        run("ln -s /data/web_static/releases/{}/ \
            /data/web_static/current".format(
            name), timeout=10)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(e)
        return False
