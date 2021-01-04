import hashlib


def crack_key(key, start='00000'):
    i = 1
    while True:
        md5 = hashlib.md5((key + str(i)).encode())
        if md5.hexdigest().startswith(start):
            return i
        i += 1


assert crack_key('abcdef') == 609043
assert crack_key('pqrstuv') == 1048970
print('4a: ', crack_key('bgvyzdsv'))
print('4b: ', crack_key('bgvyzdsv', '000000'))
