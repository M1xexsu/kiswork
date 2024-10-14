import argsniffer
import VirtFS



def main():
    args = argsniffer.parse_args()
    vfs = VirtFS(args.filesystem)
    logs = (args.logfile, args.user)

main()