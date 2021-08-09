import os

def solution_export(solution, file_name):
    """
        @ Brief: Export .txt file contains the process of solving the problem
        @ Param:    
                    solution: The process of solving the problem
                    file_name: Name of the .txt fie
    """
    path = os.path.dirname(os.path.abspath(__file__))
    solution_folder_path = os.path.abspath(os.path.join(path, os.pardir, os.pardir, 'Solution'))
    solution_path = os.path.join(solution_folder_path, file_name)
    with open(solution_path, "w", encoding='utf-8') as text_file:
        text_file.write(solution)