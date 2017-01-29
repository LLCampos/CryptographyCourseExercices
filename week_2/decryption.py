from Crypto.Cipher.AES import AESCipher
from binascii import unhexlify, hexlify


def get_iv_key_from_ciphertext(iv_ciphertext):
    # IV is appended to beginning of the ciphertext and is 16 bytes long.
    return iv_ciphertext[0:16], iv_ciphertext[16:]


def strxor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])


def add_n_to_binary(bin_str, n):
    hex_str = hexlify(bin_str)
    int_repr = int(hex_str, 16)

    new_int_repr = int_repr + n
    new_hex_str = hex(new_int_repr)[:-1]
    new_bin_str = unhexlify(new_hex_str[2:])
    return new_bin_str


def split_every_n_chars(string, n):
    return [string[i: i + n] for i in range(0, len(string), n)]


def cbc_decryption(key_hex, iv_ciphertext_hex):

    key = unhexlify(key_hex)
    iv_ciphertext = unhexlify(iv_ciphertext_hex)
    iv, ciphertext = get_iv_key_from_ciphertext(iv_ciphertext)

    aes_cipher = AESCipher(key)

    ciphertext_blocks = split_every_n_chars(ciphertext, 16)
    plaintext_blocks = []

    for i, block in enumerate(ciphertext_blocks):

        aes_decrypted = aes_cipher.decrypt(block)

        if i == 0:
            plaintext_block = strxor(aes_decrypted, iv_ciphertext)
        else:
            plaintext_block = strxor(aes_decrypted, ciphertext_blocks[i - 1])

        # If it is the last block, remove padding
        if i == len(ciphertext_blocks) - 1:
            padding_n = ord(plaintext_block[-1])
            plaintext_block = plaintext_block[0:(-1 * padding_n)]

        plaintext_blocks.append(plaintext_block)

    plaintext = ''.join(plaintext_blocks)
    return plaintext


def ctr_decryption(key_hex, iv_ciphertext_hex):

    key = unhexlify(key_hex)
    iv_ciphertext = unhexlify(iv_ciphertext_hex)

    aes_cipher = AESCipher(key)
    iv, ciphertext = get_iv_key_from_ciphertext(iv_ciphertext)

    ciphertext_blocks = split_every_n_chars(ciphertext, 16)
    plaintext_blocks = []

    for i, block in enumerate(ciphertext_blocks):
        block_iv = add_n_to_binary(iv, i)
        block_key = aes_cipher.encrypt(block_iv)

        plaintext_block = strxor(block_key, block)
        plaintext_blocks.append(plaintext_block)

    plaintext = ''.join(plaintext_blocks)
    return plaintext
