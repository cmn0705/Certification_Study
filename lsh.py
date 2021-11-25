def shingleSet(text):
    import binascii
    words = text.split(" ")
    shingleSet = set()
    for i in range(0, len(words) - 2):
        shingle = words[i] + " " + words[i + 1] + " " + words[i + 2] # 3 consecutive words
        crc = binascii.crc32(shingle.encode()) & 0xffffffff # Hash the shingle to a 32-bit integer
        shingleSet.add(crc)
    return shingleSet

def generateID(text): #numHashes, coeffA, coeffB have to be fixed for all documents in a table, check LSH.ipynb to see how I generate them
    numHashes = 5
    coeffA = [637991790, 2183903381, 4160526327, 1561289052, 2253366173]
    coeffB = [1603279463, 1892597895, 2920260016, 4231771987, 3149290334]
    nextPrime = 4294967311 # The prime number above 'maxShingleID'
    signature = []
    thisShingleSet=shingleSet(text)
    
    for i in range(0, numHashes): #creating each elemment of a signature
        minHashCode = nextPrime + 1
        for shingle in thisShingleSet:
            hashCode = (coeffA[i] * shingle + coeffB[i]) % nextPrime 
            if hashCode < minHashCode:# Track the lowest hash code seen
                minHashCode = hashCode
        signature.append(minHashCode)
    return ''.join(str(item) for item in signature)