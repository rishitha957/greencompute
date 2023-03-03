import ast
import os
from pathlib import Path
from visitors import *
from pymeasure import EnergyProfiler

def clone_repo(repo_url):
    clone_path  = "./tmp/" 
    for f in os.scandir(clone_path):
        if not f.path.endswith("md") and f.path.split("/")[-1] != repo_url.split("/")[-1]:
            print("Cloning repository: "+f.path)
            clone = "git clone "+repo_url+".git" 
            # os.system("sshpass -p your_password ssh user_name@your_localhost")
            os.chdir(clone_path) # Specifying the path where the cloned project needs to be copied
            os.system(clone) # Cloning
        else:
            print("Repository already cloned!")

    
def parse_repo(repo_url):
    clone_repo(repo_url)
    repo_dir = "./tmp/"+repo_url.split("/")[-1]
    pyfile_list = get_subdir_filepath(repo_dir)
    for file in pyfile_list:
        parse_pyfile(file.__str__())
    return

def get_subdir_filepath(repo_dir):
    result = list(Path("./tmp/").rglob("*.py"))
    return result

def parse_pyfile(pyfile_path):
    if not pyfile_path:
        return

    with open(pyfile_path, 'r') as fp:
        data = fp.readlines()
    data = ''.join(data)
    tree = ast.parse(data)
    code_components = get_code_components_from_tree(tree)
    # print(ast.dump(tree))

    # exec(compile(tree, filename="p23", mode="exec"))

def get_code_components_from_tree(tree):
    # for node in ast.walk(tree):
    #     print(node.__str__(),ast.unparse(node))
    cv = ClassVisitor()
    cv.visit(tree)
    class_map = cv.class_map
    # print(class_map)
    func_map = cv.func_def_map
    func_call_map = cv.func_call_map
    fv = FuncVisitor()
    fv.visit(tree)
    func_names_1 = fv._func_names
    func_map_1 = fv.func_map
    # print(func_names_1)
    functions_list = [f for f in func_names_1 if f not in func_map]
    f_map = {}
    # print(func_map)
    for f in functions_list:
        api_name = fv._name_api_map[f]
        # print(f,api_name)
        f_map[api_name] = func_map_1[api_name]
    sv = StatementVisitor()
    sv.visit(tree)
    stmt_map = sv.statement_map
    print(class_map)
    print("-"*30)
    print(f_map)
    print("-"*30)
    print(stmt_map)
    print("-"*30)
    ep = EnergyProfiler()
    for key,val in stmt_map.items():
        ep.measure_energy_consumption(val)

