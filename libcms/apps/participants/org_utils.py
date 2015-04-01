def get_library(code, managed_libraries):
    library = None
    for managed_library in managed_libraries:
        if managed_library.library.code == code and managed_library.is_active:
            library = managed_library.library
    return library
