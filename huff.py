import operator


def huffman_compress(message):
    freqs = {}
    message_set = list(set(message))
    for c in message_set:
        freqs[c] = message.count(c)
    tree = sorted(freqs.items(), key=operator.itemgetter(1))

    def cumulative_freq(tree, total=0):
        if type(tree[1]) == type(2):
            return tree[1]
        else:
            total += cumulative_freq(tree[0], total)
            total += cumulative_freq(tree[1], total)
        return total

    while len(tree) > 2:
        tree.append([tree[0], tree[1]])
        tree = tree[2:]
        tree = sorted(tree, key=cumulative_freq)

    def create_codes(tree, code_builder, codes):
        if str(type(tree[1])) == "<class 'int'>":
            codes[tree[0]] = code_builder
            return codes
        else:
            codes = create_codes(tree[0], code_builder + '0', codes)
            codes = create_codes(tree[1], code_builder + '1', codes)
            return codes

    codes = create_codes(tree, '', {})
    key = {v: k for k, v in codes.items()}
    binary = ''.join([codes[x] for x in message])
    return binary, key


def huffman_decompress(message, key):
    binary = message
    m = ''
    start = 0
    while start < len(binary):
        for end in range(start+1, len(binary)+1):
            if (key.get(binary[start:end]) != None):
                m += key.get(binary[start:end])
                start = end
                break
    return m


if __name__ == '__main__':
    f = open('input.txt', 'r')
    mess = f.read()
    f.close()
    m, k = huffman_compress(mess)
    s = huffman_decompress(m, k)
    print(s)
