import xml.etree.ElementTree as ET
import pandas as pd
import copy
from utils import xml_detect_node_c_type, xml_get_node_str_values
from private_enums import SeqTrend

g_node_attributes = ["Table + Node Name", "c2 trends"]
g_nodes_attributes_vals = {}
g_node_attributes_num = len(g_node_attributes) - 1


def xml_file_global_detect_nodes(file_):
    try:
        tree = ET.parse(file_)
        root = tree.getroot()

        for cell_ in root:
            for msg_ in cell_:
                for node_ in msg_:
                    for p_ in node_:
                        msg_name_ = msg_.get("class_name", "")
                        node_name_ = p_.get("v", "")
                        name_ = msg_name_ + '+' + node_name_
                        ctype_ = xml_detect_node_c_type(p_)
                        values_ = xml_get_node_str_values(p_, attr_name_=node_name_, type_='str', ctype_=ctype_)
                        if len(values_) == 1:
                            ctype_ = SeqTrend.UNKNOWN
                        if name_ not in g_nodes_attributes_vals.keys():
                            g_nodes_attributes_vals[name_] = ["None" for _ in range(g_node_attributes_num)]

                        ctype_str_ = str(ctype_)
                        if g_nodes_attributes_vals[name_][0] != 'error':
                            if g_nodes_attributes_vals[name_][0] == 'None':
                                g_nodes_attributes_vals[name_][0] = ctype_str_
                            elif g_nodes_attributes_vals[name_][0] != ctype_str_:
                                g_nodes_attributes_vals[name_][0] = 'error'

    except ET.ParseError as e:
        msg = str(e).lower()
        if "mismatched tag" in msg:
            print("错误: 标签不匹配")
        elif "not well-formed" in msg:
            print("错误: XML 格式不合法")
        elif "undefined entity" in msg:
            print("错误: 未定义的实体引用")
        else:
            print(f"XML 解析错误: {e}")
        return None

    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        print(f"文件访问错误 [{type(e).__name__}]: {e}")
        return None

    except Exception as e:
        # 兜底捕获
        print(f"未知错误 [{type(e).__name__}]: {e}")
        return None

    else:
        # 解析成功，执行后续操作
        pass
        # print("解析成功")
    return True


def xml_files_global_detect_nodes(in_files_, out_file_):
    """
    标题列表 g_node_attributes
    数据列表（每个子列表是一条记录）g_nodes_attributes_vals i.e. attrib_values_list
    创建 DataFrame，用 columns 参数指定列
    保存为 CSV：encoding='utf-8-sig'
    :param in_files_:
    :param out_file_:
    :return:
    """
    global g_nodes_attributes_vals
    g_nodes_attributes_vals = {}
    for file in in_files_:
        xml_file_global_detect_nodes(file)
    attrib_values_list = [[k_, *v_] for k_, v_ in g_nodes_attributes_vals.items()]
    # 创建 DataFrame，用 columns 参数指定列名
    df = pd.DataFrame(attrib_values_list, columns=g_node_attributes)
    df.to_csv(out_file_, index=False, encoding='utf-8-sig')
    return True


if __name__ == "__main__":
    xml_files = ["cfg.xml"]
    output_file = r"output.csv"
    xml_files_global_detect_nodes(xml_files, output_file)

