def array_rotation_detector(arr1: list[int],
                            arr2: list[int])-> bool:
    if arr1 == arr2:
        True
    if len(arr1) != len(arr2):
        return False
    if arr1 is None and arr2 is None:
        return True

    n: int = len(arr1)
    for i in range(1, n):
        if arr1[-i:] + arr1[:-i] == arr2:
            return True
    return False


print(f"True: {array_rotation_detector([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])}")
print(f"True: {array_rotation_detector([1, 2, 3, 4, 5], [4, 5, 1, 2, 3])}")
print(f"True: {array_rotation_detector([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])}")
print(f"True: {array_rotation_detector([1, 2, 3, 4, 5], [2, 3, 4, 5, 1])}")
print(f"False: {array_rotation_detector([1, 2, 3], [1, 3, 2])}")
print(f"False: {array_rotation_detector([1, 2, 3], [1, 2])}")
print(f"True: {array_rotation_detector([], [])}")
print(f"True: {array_rotation_detector([1, 1, 1], [1, 1, 1])}")
