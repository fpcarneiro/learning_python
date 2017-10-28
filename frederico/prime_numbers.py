def prime_numbers(n):
    l = [2] + list(range(3, n + 1, 2))
    removed = set((range(4, n + 1, 2)))
    limit = n // 2
    for i in l:
        if i == 2: continue
        if i > limit: break
        to_remove = set(range(2 * i, n + 1, i)) - removed
        if not to_remove: break
        removed = removed | to_remove
        [l.remove(r) for r in to_remove if r in l]
    return l


def call_prime(*nums):
    for n in nums:
        l = prime_numbers(n)
        print("%s : %s (%s)" % (n, l, len(l)))