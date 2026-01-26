# import timeit

# # Define a large list for a meaningful comparison
# N = 1_000_000
# numbers = list(range(N))

# # --- Methods to Test ---

# # 1. List Comprehension (Generally the fastest)
# def use_comprehension():
#     return [x * 2 for x in numbers]

# # 2. Map with Lambda (Slower due to function call overhead)
# def use_map_lambda():
#     # Note: list() is required to force map() to calculate all values
#     return list(map(lambda x: x * 2, numbers))

# # 3. For Loop (Slowest due to method lookup and append overhead)
# def use_for_loop():
#     doubled = []
#     for x in numbers:
#         doubled.append(x * 2)
#     return doubled

# # 4. Map with Named Function (Can sometimes be faster than map with lambda)
# def doubler(x):
#     return x * 2

# def use_map_named_function():
#     return list(map(doubler, numbers))

# # Time the list comprehension
# time_comp = timeit.timeit(use_comprehension, number=100)
# print(f"List Comprehension:     {time_comp:.4f} seconds")

# # Time the map with lambda
# time_map_l = timeit.timeit(use_map_lambda, number=100)
# print(f"Map (with lambda):      {time_map_l:.4f} seconds")

# # Time the map with named function
# time_map_named = timeit.timeit(use_map_named_function, number=100)
# print(f"Map (named function):   {time_map_named:.4f} seconds")

# # Time the for loop
# time_loop = timeit.timeit(use_for_loop, number=100)
# print(f"Traditional For Loop:   {time_loop:.4f} seconds")





# import timeit

# N = 1_000_000

# setup_code = f"""
# numbers = list(range({N}))
# def doubler(x):
#     return x * 2
# """

# # 1. List Comprehension (Direct statement in optimal context)
# time_comp = timeit.timeit(
#     stmt="[x * 2 for x in numbers]",
#     setup=setup_code,
#     number=100
# )
# print(f"List Comprehension:     {time_comp:.4f} seconds")

# # 2. Traditional For Loop (Direct statement)
# # This forces the loop to run as a single statement, avoiding the function call overhead.
# time_loop = timeit.timeit(
#     stmt="""
# doubled = []
# for x in numbers:
#     doubled.append(x * 2)
#     """,
#     setup=setup_code,
#     number=100
# )
# print(f"Traditional For Loop:   {time_loop:.4f} seconds")

# # 3. Map with Lambda (Direct statement)
# time_map_l = timeit.timeit(
#     stmt="list(map(lambda x: x * 2, numbers))",
#     setup=setup_code,
#     number=100
# )
# print(f"Map (with lambda):      {time_map_l:.4f} seconds")

# # 4. Map with Named Function (Direct statement)
# time_map_named = timeit.timeit(
#     stmt="list(map(doubler, numbers))",
#     setup=setup_code,
#     number=100
# )
# print(f"Map (named function):   {time_map_named:.4f} seconds")





# in list


def stable_partition(lst, predicate):
    seen = set()
    result = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            result.append(x)


lst = [5, 2, 8, 1, 9, 3]
print(stable_partition(lst, lambda x: x % 2 == 0))
