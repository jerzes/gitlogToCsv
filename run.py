import re


class GitlogToCsv():

    def __init__(self, file):
        self.filename = file
        self.ws_counter = -1
        self.list = []
        self.csv = ""

    def commit(self, commit):
        rt = commit.split(" ")[1]
        return rt.rstrip()

    def author(self, author):
        result = author.split('<')[1][:-2]
        return result

    def message(self, msg):
        return msg.lstrip().rstrip()

    def date(self, dat):
        tab = dat.split(' ',4)
        result = tab[4][:-7]
        return result

    def createRecord(self):
        rec = ";".join(self.list)
        self.csv += rec+';\n'
        self.list = []

    def getRecord(self, iter):
        if iter.find("Author") == 0:
            return self.author(iter)
        elif iter.find("commit") == 0:
            return self.commit(iter)
        elif iter.find("Date") == 0:
            self.ws_counter = 0
            return self.date(iter)
        elif re.match(r'\n', iter) and self.ws_counter != 1:
            self.ws_counter = self.ws_counter + 1
            return -1
        elif re.match(r'\s', iter) and self.ws_counter == 1:
            self.ws_counter = -1
            return self.message(iter)
    def getCsv(self):
        return self.csv

    def saveCsv(self, filename):
        f = open(filename, "w+")
        f.write(self.getCsv())
        f.close()

    def convert(self):
        try:
            f = open(self.filename)
            tab = f.readlines()
            count = 0
            for i in tab:
                result = self.getRecord(i)

                if result != -1:
                    self.list.append(result)
                    count += 1
                if count == 4:
                    self.createRecord()
                    count = 0

        except IOError as e:
            print(e)


git = GitlogToCsv("log.txt")
git.convert()
print(git.getCsv())
git.saveCsv("pajac.csv")
