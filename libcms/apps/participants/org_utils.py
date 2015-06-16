def get_library(code, managed_libraries):
    library = None
    for managed_library in managed_libraries:
        if managed_library.code == code:
            library = managed_library
            break
    return library
