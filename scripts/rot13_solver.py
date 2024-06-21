def rot13_decrypt(encoded_message):
    """
    Decrypts a ROT13 encoded message.

    Args:
        encoded_message (str): The ROT13 encoded message.

    Returns:
        str: The decrypted message.
    """
    decrypted_message = []
    for char in encoded_message:
        if 'a' <= char <= 'z':
            decrypted_message.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            decrypted_message.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            decrypted_message.append(char)
    return ''.join(decrypted_message)

if __name__ == "__main__":
    # Example encoded message from the "Mod 26" challenge on picoCTF
    encoded_message = "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_uJdSftmh}"

    # Decrypt the encoded message using the rot13_decrypt function
    flag = rot13_decrypt(encoded_message)

    # Print the decrypted flag
    print(f"Decrypted flag: {flag}")
