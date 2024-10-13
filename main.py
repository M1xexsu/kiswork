import os




def main():
    args = _getargs()
    vfs = _makefs()
    logs = _logs(args.logfile, args.user)

main()