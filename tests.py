from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def info_tests():
    test1 = get_files_info('calculator', '.')
    print(test1)

    test2 = get_files_info("calculator", "pkg")
    print(test2)

    test3 = get_files_info("calculator", "/bin")
    print(test3)

    test4 = get_files_info("calculator", "../")
    print(test4)
    
def contents_test():
    print(get_file_content("calculator", "lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


contents_test()