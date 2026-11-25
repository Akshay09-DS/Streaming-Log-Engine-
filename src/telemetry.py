def timer(func):
    import time
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        fun = func(*args,**kwargs)
        end = time.perf_counter()
        print(f"[TIMER]: {func.__name__} executed in {end-start}")
        return fun
    return wrapper

if __name__=='__main__':
    @timer
    def table(num):
        tab = []
        for i in range(1,11):
            tab.append(num*i)
        return tab
    print(table(5))
