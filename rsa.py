from random import getrandbits
from time import clock
from huff import *
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


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


def aug_read_file(file_name):
    file_handle = open(file_name, 'r')
    file_content = file_handle.read()
    file_handle.close()
    return huffman_compress(file_content)


def write_file(file_name, data):
    data_to_write = ''
    i = 0
    while i < len(data):
        data_to_write += chr(int(data[i:i+7], 2))
        i += 7
    file_handle = open(file_name, 'w')
    file_handle.write(data_to_write)
    file_handle.close()


def plot_encryption_decryption_details_1(details_dict, details_aug_dict):
    encryption_time_list = []
    decryption_time_list = []
    aug_encryption_time_list = []
    aug_decryption_time_list = []
    size_list = []
    tick_list = []
    i = 0
    while i < len(details_dict.keys()):
        encryption_time_list.append(details_dict[str(10**i) + 'kB']['encryption_time'])
        decryption_time_list.append(details_dict[str(10**i) + 'kB']['decryption_time'])
        aug_encryption_time_list.append(details_aug_dict[str(10 ** i) + 'kB']['encryption_time'])
        aug_decryption_time_list.append(details_aug_dict[str(10 ** i) + 'kB']['decryption_time'])
        size_list.append(10 ** i)
        tick_list.append(i)
        i += 1
    plt.subplot(2, 2, 1)
    plt.plot(encryption_time_list, marker='o', label='RSA')
    plt.plot(aug_encryption_time_list, marker='o', label='A-RSA')
    plt.title('Time for encryption')
    plt.legend(loc=2)
    plt.xticks(tick_list, size_list)
    plt.ylabel('time (in ms)')
    plt.xlabel('size of input file (in kB)')
    plt.subplot(2, 2, 2)
    plt.plot(size_list, encryption_time_list, marker='o', label='RSA')
    plt.plot(size_list, aug_encryption_time_list, marker='o', label='A-RSA')
    plt.title('Time for encryption')
    plt.legend(loc=2)
    plt.ylabel('time (in ms)')
    plt.xlabel('size of input file (in kB)')
    plt.subplot(2, 2, 3)
    plt.plot(decryption_time_list, marker='o', label='RSA')
    plt.plot(aug_decryption_time_list, marker='o', label='A-RSA')
    plt.title('Time for decryption')
    plt.legend(loc=2)
    plt.xticks(tick_list, size_list)
    plt.ylabel('time (in ms)')
    plt.xlabel('size of input file (in kB)')
    plt.subplot(2, 2, 4)
    plt.plot(size_list, decryption_time_list, marker='o', label='RSA')
    plt.plot(size_list, aug_decryption_time_list, marker='o', label='A-RSA')
    plt.title('Time for decryption')
    plt.legend(loc=2)
    plt.ylabel('time (in ms)')
    plt.xlabel('size of input file (in kB)')
    plt.show()


def plot_encryption_decryption_details_2(details_dict, details_aug_dict):
    input_data_size_list = []
    encrypted_data_size_list = []
    percentage_increase_list = []
    aug_input_data_size_list = []
    aug_encrypted_data_size_list = []
    aug_percentage_increase_list = []
    size_list = []
    tick_list = []
    i = 0
    while i < len(details_dict.keys()):
        input_data_size_list.append(details_dict[str(10 ** i) + 'kB']['input_data_size'])
        encrypted_data_size_list.append(details_dict[str(10 ** i) + 'kB']['encrypted_data_size'])
        percentage_increase_list.append(details_dict[str(10 ** i) + 'kB']['percentage_increase'])
        aug_input_data_size_list.append(details_aug_dict[str(10 ** i) + 'kB']['input_data_size'])
        aug_encrypted_data_size_list.append(details_aug_dict[str(10 ** i) + 'kB']['encrypted_data_size'])
        aug_percentage_increase_list.append(details_aug_dict[str(10 ** i) + 'kB']['percentage_increase'])
        size_list.append(10 ** i)
        tick_list.append(i)
        i += 1
    plt.subplot(2, 2, 1)
    plt.plot(size_list, input_data_size_list, marker='o', label='input')
    plt.plot(size_list, encrypted_data_size_list, marker='o', label='encrypted-RSA')
    plt.plot(size_list, aug_encrypted_data_size_list, marker='o', label='encrypted-A-RSA')
    plt.title('Size of input and encrypted files')
    plt.legend(loc=2)
    plt.ylabel('size (in bits)')
    plt.xlabel('size of input file (in kB)')
    plt.subplot(2, 2, 2)
    plt.plot(input_data_size_list, marker='o', label='input')
    plt.plot(encrypted_data_size_list, marker='o', label='encrypted-RSA')
    plt.plot(aug_encrypted_data_size_list, marker='o', label='encrypted-A-RSA')
    plt.title('Size of input and encrypted files')
    plt.legend(loc=2)
    plt.xticks(tick_list, size_list)
    plt.ylabel('size (in bits)')
    plt.xlabel('size of input file (in kB)')
    plt.subplot(2, 2, 3)
    plt.plot(percentage_increase_list, marker='o', label='RSA')
    plt.plot(aug_percentage_increase_list, marker='o', label='A-RSA')
    plt.title('Percentage increase in size from input to encrypted data')
    plt.legend(loc=5)
    plt.xticks(tick_list, size_list)
    plt.ylabel('Percentage increase (%)')
    plt.xlabel('size of input file (in kB)')
    plt.show()


