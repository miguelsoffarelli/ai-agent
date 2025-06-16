from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file

# get_files_info tests

# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))

# # Example of what's mentioned in get_files_info.py line 8. 
# # If lines 11 and 12 were to be removed, this test would return the directory contents even when it's outside the working directory
# print(get_files_info("calculator", "../calculator1")) 
#--------------------------------------------------------------

# # get_file_content tests

# print(get_file_contents("calculator", "main.py"))
# print(get_file_contents("calculator", "pkg/calculator.py"))
# print(get_file_contents("calculator", "/bin/cat"))
#--------------------------------------------------------------

# write_file tests

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
