# coding=utf-8

def loadFile(path):
    with open(path) as fr:
        content = fr.read()
    return content


class HuffmanNode:
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data


from collections import Counter
import heapq


class HuffmanCode:
    def __init__(self, content):
        self.content = content
        self.freq = [(cnt, HuffmanNode(data=ch)) for ch, cnt in Counter(self.content).items()]
        heapq.heapify(self.freq)  # 最小堆
        self.tree = self.createHuffmanTree()
        self.code = {}
        self.getHuffmanCode(self.tree, prefix='', code=self.code)

    def createHuffmanTree(self):
        while len(self.freq) > 1:
            l, r = heapq.heappop(self.freq), heapq.heappop(self.freq)
            newnode = HuffmanNode(left=l[1], right=r[1])
            heapq.heappush(self.freq, (l[0] + r[0], newnode))
        return self.freq[0][1]

    def getHuffmanCode(self, node, prefix="", code={}):
        if node and node.left is None and node.right is None:
            code[node.data] = prefix
            return
        self.getHuffmanCode(node.left, prefix=prefix + '0', code=code)
        self.getHuffmanCode(node.right, prefix=prefix + '1', code=code)

    def compress(self, compress_file=None):
        codes = ''
        for ch in content:
            codes += self.code[ch]
        if compress_file:
            packed_data = ''.join(chr(int(codes[i:i + 8], 2)) for i in range(0, len(codes), 8))
            packed_data = chr(len(codes) % 8) + packed_data  # 记录最后一个编码的长度
            with open(compress_file, 'wb') as fw:
                fw.write(packed_data)
        return codes

    def decodeHuffman(self, codes):
        n = len(codes)
        i = 0
        res = ''
        while i < n:
            node = self.tree
            while node and node.left and node.right:
                if codes[i] == '0':
                    node = node.left
                else:
                    node = node.right
                i += 1
            res += node.data
        return res

    def decodeHuffmanFromFile(self, compress_file):
        with open(compress_file, 'rb') as fr:
            compress_data = fr.read()

        last_byte_length, compress_data, last_byte = (
            compress_data[0], compress_data[1:-1], compress_data[-1]
        )
        if not last_byte_length:
            last_byte_length = 8
        codes = reduce(lambda x, y: x + y, [bin(ord(byte))[2:].zfill(8) for byte in compress_data]) \
                + bin(ord(last_byte))[2:].zfill(ord(last_byte_length))
        print 'read compress file done'
        res = self.decodeHuffman(codes)
        return res


if __name__ == '__main__':
    content = loadFile(r'data/Aesop_Fables.txt')
    huffman = HuffmanCode(content)
    codes = huffman.compress(compress_file=r'data/Aesop_Fables.huff')
    print 'compress done'
    decodes = huffman.decodeHuffmanFromFile(compress_file=r'data/Aesop_Fables.huff')
    print content == decodes
