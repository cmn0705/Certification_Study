def shar256(text):
    from hashlib import sha256
    h = sha256()
    h.update(b'text')
    return h.hexdigest()