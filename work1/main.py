import argsniffer
import VirtFS
import logger
import tarfile

def startscript(script, vfs, tar):
    try:
        with open(script, "r") as i:
            for l in i:
                c = l.strip()
                if c:
                    switchcommand(c, vfs, tar, user=None)
    except FileNotFoundError:
        print(f"Ошибка: Стартовый скрипт {script} не найден.")
    except Exception as e:
        print(f"Ошибка при выполнении стартового скрипта: {e}")

def switchcommand(command, vfs, tar, user):
    try:
        if command.startswith("ls"):
            print(vfs.listdir())
        elif command.startswith("cd"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                path = parts[1]
                vfs.jumpto(path)
            else:
                print("zsh: cd: missing argument")
        elif command.startswith("rmdir"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                path = parts[1]
                vfs.rmdir(path)
            else:
                print("zsh: rmdir: missing argument")
        elif command.startswith("uname"):
            print("Darwin")
        elif command.startswith("du"):
            vfs.du(tar)
        elif command == 'exit':
            print(f"Connection to {user} closed.")
            exit(0)
        else:
            print(f"zsh: command not found: {command}")
    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")


def main():
    args = argsniffer.parse_args()
    vfs = VirtFS.VirtFS(args.filesystem)
    logs = logger.logger(args.logfile, args.user)

    try:
        with tarfile.open(args.filesystem, "r") as tar:
            if args.script:
                startscript(args.script, vfs, tar)
            while True:
                try:
                    command = input(f"{args.user}@{args.host} {vfs.dir}$ ")
                    logs.createaction(command)
                    switchcommand(command, vfs, tar, user=args.user)
                except KeyboardInterrupt:
                    print("\nПрерывание программы.")
                    break
    except FileNotFoundError:
        print(f"Ошибка: Файловая система {args.filesystem} не найдена.")
    except Exception as e:
        print(f"Ошибка при работе с файловой системой: {e}")

if __name__ == "__main__":
    main()
