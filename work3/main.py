import argsniffer
import xmlparser
import re




def main():
    args = argsniffer.parse_args()
    with open(args.input, "r") as w:
        file = w.read()
    file = re.sub(r"<!--",'<comment>',file)
    file = re.sub(r"-->",'</comment>',file)
    print(file)
    parser = xmlparser.xm()
    parser.convert(file, args.output)

    

if __name__ == "__main__":
    main()