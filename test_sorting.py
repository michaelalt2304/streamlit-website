
# def order_by_tstamp(arr, order_ls):
#     ARR_CP = arr[:]
#     def sort_fun(el):
#         return order_ls[ARR_CP.index(el)]
#     arr.sort(key=sort_fun)
#     return arr
# arr =      ["list", "to", "swap", "around", "this", "time"]
# order_ls = [4,      5,    0,      3,        1,      2     ]
# order_by_tstamp(arr, order_ls)
# print(arr)

def strip_chars(start: str, chrs_to_rem = [',', '\\', '"', '\'']):
    for ch in chrs_to_rem:
        start = start.replace(ch, '')
    return start

# print('<',strip_chars("''''''''"),'>', sep = '')

ILLEGAL_STRING_CHARS = [',', '\\', '"', '\'', ';']

print(' '.join(ILLEGAL_STRING_CHARS))