class RsaObject(object):
    p = None
    q = None
    n = None
    phi_n = None
    e = None
    d = None
    n_length = None
    spill_over = None
    comp_keys = None

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
            if self.q!=self.p:
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
        while i < len(input_data)-self.n_length:
            M = int(input_data[i:i+self.n_length], 2)
            i = i+self.n_length
            C = format(pow(M, self.e, self.n), 'b')
            encrypted_data += '0'*(self.length-len(C)) + C
        M = int(input_data[i:], 2)
        self.spill_over = len(input_data)-i
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
        details_file_handle.write('percentage increase = ' + str(percentage_increase) + ' %\n')
        details_file_handle.write('\ntime for encryption = ' + str((end-start)*1000) + ' milliseconds\n')
        details_file_handle.write('\ninput data in bits\n' + input_data)
        details_file_handle.write('\nencrypted data in bits\n' + encrypted_data)
        details_file_handle.close()

    def aug_encrypt(self, file_name):
        input_data = read_file(file_name)
        start = clock()
        input_comp_data, self.comp_keys = aug_read_file(file_name)
        encrypted_data = ''
        i = 0
        r = self.e
        while i < len(input_comp_data)-self.n_length:
            M = int(input_comp_data[i:i + self.n_length], 2)
            M = M ^ r
            i = i + self.n_length
            C = pow(M, self.e, self.n)
            r = C >> (self.length-self.n_length)
            C = format(C, 'b')
            encrypted_data += '0' * (self.length - len(C)) + C
        M = int(input_comp_data[i:], 2)
        M = M ^ r
        self.spill_over = len(input_comp_data)-i
        C = pow(M, self.e, self.n)
        C = format(C, 'b')
        encrypted_data += '0' * (self.length - len(C)) + C
        end = clock()
        write_file('encrypted_data.txt', encrypted_data)
        encrypted_file_handle = open('encrypted_data_binary.txt', 'w')
        encrypted_file_handle.write(encrypted_data)
        encrypted_file_handle.close()
        details_file_handle = open('details.txt', 'w')
        details_file_handle.write('length of input data = ' + str(len(input_data)) + ' bits\n')
        details_file_handle.write('length of encrypted data = ' + str(len(encrypted_data)) + ' bits\n')
        percentage_increase = (len(encrypted_data) - len(input_data)) * 100 / len(input_data)
        details_file_handle.write('percentage increase = ' + str(percentage_increase) + ' %\n')
        details_file_handle.write('\ntime for encryption = ' + str((end - start) * 1000) + ' milliseconds\n')
        details_file_handle.write('\ninput compressed data in bits\n' + input_comp_data)
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
            if i != len(encrypted_data):
                M = '0' * (self.n_length - len(M)) + M
            else:
                M = '0' * (self.spill_over - len(M))+M
            decrypted_data += M
        end = clock()
        write_file('decrypted_data.txt', decrypted_data)
        details_file_handle = open('details.txt', 'a')
        details_file_handle.write('\ndecrypted data in bits\n' + decrypted_data)
        details_file_handle.write('\n\ntime for decryption = ' + str((end - start)*1000) + ' milliseconds\n')

    def aug_decrypt(self, file_name):
        file_handle = open(file_name, 'r')
        encrypted_data = file_handle.read()
        file_handle.close()
        start = clock()
        decrypted_data = ''
        i = len(encrypted_data)
        while i > 0:
            C = int(encrypted_data[i-self.length:i], 2)
            i = i - self.length
            M = pow(C, self.d, self.n)
            if i == 0:
                r = self.e
            else:
                r = int(encrypted_data[i-self.length:i], 2) >> (self.length-self.n_length)
            M = M ^ r
            M = format(M, 'b')
            if len(decrypted_data) != 0:
                M = '0' * (self.n_length - len(M)) + M
            else:
                M = '0' * (self.spill_over - len(M)) + M
            decrypted_data = M + decrypted_data
        decrypted_data_decompressed = huffman_decompress(decrypted_data, self.comp_keys)
        end = clock()
        file_handle = open('decrypted_data.txt', 'w')
        file_handle.write(decrypted_data_decompressed)
        file_handle.close()
        details_file_handle = open('details.txt', 'a')
        details_file_handle.write('\ndecrypted compressed data in bits\n' + decrypted_data)
        details_file_handle.write('\n\ntime for decryption = ' + str((end - start) * 1000) + ' milliseconds\n')


