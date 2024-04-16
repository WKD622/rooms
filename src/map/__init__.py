class Map:
    def __init__(self, file_path):
        self.fp = open(file_path, 'r')

        self.width = len(self.fp.readline()) - 1  # we need to subtract EOL character
        self.fp.seek(0)
        self.content = self.fp.readlines()
        self.height = len(self.content)

    def get_dimensions(self):
        return self.width, self.height
