from ly.cli.command import version

import argsniffer
import reqgen


def main():
    args = argsniffer.parse_args()
    version = ""

    if args.package.startswith('pkg:maven'):
        args.package = args.package[len('pkg:maven/'):]
    if "@" in args.package:
        version = args.package.split("@")[1]
        args.package = args.package.split("@")[0]




if __name__ == "__main__":
    main()