import keys


def encode_keys():
    if keys.encoded is False:
        for key in keys.TWITTER_KEYS.itervalues():
            key.encode('rot13')
        keys.encoded = True
