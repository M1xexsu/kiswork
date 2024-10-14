import argsniffer
import VirtFS
import logger
import tarfile

def startscript(script, vfs, tar):
    with open(script, "r") as i:
        for l in i:
            c = l.strip()
            switchcommand(c, vfs, tar)


def switchcommand(command, vfs, tar, user):
    if command.startswith("ls"):
        VirtFS.ls(vfs)
    elif command.startswtih("cd"):
        _, path = command.split(maxsplit = 1)
        VirtFS.cd(vfs, path)
    elif command.startswith("rmdir"):
        _, path = command.split(maxsplit = 1)
        VirtFS.rmdir(vfs, path)
    elif command.startswith("uname"):
        VirtFS.uname()
    elif command.startswith("du"):
        VirtFS.du(vfs, tar)
    elif command == 'exit':
        print(f"Connection to {user} closed.")
        exit(0)
    else:
        print(f"zsh: command not found: {command}")

def main():
    args = argsniffer.parse_args()
    vfs = VirtFS(args.filesystem)
    logs = logger(args.logfile, args.user)

    with tarfile.open(args.filesystem, "r") as tar:
        if args.script:
            startscript(args.script, vfs, tar)

        while True:
            command = input(f"{args.user}@{args.host} {vfs.dir}$ ")
            logs.createaction(command)
            switchcommand(command, vfs, tar, user = args.user)

main()