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