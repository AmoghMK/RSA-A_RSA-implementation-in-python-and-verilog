from random import getrandbits
from time import clock


def generate_random_number(length, make_odd=True):
    if make_odd:
        return getrandbits(length) | 1
    else:
        return getrandbits


# Miller-Rabin Primality Test
def check_prime(number):
    if number == 1 or number == 0:
        return False
    a_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    d = number-1
    s = 0
    while d & 1 == 0:
        s = s+1
        d = d//2
    for a in a_list:
        if a >= number:
            break
        if pow(a, d, number) == 1:
            continue
        else:
            composite_flag = True
            for r in range(s):
                d2 = d << r
                if pow(a, d2, number) == number-1:
                    composite_flag = False
                    break
            if composite_flag:
                return False
    return True


def read_file(file_name):
    file_handle = open(file_name, 'r')
    file_content = file_handle.read()
    file_handle.close()
    data = ''
    for x in file_content:
        x_bin = format(ord(x), 'b')
        data += '0'*(7-len(x_bin)) + x_bin
    return data


def write_file(file_name, data):
    data_to_write = ''
    i = 0
    while i < len(data):
        data_to_write += chr(int(data[i:i+7], 2))
        i += 7
    file_handle = open(file_name, 'w')
    file_handle.write(data_to_write+'\n')
    file_handle.write(data)
    file_handle.close()


class RsaObject(object):
    p = None
    q = None
    n = None
    phi_n = None
    e = None
    d = None
    n_length = None
    spill_over = None

    def __init__(self, length):
        self.length = length
        start = clock()
        self.generate_prime_numbers(int(self.length/2))
        self.generate_keys()
        end = clock()
        print('time taken for key generation = ', (end-start)*1000, ' milliseconds')
        print(self.__dict__)

    def generate_prime_numbers(self, length):
        flag = False
        while not flag:
            self.p = generate_random_number(length)
            flag = check_prime(self.p)
        flag = False
        while not flag:
            self.q = generate_random_number(length)
            flag = check_prime(self.q)
        self.n = self.p * self.q
        self.n_length = len(format(self.n, 'b'))-1
        self.phi_n = (self.p-1) * (self.q-1)

    def generate_keys(self):
        self.e = 3
        while True:
            a = self.phi_n
            b = self.e
            y = 1
            y_prev = 0
            while b != 0:
                temp_a = a
                temp_b = b
                temp_y = y
                a = temp_b
                b = temp_a % temp_b
                y = y_prev - (temp_a//temp_b)*temp_y
                y_prev = temp_y
            if a == 1 and y_prev >= 0:
                self.d = y_prev
                return
            else:
                self.e += 2

    def encrypt(self, file_name):
        input_data = read_file(file_name)
        start = clock()
        encrypted_data = ''
        i = 0
        while i < len(input_data):
            M = int(input_data[i:i+self.n_length], 2)
            i = i+self.n_length
            C = format(pow(M, self.e, self.n), 'b')
            encrypted_data += '0'*(self.length-len(C)) + C
        if i != len(input_data):
            M = int(input_data[i-self.n_length:], 2)
            self.spill_over = (self.n_length-(i-len(input_data)))
            C = format(pow(M, self.e, self.n), 'b')
            encrypted_data += '0' * (self.length - len(C)) + C
        end = clock()
        write_file('encrypted_data.txt', encrypted_data)
        encrypted_file_handle = open('encrypted_data_binary.txt', 'w')
        encrypted_file_handle.write(encrypted_data)
        encrypted_file_handle.close()
        details_file_handle = open('details.txt', 'w')
        details_file_handle.write('length of input data = ' + str(len(input_data)) + ' bits\n')
        details_file_handle.write('length of encrypted data = ' + str(len(encrypted_data)) + ' bits\n')
        percentage_increase = (len(encrypted_data)-len(input_data))*100/len(input_data)
        details_file_handle.write('percentage increase = ' + str(percentage_increase) + '%\n')
        details_file_handle.write('\ntime for encryption = ' + str((end-start)*1000) + ' milliseconds\n')
        details_file_handle.write('\ninput data in bits\n' + input_data)
        details_file_handle.write('\nencrypted data in bits\n' + encrypted_data)
        details_file_handle.close()

    def decrypt(self, file_name):
        file_handle = open(file_name, 'r')
        encrypted_data = file_handle.read()
        file_handle.close()
        start = clock()
        decrypted_data = ''
        i = 0
        while i < len(encrypted_data):
            C = int(encrypted_data[i:i+self.length], 2)
            i = i + self.length
            M = format(pow(C, self.d, self.n), 'b')
            M = '0'*(self.n_length-len(M)) + M
            if i == len(encrypted_data):
                decrypted_data = decrypted_data[:-self.n_length]
                M = M[-self.spill_over:]
            decrypted_data += M
        end = clock()
        write_file('decrypted_data.txt', decrypted_data)
        details_file_handle = open('details.txt', 'a')
        details_file_handle.write('\ndecrypted data in bits\n' + decrypted_data)
        details_file_handle.write('\n\ntime for decryption = ' + str((end - start)*1000) + ' milliseconds\n')


a = RsaObject(128)
a.encrypt('input.txt')
a.decrypt('encrypted_data_binary.txt')
exit()
