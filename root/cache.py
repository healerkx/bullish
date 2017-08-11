
class MemoryStorage:
    memory_storage = dict()

    def get_cached_value(self, options, args):
        key = "-".join(args)
        if key in self.memory_storage:
            return self.memory_storage[key]
        return None
    
    def set_cached_value(self, options, args, value):
        key = "-".join(args)
        self.memory_storage[key] = value

# Global
default_memory_storage = MemoryStorage()


class FileStorage:
    def get_cached_value(self, options, args):
        
        return None

    def set_cached_value(self, options, args, value):
        pass


def get_storage(storage):
    if isinstance(storage, str):
        if storage == 'memory':
            global default_memory_storage
            return default_memory_storage
    else:
        return storage

#
def cache(**options):
    def outer_func(func):
        def inner_func(*args):
            storage = 'memory'
            if 'storage' in options:
                storage = options['storage']
            
            storage_obj = get_storage(storage)

            cached_value = storage_obj.get_cached_value(options, args)
            if cached_value is not None:
                return cached_value

            ret_value = func(*args)
            if ret_value is not None:
                storage_obj.set_cached_value(options, args, ret_value)

            return ret_value
        return inner_func
    return outer_func


@cache(storage="memory")
def f(a, b):
    return a + b

@cache(storage="file", path="/")
def f2(a, b):
    return a + b


if False:
    print(default_memory_storage.memory_storage)
    print(f("111", "22"))
    print(default_memory_storage.memory_storage)
    print(f("111", "22"))
    print(default_memory_storage.memory_storage)
    print(f("111", "223"))
    print(default_memory_storage.memory_storage)
