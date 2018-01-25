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
from os.path import exists
from json import loads, dumps
from copy import deepcopy
from time import time


class colors:

    color = {
        "HEADER": '\033[95m',
        "OKBLUE": '\033[94m',
        "OKGREEN": '\033[92m',
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m',
        "UNDERLINE": '\033[4m'
    }

    @staticmethod
    def text(value, color):
        return colors.color[color] + value + colors.color["ENDC"]


class Validators:

    @staticmethod
    def mail(value):
        return False if match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value) is None else True

    @staticmethod
    def date(value):
        return False if match(r"(^(0?[1-9]|[12][0-9]|3[01])[/](0?[1-9]|1[012])[/]\d{4}$)", value) is None else True


class Data:

    profile_template = {
            "__creadate__": 0,
            "__lastupdate__": 0,
            "__description__": "",
            "names": [],
            "mail": "",
            "b_date": "",
            "f_things": [],
            "nicknames": [],
            "t_numbers": []
        }

    validators = {
        "mail": [Validators.mail, "E-Mail is not valid!"],
        "b_date": [Validators.date, "Date not in DD/MM/YYYY format!"]
    }

    noLoadedProfile = "No profile is loaded!"
    profiles = {}
    active_profile = ""
    passwords = []
    filename = "profiles.json"
    endings = []


class Utils:

    @staticmethod
    def load():
        if exists(Data.filename):
            with open(Data.filename) as f:
                content = f.read()
                if len(content) > 0:
                    Data.profiles = loads(content)
                    print("Loaded {} profiles from file!".format(len(Data.profiles)))

    @staticmethod
    def isNotEmpty(*args):
        for arg in args:
            if arg not in Data.profiles[Data.active_profile].keys():
                return False
        return True

    @staticmethod
    def getValue(option):
        return Data.profiles[Data.active_profile][option]

    @staticmethod
    def addPassword(password):
        if password not in Data.passwords:
            Data.passwords.append(password)

    @staticmethod
    def generate():
        if Data.active_profile:
            print(Data.noLoadedProfile)
            return
        i = 0
        while True:
            if ("step" + str(i)) in PasswordGenerator.__dict__.keys():
                getattr(PasswordGenerator, "step" + str(i))()
            else:
                break
            i += 1

    @staticmethod
    def checkAndValidate(option, value, cls):
        if not Data.active_profile:
            print(Data.noLoadedProfile)
            return False
        if option == "info" and isinstance(cls, str):
            Data.profiles[Data.active_profile]["__description__"] = value
            return False
        if option.startswith("__"):
            print(colors.text("Option {} does not exists!"), "WARNING")
            return False
        if option not in Data.profiles[Data.active_profile].keys():
            print(colors.text("Option {} does not exists!"), "WARNING")
            return False
        if not isinstance(Data.profiles[Data.active_profile][option], cls):
            if isinstance(Data.profiles[Data.active_profile][option], list):
                print(colors.text("Option {} is list, you must add/remove command!".format(option)), "WARNING")
                return False
            else:
                print(colors.text("Option {} is string, you must set/empty command!".format(option)), "WARNING")
                return False
        return True


class Controls:

    @staticmethod
    def write():
        with open(Data.filename, "a+") as f:
            f.truncate()
            f.write(dumps(Data.profiles))

    @staticmethod
    def selectProfile(name):
        if name in Data.profiles.keys():
            Data.active_profile = name
        else:
            print("Profile {} cannot exists!".format(name))

    @staticmethod
    def createProfile(name):
        if name not in Data.profiles.keys():
            Data.profiles.update({name: deepcopy(Data.profile_template)})
            Data.active_profile = name
            Data.profiles[Data.active_profile]["__creadate__"] = time()
            Data.profiles[Data.active_profile]["__lastupdate__"] = time()
        else:
            print("Profile {} already exists!".format(name))

    @staticmethod
    def showOptions(all_):
        if not Data.active_profile:
            print(Data.noLoadedProfile)
            return
        out = "\n"
        for option in Data.profiles[Data.active_profile].keys():
            if all_:
                out += "{} : {}\n".format(option, Data.profiles[Data.active_profile][option])
            else:
                if Data.profiles[Data.active_profile][option] != "" and Data.profiles[Data.active_profile][option] != []:
                    out += "{} : {}\n".format(option, Data.profiles[Data.active_profile][option])
        print(out)

    @staticmethod
    def setOption(option, value):
        if Utils.checkAndValidate(option, value, str) and (Data.profiles[Data.active_profile][option] != value):
            Data.profiles[Data.active_profile]["__lastupdate__"] = time()
            Data.profiles[Data.active_profile][option] = value
            print(colors.text("[{}][{}] = {}".format(Data.active_profile, option, value), "OKGREEN"))

    @staticmethod
    def addItemToList(option, value):
        if Utils.checkAndValidate(option, value, list) and (value not in Data.profiles[Data.active_profile][option]):
            Data.profiles[Data.active_profile][option].append(value)
            print(colors.text("[{}][{}] < {}".format(Data.active_profile, option, value), "OKGREEN"))

    @staticmethod
    def removeLastItemFromlist(option):
        if Utils.checkAndValidate(option, "", list) and (len(Data.profiles[Data.active_profile][option]) > 0):
            value = Data.profiles[Data.active_profile][option].pop(-1)
            print(colors.text("[{}][{}] > {}".format(Data.active_profile, option, value), "OKGREEN"))


    @staticmethod
    def printPasswords():
        Utils.generate()
        r = ""
        for pas in Data.passwords:
            r = r + pas + "\n"
        print(r[:-1])

    @staticmethod
    def count():
        Utils.generate()
        print(colors.text("Probably passwords count: " + str(len(Data.passwords)), "OKGREEN"))


