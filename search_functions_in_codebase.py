import os
import re

def find_function_definition(file_path, function_name):
    """
    在单个文件中查找函数定义。
    如果找到函数定义，返回 True；否则返回 False。
    """
    # 定义正则表达式匹配函数定义，支持跨行和换行的形参列表
    function_pattern = re.compile(
        r'\b' + re.escape(function_name) + r'\s*\([^)]*\)\s*(\{|;)', 
        re.MULTILINE | re.DOTALL
    )
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找函数定义
        if function_pattern.search(content):
            return True
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误：{e}")
    
    return False

def search_functions_in_codebase(root_dir, function_names):
    """
    在代码库中递归搜索多个函数的定义。
    """
    results = {func: [] for func in function_names}  # 初始化结果字典
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):  # 假设代码库中包含 .c 和 .h 文件
                file_path = os.path.join(root, file)
                for function_name in function_names:
                    if find_function_definition(file_path, function_name):
                        results[function_name].append(file_path)
    
    return results

def search_functions_main_fun(function_names=None, root_dir=None):
    if (function_names is None) or (root_dir is None):
        return
    
    function_names = [name.strip() for name in function_names]  # 去除多余的空格
    
    results = search_functions_in_codebase(root_dir, function_names)
    
    for function_name, file_paths in results.items():
        if file_paths:
            print(f"找到函数 '{function_name}' 的定义：")
            for file_path in file_paths:
                print(file_path)
        else:
            print(f"未找到函数 '{function_name}' 的定义。")

if __name__ == "__main__":
    search_functions_main_fun()

    