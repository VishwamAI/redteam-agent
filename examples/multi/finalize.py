def generate_password(length=10):
    ALPHABET = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789-_+=.'
    )
    return ''.join(random.choices(ALPHABET, k=length))
