# Copyright (c) 2017 Michal Paulenka <paulenkamichal@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


banner = """
.------------------..------------------..------------------. 
| .--------------. || .--------------. || .--------------. |
| |   ______     | || |    ______    | || | ____    ____ | |
| |  |_   __ \   | || |  .' ___  |   | || ||_   \  /   _|| |
| |    | |__) |  | || | / .'   \_|   | || |  |   \/   |  | |
| |    |  ___/   | || | | |    ____  | || |  | |\  /| |  | |
| |   _| |_      | || | \ `.___]  _| | || | _| |_\/_| |_ | |
| |  |_____|     | || |  `._____.'   | || ||_____||_____|| |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' 
                (Password Guessing Machine)
                                                 by F3sh1d3r
"""

help = """"""

from re import match


class Validators:

    @staticmethod
    def mail(value):
        return False if match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value) is None else True

    @staticmethod
    def date(value):
        return False if match(r"(^(0?[1-9]|[12][0-9]|3[01])[/](0?[1-9]|1[012])[/]\d{4}$)", value) is None else True

data = {
    "f_name": ["", None],
    "l_name": ["", None],
    "mail": ["", Validators.mail, "E-Mail is not valid!"],
    "b_date": ["", Validators.date, "Date not in DD/MM/YYYY format!"]
}

class PasswordGenerator:

    passwords = []

    @staticmethod
    def isNotEmpty(*args):
        for arg in args:
            if arg not in data.keys():
                return False
        return True

    @staticmethod
    def patternBirthDate():
        if PasswordGenerator.isNotEmpty("b_date"):
            date = data["b_date"][0].split("/")
            PasswordGenerator.passwords.append("".join[date])
            PasswordGenerator.passwords.append((date[0] + date[1])*2)

    @staticmethod
    def generate():
        for method in PasswordGenerator.__dict__.keys():
            if method.startswith("pattern"):
                PasswordGenerator.__dict__[method].__get__(object)

    @staticmethod
    def printPasswords():
        PasswordGenerator.generate()
        r = ""
        for pas in PasswordGenerator.passwords:
            r = r + pas + "\n"
        print(r[:-1])

class Controller:

    @staticmethod
    def getData(all):
        r = ""
        for key in data.keys():
            if all:
                r = r + "  " + key + " : " + data[key][0] + "\n"
            else:
                if data[key][0] != "":
                    r = r + "  " + key + " : " + data[key][0] + "\n"
        return r

    @staticmethod
    def setData(key, value):
        for k in data.keys():
            if k == key:
                if data[key][1] is not None:
                    if not data[key][1](value):
                        return data[key][2]
                data[key][0] = value
                return "  " + key + " : " + value
        return "Not found option: " + key


if __name__ == "__main__":
    print(banner)
    while True:
        inp = raw_input(">> ").split(" ")

        if len(inp) == 0:
            continue

        if len(inp) == 1:
            if inp[0] == "help":
                print("\n" + help + "\n")
                continue
            elif inp[0] == "passwords":
                PasswordGenerator.printPasswords()
                continue

        if len(inp) == 2:
            if inp[0] == "options":
                if inp[1] == "all":
                    print(Controller.getData(True)[:-1])
                    continue
                elif inp[1] == "filled":
                    print(Controller.getData(False)[:-1])
                    continue
                else:
                    print ("options all/filled")
                    continue
            elif inp[0] == "empty":
                print(Controller.setData(inp[1], ""))
                continue

        if len(inp) == 3:
            if inp[0] == "set":
                print(Controller.setData(inp[1], inp[2]))
                continue

        print("Unknown command!")
