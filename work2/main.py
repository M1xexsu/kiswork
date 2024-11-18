from ly.cli.command import version

import argsniffer
import reqgen
import generateoutput
import requests
import xml.etree.ElementTree as ET


def main():
    args = argsniffer.parse_args()
    version = ""

    if args.package.startswith('pkg:maven'):
        args.package = args.package[len('pkg:maven/'):]
    if "@" in args.package:
        version = args.package.split("@")[1]
        args.package = args.package.split("@")[0]
    else:
        pkgxml = requests.get(
            f'https://repo1.maven.org/maven2/{args.package.replace('.','/')}/maven-metadata.xml').text
        version = ET.fromstring(pkgxml).find('versioning/release').text

    reqgen.generate(args.package, int(args.depth), version, 0 , args.file)
    with open(f"{args.file}.puml", "a") as f:
        f.write("@enduml")
    generateoutput.generateOutput(args.file, args.library)




if __name__ == "__main__":
    main()