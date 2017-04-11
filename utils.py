# -*- coding: utf-8 -*-

import numpy as np
from babelApi import BabelApi
import json
import sys
from tqdm import tqdm
import math
from termcolor import colored

def base29encode(number):
    if number < 0:
        raise ValueError('number must be positive')

    alphabet, base29 = ['abcdefghijklmnopqrstuvwxyz ,.', '']
    j = 0
    while number:
        j += 1
        number, i = divmod(number, 29)
        base29 = alphabet[int(i)] + base29
    if j < 2:
        base29 = "a" * (2 - j) + base29
    return base29


def base29decode(number):

    alphabet = 'abcdefghijklmnopqrstuvwxyz ,.'
    base10 = np.uint16(0)
    i = 0
    while number:
        base10 += np.uint16(alphabet.find(number[0])) * np.uint16(len(alphabet)) ** np.uint16(1 - i)
        i += 1
        number = number[1:]
    return base10

def calculateFileSize(path):
    try:
        f = open(path, 'r')
        metadata = json.load(f)
    except Exception as e:
        return None
    f.close()
    size = 0
    for elem in metadata:
        size += elem['len'] / 2
    return size

def readFile(path, offset, length):
    ba = BabelApi()
    f = open(path, "r")
    chunkOffset = [offset / 1600, int(math.ceil(((float(length) * 2.0) - (3200.0 - ((float(offset) * 2.0) % 3200.0))) 
                                      / 3200.0)) + 1]
    try:
        total_metadata = json.load(f)
    except:
        return None
    metadata = total_metadata[chunkOffset[0] : chunkOffset[1] + chunkOffset[0]]
    print ("Offset is {0} , length is {1} , and we are reading on metdata block {2} to {3}. File size is {4}. Length of metadat is {5}. We have {6} metadat blocks".format(offset, length, chunkOffset[0], chunkOffset[0] + chunkOffset[1], calculateFileSize(path), len(metadata), len(total_metadata)))
    f.close()
    text = ''
    if len(metadata) == 1:
        text = ba.lookup(metadata[0])[(offset % 1600) * 2 : (offset % 1600) * 2 + length * 2]
    else:
        for i, elem in enumerate(tqdm(metadata)):
            if i == 0:
                text = ba.lookup(elem)[(offset % 1600) * 2:]
            elif i == len(metadata) - 1:
                _ = ba.lookup(elem)[:(length * 2) - len(text)]
                text += _
            else:
                _ = ba.lookup(elem)
                text += _
    chunkSize = 2
    final = np.ndarray((len(text) / chunkSize, ), dtype="uint8")
    for chunk in tqdm(xrange(0, len(text), chunkSize)):
        final[chunk / chunkSize] = base29decode(text[chunk:chunk + chunkSize])
    if length != len(final):
        print colored('----------------------\nWe were supposed to read {0} bytes, and we returned {1} bytes'.format(length, len(final)), 'red')
    return final.tobytes()

def writeFile(path, offset, data):
    if offset != 0:
        print colored('I need to take care of this', 'red')
        raise Exception('I really need to take care of writing with offset')
    content = bytearray(data)
    text = ''
    for elem in tqdm(content):
        text += base29encode(elem)
    f = open(path, 'w')
    chunkSize = 3200
    jsonInfos = []
    ba = BabelApi()
    for chunk in tqdm(xrange(0, len(text), chunkSize)):
        jsonInfos.append(ba.search(text[chunk : chunk + chunkSize]))
    json.dump(jsonInfos, f)
    return len(data)
