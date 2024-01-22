def xor_encrypt(text):
    text = bytearray(text.encode("latin-1"))
    xor_string = "?|/?*" # fbxfiletokens.h
    last = 0x7f
    for i in range(len(text)):
        text[i] ^= last ^ ord(xor_string[i % len(xor_string)])
        last = text[i]
    
    return text.decode("latin-1")

def xor_decrypt(text):
    text = bytearray(text.encode("latin-1"))
    xor_string = "?|/?*" # fbxfiletokens.h
    last = 0x7f
    for i in range(len(text)):
        new_last = text[i]
        text[i] ^= last ^ ord(xor_string[i % len(xor_string)])
        last = new_last
    
    return text.decode("latin-1")

# test decrypt
# you can copy this string from the fbx explorer in autodesk fbx converter
print(xor_decrypt("0-p;<2a|n-`u)u+ru30)pn9"))

# test encrypt
# the sample decrypt code uses scanf %s, so don't use spaces in the password
print(xor_encrypt("part-1/2-irisctf{i<3fbx"))