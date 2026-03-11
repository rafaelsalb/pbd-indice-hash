def prime_sum(word, bucket_count):
    p = 31
    h = 0
    for c in word:
        h = (h * p + ord(c)) % bucket_count
    return h
