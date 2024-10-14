import tarfile

class VirtFS:
    def __init__(self, path):
        self.tree = {}
        self.dir = '/'
        self.init_fs(path)
    
    def init_fs(self, path):
        with tarfile.open(path, "r") as tar:
            for i in tar.getmembers():
                self.pushtree(i)
    
    def pushtree(self, file):
        path = file.name.split('/')
        current = self.tree

        for i in path:
            if i not in current:
                current[i] = {}
            current = current[i]
    
    def listdir(self, path=None):
        if path is None:
            path = self.dir
        dir = self.jumpto(path)
        if dir is None:
            print(F"ls: {path}: No such file or directory")
            return []
        return list(dir.keys())
    
    def jumpto(self, path):
        dir = self.goto(path)
        if dir is not None:
            if path.startswith('/'):
                self.dir = '/' + '/'.join(path.strip('/').split('/'))
            else:
                parts = self.dir.strip('/').split('/') + path.split('/')
                new_parts = []
                for i in parts:
                    if i == '..':
                        if new_parts:
                            new_parts.pop()
                    elif i != '.' and i != '':
                        new_parts.append(i)
        else:
            print(f"cd: {path}: No such directory")
    
    def goto(self, path):
        if path.startswith('/'):
            dir = self.tree
            path_parts = path.strip('/').split('/')
        else:
            path_parts = self.dir.strip('/').split('/') + path.split('/')

        new_path = []

        for i in path_parts:
            if i == '..':
                if new_path:
                    new_path.pop()
            elif i == '.' or i == '':
                continue
            else:
                new_path.append(i)
        
        dir - self.tree
        for i in new_path:
            if i in dir:
                dir = dir[i]
            else:
                return None
        
        return dir
    

    def ls(vfs):
        for i in vfs.listdir():
            print(i)
    
    def cd(vfs, path):
        vfs.jumpto(path)
    

    def du(vfs, tar):
        dir = vfs.dir.strip('/')
        for i in tar.getmembers():
            if i.isfile() and i.name.startswith(dir):
                print(f"{i.size} ./{i.name}")

    def uname():
        print("Darwin")
    
    def rmdir(vfs, dir_name):
        node = vfs.goto(vfs.dir)
        if dir_name in node and not node[dir_name]:
            del node[dir_name]
        else:
            print(f"rmdir: {dir_name}: No such file or directory")