a = RsaObject(128)

filename_str = 'SampleTextFile_{}kB.txt'
details_dict = {}
i = 0
print('RSA: ')
while i <= 3:
    filename = filename_str.format(10**i)
    a.encrypt(filename)
    a.decrypt('encrypted_data_binary.txt')
    file_handle = open('details.txt', 'r')
    details_file_data = file_handle.read()
    file_handle.close()
    local_dict = {}
    details_file_data = details_file_data.split('\n')
    local_dict['encryption_time'] = float((details_file_data[4].split(' '))[4])
    local_dict['decryption_time'] = float((details_file_data[13]).split(' ')[4])
    local_dict['input_data_size'] = float((details_file_data[0]).split(' ')[5])
    local_dict['encrypted_data_size'] = float((details_file_data[1]).split(' ')[5])
    local_dict['percentage_increase'] = float((details_file_data[2]).split(' ')[3])
    details_dict[str(10**i) + 'kB'] = local_dict
    print(filename)
    print(local_dict)
    i += 1

details_aug_dict = {}
i = 0
print('\nAugmented RSA: ')
while i <= 3:
    filename = filename_str.format(10**i)
    a.aug_encrypt(filename)
    a.aug_decrypt('encrypted_data_binary.txt')
    file_handle = open('details.txt', 'r')
    details_file_data = file_handle.read()
    file_handle.close()
    local_dict = {}
    details_file_data = details_file_data.split('\n')
    local_dict['encryption_time'] = float((details_file_data[4].split(' '))[4])
    local_dict['decryption_time'] = float((details_file_data[13]).split(' ')[4])
    local_dict['input_data_size'] = float((details_file_data[0]).split(' ')[5])
    local_dict['encrypted_data_size'] = float((details_file_data[1]).split(' ')[5])
    local_dict['percentage_increase'] = float((details_file_data[2]).split(' ')[3])
    details_aug_dict[str(10**i) + 'kB'] = local_dict
    print(filename)
    print(local_dict)
    i += 1

plot_encryption_decryption_details_1(details_dict, details_aug_dict)
plot_encryption_decryption_details_2(details_dict, details_aug_dict)

a.encrypt('Sample_FOBtest.txt')
a.decrypt('encrypted_data_binary.txt')

file_handle = open('encrypted_data_binary.txt', 'r')
file_content = file_handle.read()
file_handle.close()
new_binary_data = ''
i=0
while i < len(file_content):
    new_binary_data += (file_content[i:i+128] + '\n')
    i += 128
file_handle = open('encrypted_data_binary_block.txt', 'w')
file_handle.write(new_binary_data)
file_handle.close()

input('\n\ncontinue:')

a.aug_encrypt('Sample_FOBtest.txt')
a.aug_decrypt('encrypted_data_binary.txt')

file_handle = open('encrypted_data_binary.txt', 'r')
file_content = file_handle.read()
file_handle.close()
new_binary_data = ''
i=0
while i < len(file_content):
    new_binary_data += (file_content[i:i+128] + '\n')
    i += 128
file_handle = open('encrypted_data_binary_block.txt', 'w')
file_handle.write(new_binary_data)
file_handle.close()


