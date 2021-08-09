import os

def solution_export(solution, file_name):
    # Xuất ra file.txt quá trình giải bài toán
    # solution quá trình giải bài toán (string)
    # file_name: tên của file txt
    path = os.path.dirname(os.path.abspath(__file__))
    solution_folder_path = os.path.abspath(os.path.join(path, os.pardir, os.pardir, 'Solution'))
    solution_path = os.path.join(solution_folder_path, file_name)
    with open(solution_path, "w", encoding='utf-8') as text_file:
        text_file.write(solution)