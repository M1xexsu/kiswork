import argsniffer
import xmlparser


def main():
    args = argsniffer.parse_args()
    parser = xmlparser.xm()
    parser.convert(args.input, args.output)
    

if __name__ == "__main__":
    main()