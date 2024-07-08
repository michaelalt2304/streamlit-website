
def order_by_tstamp(arr, order_ls):
    ARR_CP = arr[:]
    def sort_fun(el):
        return order_ls[ARR_CP.index(el)]
    arr.sort(key=sort_fun)
    return arr
arr =      ["list", "to", "swap", "around", "this", "time"]
order_ls = [4,      5,    0,      3,        1,      2     ]
order_by_tstamp(arr, order_ls)
print(arr)