tuple = (1,2,3,4,5)
tuple = tuple[:3] + tuple[4:]
print(tuple)
tuple = tuple[:0]
print(tuple)
print(len(tuple))
print(not tuple)

distances = {}
stateOne = (5, 17, 8 ,24, 42, 88, 19, 11)
for corner in stateOne:
    distances[corner - 3] = corner
sorted = [value for (key, value) in sorted(distances.items())]
print(sorted)
