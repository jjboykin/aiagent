# tests.py

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():

    '''
    print("Test 1: get_files_info('calculator', '.')")
    print(get_files_info("calculator", "."))

    print("\nTest 2: get_files_info('calculator', 'pkg')")
    print(get_files_info("calculator", "pkg"))

    print("\nTest 3: get_files_info('calculator', '/bin')")
    print(get_files_info("calculator", "/bin"))  # Expected to return an error string

    print("\nTest 4: get_files_info('calculator', '../')")
    print(get_files_info("calculator", "../"))  # Expected to return an error string
    '''

    # print(get_file_content("calculator", "lorem.txt"))

    '''
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat")) # Expected to return an error string)
    '''

    '''
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    '''

    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py")) # (this should return an error)
    print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)

if __name__ == "__main__":
    main()
