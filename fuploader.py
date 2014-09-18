import glob
import json
import shutil
import click
from subprocess import Popen, PIPE
import sys
import os


def read_conf(filepath=None):
    conf = dict(
        DEF_TARGET="example.com",
        DEF_FOLDER="~/public_html/",
        DEF_PREFIX="~username",
    )
    if not filepath:
        filepath = "~/.config/fuploader.json"

    try:
        with open(filepath) as inp:
            raw_conf = json.loads(inp.read())
    except Exception:
        raw_conf = {}

    conf.update(raw_conf)
    return conf

@click.command()
@click.option('--target', '-t', default=None,
              help='Target host to upload files')
@click.option('--folder', '-f', default=None,
              help='Base folder on remote host')
@click.option('--sub-folder', '-s', default='',
              help='Sub folder on remote host, will be '
                   'added to http prefix as well')
@click.option('--prefix', '-p', default=None,
              help='Prefix to append after hostname for results')
@click.option('--verbose', '-v', default=False, is_flag=True,
              help='Enable verbose output')
@click.option('--cleanup', '-c', default=False, is_flag=True,
              help='Delete uploaded files from local machine')
@click.argument('src_files', nargs=-1)
def upload(target, folder, sub_folder, prefix, src_files, verbose, cleanup):
    conf = read_conf()

    target = target or conf["DEF_TARGET"]
    folder = folder or conf["DEF_FOLDER"]
    prefix = prefix or conf["DEF_PREFIX"]

    files = []

    unvisited = set(src_files)
    while unvisited:
        fn = unvisited.pop()
        if os.path.exists(fn):
            if os.path.isfile(fn):
                files.append(os.path.abspath(fn))
            elif os.path.isdir(fn):
                for r, d, _files in os.walk(fn):
                    #pre = os.path.join(r, *d)
                    for f in _files:
                        files.append(os.path.join(r, f))
        else:
            for f in glob.glob(fn):
                unvisited.add(os.path.abspath(f))

    if not files:
        click.echo("Nothing to upload, bye!")
        sys.exit(0)
    if verbose:
        click.echo("Going to upload:\n\t{}".format("\n\t".join(files)))

    cmd = ['rsync', '-avz']
    cmd.extend(files)

    remote_path = "{}:{}".format(target, folder)
    if sub_folder:
        remote_path = "{}/{}/".format(remote_path, sub_folder)
    cmd.append(remote_path)

    if verbose:
        click.echo("Executing command: \n\t{}".format(" ".join(cmd)))

    handle = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = handle.communicate()

    if verbose:
        click.echo("stdout: \n{}".format(stdout), err=True)
        click.echo("stderr: \n{}".format(stderr), err=True)

    click.echo("Upload finished\nFiles on server:")

    if prefix and prefix[-1] != "/":
        prefix += "/"

    results = []
    base_path = "http://{}/{}".format(target, prefix)
    if sub_folder:
        base_path = "{}{}/".format(base_path, sub_folder)

    for fn in files:
        results.append("{}{}".format(base_path, os.path.basename(fn)))

    click.echo("\n".join(results))

    if cleanup:
        for fn in files:
            os.remove(fn)

        click.echo("files removed")


if __name__ == '__main__':
    upload()
