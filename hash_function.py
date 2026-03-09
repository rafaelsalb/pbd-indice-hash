def prime_sum(word, bucket_count):
    return sum(ord(c) for c in word) % bucket_count
