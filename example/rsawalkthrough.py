import math
import sys

unencryptedMessage = "Hello World!"

p1 = 5  # prime number 1
p2 = 11  # prime number 2

t = 40  # totient. AKA (p1-1)*(p2-1)
n = 55  # n. AKA p*q - part of public key
e = 13  # e. prime number - part of public key
d = 37  # d. private key


plaintext_message_seg_length = int(math.floor(math.log(float(n), 2)))
encrypted_message_seg_length = int(math.ceil(math.log(float(n), 2)))

print("Plaintext: " + str(plaintext_message_seg_length))
print("Encrypted: " + str(encrypted_message_seg_length))
print("Original Message: " + unencryptedMessage)

# convert the message to all binary bits - padd out to make sure they all are 8 bits long for the character
binaryUnencryptedMessage = ''.join(format(ord(x), '08b') for x in unencryptedMessage)
print(binaryUnencryptedMessage)

# post pad the string to get an even number
while len(binaryUnencryptedMessage) % plaintext_message_seg_length != 0:
    binaryUnencryptedMessage += '0'

print(binaryUnencryptedMessage)

# split it up into segments of plaintext_message_seg_length
unencryptedMessageSegments = list()
for i in range(0, len(binaryUnencryptedMessage), plaintext_message_seg_length):
    unencryptedMessageSegments.append(binaryUnencryptedMessage[i: i + plaintext_message_seg_length])

print(unencryptedMessageSegments)

#encrypt each segment using RSA
encryptedMessageSegments = list()
for i in unencryptedMessageSegments:
    print("------------------")
    print(i)
    segmentInt = int(i, 2)  # converts string to int, interpreting it as in base 2
    print(str(segmentInt) + " - " + bin(segmentInt))
    encryptedSegmentInt = (segmentInt ** e) % n
    print(str(encryptedSegmentInt) + " - " + bin(encryptedSegmentInt))
    encryptedSegmentBinary = format(encryptedSegmentInt, '0' + str(encrypted_message_seg_length) + 'b')
    print(encryptedSegmentBinary)
    encryptedMessageSegments.append(encryptedSegmentBinary)


print("***********************")
print(encryptedMessageSegments)
encryptedMessageBinaryString = ''.join(encryptedMessageSegments)
print(encryptedMessageBinaryString)

encryptedMessageInt = int(encryptedMessageBinaryString, 2)
print(encryptedMessageInt)
print(bin(encryptedMessageInt))


encryptedMessage = encryptedMessageInt.to_bytes(byteorder=sys.byteorder,
                                            length=math.ceil(len(encryptedMessageBinaryString) / 8 ))
print(encryptedMessage)

# -- AT THIS POINT THE MESSAGE IS ENCRYPTED AS A BYTE ARRAY--

number = int.from_bytes(encryptedMessage, byteorder=sys.byteorder, signed=False)
print(number)

print (" ** BEGINNING DECRYPTION **")

binaryEncryptedMessage = str(bin(number))[2:]
print(binaryEncryptedMessage)

# pre pad encrypted until is appropriate length to be cut up
while len(binaryEncryptedMessage) % encrypted_message_seg_length != 0:
    binaryEncryptedMessage = '0' + binaryEncryptedMessage

# cut into decryptable segments
encryptedMessageSegments = list()
for i in range(0, len(binaryEncryptedMessage), encrypted_message_seg_length):
    encryptedMessageSegments.append(binaryEncryptedMessage[i: i + encrypted_message_seg_length])

print(encryptedMessageSegments)

unencryptedSegments = list()
for i in encryptedMessageSegments:
    print("------------")
    segmentInt = int(i, 2)  # converts string to int, interpreting it as in base 2
    print(i)
    print(str(segmentInt) + " - " + bin(segmentInt))
    unencryptedSegmentInt = int((segmentInt ** d) % n)
    print(unencryptedSegmentInt)

    # left pad with 0 to return segment to decrypted segment length
    unencryptedSegmentBinary = format(unencryptedSegmentInt, '0' + str(plaintext_message_seg_length) + 'b')
    print(unencryptedSegmentBinary)
    unencryptedSegments.append(unencryptedSegmentBinary)

print(unencryptedSegments)
joinedSegments = ''.join(unencryptedSegments)
print(joinedSegments)


letters = list()
for i in range(0, len(joinedSegments), 8):
    letters.append(joinedSegments[i: i + 8])

print(letters)

plainMessage = ""
for letter in letters:
    letterInt = int(letter, 2)
    character = chr(letterInt)
    plainMessage += character

print(plainMessage)



