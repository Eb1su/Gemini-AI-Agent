from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def info_tests():
    print(get_files_info('calculator', '.'))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
    
def contents_test():
    print(get_file_content("calculator", "lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


def write_tests():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

info_tests()
contents_test()
write_tests()