import uuid


class MiniHashTable:
    # TODO DEBUG THIS
    def __init__(self, size, r):
        self.size = size
        self.r = r
        self.rand_a, self.rand_b = self.create_rand_ints()
        self.prime = 15373875993579943603
        self.slots = [None] * self.size
        self.data = [[]] * self.size

    def create_rand_ints(self):
        rand_a = []
        rand_b = []
        for _ in range(self.r):
            rand_a.append(uuid.uuid4().int & (1 << 64) - 1)
            rand_b.append(uuid.uuid4().int & (1 << 64) - 1)
        return rand_a, rand_b

    @staticmethod
    def hash_function(word, a, b, prime):
        h = (a * word + b) % prime
        return h

    def hash_signature(self, key):
        min_hashes = ""
        for permutation in range(self.r):
            a = self.rand_a[permutation]
            b = self.rand_b[permutation]
            hashes = []
            for word in key:
                hash = self.hash_function(word, a, b, self.prime)
                hashes.append(hash)

            min_hashes = min_hashes + str(min(hashes))

        return min_hashes

    def put(self, key, item):
        hash_value = self.hash_signature(key)
        index = int(hash_value) % self.size
        self.slots[index] = hash_value
        data_at_key = self.data[index].copy()
        data_at_key.append(item)
        self.data[index] = data_at_key

    def get(self, key):
        hash_value = self.hash_signature(key)
        index = int(hash_value) % self.size
        return self.data[index]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, item):
        self.put(key, item)
