import enum
import requests
import random
import string

class Operators(enum.Enum):
    equal = 0
    plus = 1
    minus = 2
    times = 3
    divide = 4


def reverse(s):
    return s[::-1]

if __name__ == "__main__":
    while 1:
        user = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        psw = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        r = requests.post("http://lnhnzd.cn/2018.php", {"user" : user, "pass" : psw}, allow_redirects=False)
        print(r.status_code)