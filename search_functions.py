import os
import re


def extract_functions_from_cfile(file_path):
    # 定义正则表达式匹配函数定义
    # 匹配形如：返回类型 函数名(参数列表) { 或者 返回类型 函数名(参数列表);
    # 支持跨行匹配
    function_pattern = re.compile(
        r'^(.+?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*(\{|;)',
        re.MULTILINE | re.DOTALL
    )

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # 查找所有匹配的函数定义
        functions = function_pattern.findall(content)

        # 提取函数名并去重
        function_names = list(set(func[1] for func in functions))

        return function_names
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return []
    except Exception as e:
        print(f"发生错误：{e}")
        return []


def extract_functions_from_file_list(file_list=None):
    if file_list is None:
        return

    for file_name in file_list:
        funcs_ = extract_functions_from_cfile(file_name)

        if funcs_:
            print(f"文件 {file_name} 中的函数列表：")
            for func in funcs_:
                print(f"{func}")
        else:
            print(f"文件 {file_name} 中未找到任何函数。")


def find_function_definition(file_path, function_name):
    """
    在单个文件中查找函数定义。
    如果找到函数定义，返回 True；否则返回 False。
    """
    function_pattern = re.compile(
        r'\b' + re.escape(function_name) + r'\s*\([^)]*\)\s*(\{|;)',
        re.MULTILINE | re.DOTALL
    )

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # 查找函数定义
        if function_pattern.search(content):
            return True
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误：{e}")

    return False


def search_function_in_codebase(root_dir, function_name):
    """
    在代码库中递归搜索指定函数的定义。
    """
    results = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):  # 假设代码库中包含 .c 和 .h 文件
                file_path = os.path.join(root, file)
                if find_function_definition(file_path, function_name):
                    results.append(file_path)

    return results


def search_function_print_result(root_dir, function_name):
    """
    在代码库中递归搜索指定函数的定义。
    """
    results = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):  # 假设代码库中包含 .c 和 .h 文件
                file_path = os.path.join(root, file)
                if find_function_definition(file_path, function_name):
                    results.append(file_path)

    return results


def search_function(function_name=None, root_dir=None):
    """
    :param function_name: 要查找的函数名称
    :param root_dir: 代码库
    :return:
    """

    results = search_function_in_codebase(root_dir, function_name)

    if results:
        print(f"找到函数 '{function_name}' 的定义：")
        for file_path in results:
            print(file_path)
    else:
        print(f"未找到函数 '{function_name}' 的定义。")


# 示例用法
if __name__ == "__main__":
    # main()

    c_file_path = r'test.c'
    functions = extract_functions_from_cfile(c_file_path)

    if functions:
        print("找到的函数列表：")
        for func in functions:
            print(func)
    else:
        print("未找到任何函数。")

