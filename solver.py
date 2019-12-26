from grid import Grid

cache = dict()


def memoize(func):

    def memoized_func(*args):
        global cache
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


def possible_slice_fits_current_slice(current_slice, possible_slice):
    for current_value, possible_value in zip(current_slice, possible_slice):
        if current_value != possible_value and current_value != 0:
            if current_value == -1 and possible_value == 1:
                return False
            if current_value == 1:
                return False

    return True


def generate_all_possible_slices_generator(constrains, slice):
    if len(constrains) == 0:
        yield tuple(0 for i in range(len(slice)))
    else:
        packed_length = sum(constrains) + len(constrains) - 1
        for start_index in range(0, len(slice) - packed_length + 1):
            start_of_slice = [0 for i in range(constrains[0] + start_index)]
            for i in range(constrains[0]):
                start_of_slice[start_index + i] = 1

            if possible_slice_fits_current_slice(slice, start_of_slice):
                if len(start_of_slice) == len(slice):
                    if possible_slice_fits_current_slice(slice, start_of_slice):
                        yield tuple(start_of_slice)
                else:
                    for end_of_slice in generate_all_possible_slices(constrains[1:], slice[len(start_of_slice) + 1:]):
                        possible_slice = tuple(start_of_slice) + (0, ) + end_of_slice
                        if possible_slice_fits_current_slice(slice, possible_slice):
                            yield possible_slice


@memoize
def generate_all_possible_slices_memoized(constraints, slice):
    return tuple(generate_all_possible_slices_generator(constraints, slice))


def generate_all_possible_slices(constraints, slice):
    if sum(1 for i in slice if i != 0) <= 2:
        return generate_all_possible_slices_memoized(constraints, slice)
    else:
        return tuple(generate_all_possible_slices_generator(constraints, slice))


def make_deductions(constrains, slice):
    filled = list(0 for i in range(len(slice)))
    empty = list(0 for i in range(len(slice)))
    slice_count = 0
    for possible_slice in generate_all_possible_slices(constrains, slice):
        slice_count += 1
        for i, possible_value in enumerate(possible_slice):
            if possible_value == 1:
                filled[i] += 1
            else:
                empty[i] += 1

    new_slice = list(0 for i in range(len(slice)))
    for i in range(len(slice)):
        if filled[i] == slice_count:
            new_slice[i] = 1
        elif empty[i] == slice_count:
            new_slice[i] = -1

    if all(old == new for old, new in zip(slice, new_slice)):
        return None
    else:
        return tuple(new_slice)


def solve(problem, debug_print = False):
    cache.clear()

    grid = Grid.from_problem(problem)
    grid.debug_print = True
    finished = False
    while not finished:
        at_least_one_change = False
        for x in range(grid.width):
            solved_slice = make_deductions(problem[0][x], grid.get_column(x))
            if solved_slice is not None:
                at_least_one_change = True
                grid.apply_column(x, solved_slice)

        for y in range(grid.height):
            solved_slice = make_deductions(problem[1][y], grid.get_row(y))
            if solved_slice is not None:
                at_least_one_change = True
                grid.apply_row(y, solved_slice)

        if debug_print:
            print(grid)

        if not at_least_one_change:
            if not grid.is_solved():
                print("Not solved :'(")
            finished = True

    grid.debug_print = False
    return grid



