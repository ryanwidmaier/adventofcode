import hashlib

input_data = 'wtnhxymk'
# input_data = 'abc'

code = ['-'] * 8
i = 0

while '-' in code:
    md5 = hashlib.md5()

    hash_input = input_data + str(i)
    md5.update(hash_input)
    hash_output = md5.hexdigest()

    if hash_output.startswith('00000'):
        pos, ch = hash_output[5:7]

        if '0' <= pos < '8':
            pos = ord(pos) - ord('0')
            if code[pos] == '-':
                code[pos] = ch

    i += 1
    if i % 10000:
        print "I={}, code={}".format(i, ''.join(code))

print ''.join(code)
