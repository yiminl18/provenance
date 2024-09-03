# I'll modify the `remove_intervals` function to achieve the desired result where adjacent intervals are not merged.
def remove_intervals(full_intervals: list[list[int]], remove_intervals: list[list[int]]):
    full_set = convert_intervals_to_set(full_intervals)
    remove_set = convert_intervals_to_set(remove_intervals)
    result_set = full_set - remove_set
    result_intervals = convert_set_to_intervals_without_merging(result_set, full_intervals)
    return result_intervals

def convert_set_to_intervals_without_merging(result_set, original_intervals):
    if not result_set:
        return []
    
    intervals = []
    for original_interval in original_intervals:
        start, end = original_interval
        current_interval = []
        for i in range(start, end + 1):
            if i in result_set:
                current_interval.append(i)
            else:
                if current_interval:
                    intervals.append([current_interval[0], current_interval[-1]])
                    current_interval = []
        if current_interval:
            intervals.append([current_interval[0], current_interval[-1]])
    
    return intervals

def convert_intervals_to_set(intervals: list[list[int]]):
    result_set = set()
    
    for interval in intervals:
        start, end = interval
        result_set.update(range(start, end + 1))
    
    return result_set

# Test the function with the provided example
full_intervals = [[1,2], [3,6], [11, 20]]
remove_intervals = [[4, 5], [13,17]]
print(remove_intervals(full_intervals, remove_intervals))