class WordUtils:

    @staticmethod
    def cases(value):
        ret = []
        ret.append(value.lower())
        ret.append(value.upper())
        if len(value > 1):
            ret.append(value[0].upper() + value[1:].lower())
        return ret

    @staticmethod
    def findNumberEndings():
        lst = []
        if Utils.isNotEmpty("mail"):
            lst.append(Utils.getValue("mail").split("@")[0])
        for number in Utils.getValue("t_numbers"):
            Utils.addPassword(number[-3:])
        lst.extend(Utils.getValue("f_things").extend(Utils.getValue("nicknames")))
        for word in lst:
            for i in range(len(word)):
                try:
                    int(word[i:], 10)
                except:
                    continue
                Data.endings.append(word[i:])
                break
        

class PasswordGenerator:

    endings = []

    @staticmethod
    def step0():
        WordUtils.findNumberEndings()

    @staticmethod
    def step1():
        if Utils.isNotEmpty("t_numbers"):
            for number in Utils.getValue("t_numbers"):
                Utils.addPassword(number)
                numberClean = ""
                for c in number:
                    try:
                        int(c, 10)
                    except ValueError:
                        continue
                    numberClean += c
                Utils.addPassword(numberClean)
                numberCleanWithSpaces = ""
                for c in number:
                    if c in "0123456789 ":
                        numberCleanWithSpaces += c
                Utils.addPassword(numberCleanWithSpaces)



    @staticmethod
    def step2():
        if Utils.isNotEmpty("b_date"):
            date = Utils.getValue("b_date")
            Utils.addPassword(date.replace("/", ""))
            date = date.split("/", "")
            Utils.addPassword((date[0] + date[1]) * 2)
            Utils.addPassword((date[2] + date[2]) * 2)
            Utils.addPassword((date[0] + date[1]) + date[2][-2:])

    @staticmethod
    def step3():
        if Utils.isNotEmpty("f_things"):
            date = Utils.getValue("b_date")



if __name__ == "__main__":
    print(banner)
    Utils.load()
    while True:
        inp = raw_input(">> " if Data.active_profile == "" else colors.text("[{}]".format(Data.active_profile), "OKBLUE") + "  >> ").split(" ")

        if len(inp) == 0:
            continue

        if len(inp) == 1:
            if inp[0] == "help":
                print("\n" + help + "\n")
                continue

            elif inp[0] == "print":
                Controls.printPasswords()
                continue

            elif inp[0] == "count":
                Controls.count()
                continue

            elif inp[0] == "save":
                Controls.write()
                continue

            elif inp[0] == "exit":
                exit(0)
                continue

        if len(inp) == 2:

            if inp[0] == "options":
                if inp[1] == "all":
                    Controls.showOptions(True)
                    continue

                elif inp[1] == "filled":
                    Controls.showOptions(False)
                    continue

                else:
                    print (colors.text("options all/filled", "WARNING"))
                    continue

            elif inp[0] == "empty":
                Controls.setOption(inp[1], "")
                continue

            elif inp[0] == "remove":
                Controls.removeLastItemFromlist(inp[1])
                continue

            elif inp[0] == "select":
                Controls.selectProfile(inp[1])
                continue

            elif inp[0] == "create":
                Controls.createProfile(inp[1])
                continue

        if len(inp) == 3:

            if inp[0] == "set":
                Controls.setOption(inp[1], inp[2])
                continue

            elif inp[0] == "add":
                Controls.addItemToList(inp[1], inp[2])
                continue

        print(colors.text("Unknown command!", "WARNING"))
