import xml.etree.ElementTree as ET
import copy
from private_enums import SeqTrend

g_node_tag_cascade = ["school", "class", "student", "attr"]
g_node_attrib_cascade = ["school_name", "class_name", "name", "v"]
g_temp_xml_file = "temp_xml.xml"
g_etree_object = None


def return_node(node_):
    if not isinstance(node_, ET.Element):
        print("node is not ET.Element.")
    return node_


def enquire_and_operate_specific_node_dfs(node_, val_cascade_=None, pos_=0, offset_=1, operator_=None, args_=None):
    """
    通过深度优先，搜索节点，然后执行回调函数
    :param node_: 本级节点
    :param val_cascade_: 属性值列表，按列表逐级搜索，不含起始节点的属性值
    :param pos_:
    :param offset_: val_cascade_ 起始相对于 g_node_tag_cascade 的偏移
    :param operator_: 回调函数
    :param args_: 回调函数入口
    :return: None 未找到节点，False 输入错误或回调函数返回失败，True 回调函数执行成功，其它 回调函数返回
    """
    if not isinstance(val_cascade_, list):
        return False
    if pos_ > len(val_cascade_):
        return False
    if pos_ == len(val_cascade_):
        if operator_ is None:
            # 默认查询函数
            return True
        if args_ is None:
            return operator_(node_)
        if isinstance(args_, list):
            return operator_(node_, *args_)
        return False
    for c_ in node_:
        if c_.tag == g_node_tag_cascade[pos_ + offset_]:
            temp_attr_ = g_node_attrib_cascade[pos_ + offset_]
            if c_.get(temp_attr_, "") == val_cascade_[pos_]:
                return enquire_and_operate_specific_node_dfs(c_, val_cascade_=val_cascade_, pos_=pos_ + 1,
                                                             operator_=operator_, args_=args_)
    return None


def create_etree_object_hex_text(v_, attr_v_):
    rst_obj_ = ET.Element('p', {'v': str(attr_v_)})
    rst_obj_.text = hex(v_)
    rst_obj_.tail = '\n'
    return rst_obj_


def create_etree_object_str_text(text_, attr_v_):
    rst_obj_ = ET.Element('p', {'v': str(attr_v_)})
    rst_obj_.text = text_
    rst_obj_.tail = '\n'
    return rst_obj_


def inquire_node_multi_value_and_type(node_):
    """
    查询节点的值，节点包含多个子节点
    返回（列表, 标识)
    列表：节点元素值列表 (v="6", "7", ...)
    标识：属性 v 是否相等
    :param node_:
    :return:
    """
    attr_equal_ = None  # True: 属性 v 相等；False: 属性 v 不等，默认递增
    attr_v_ = None
    rst_value_ = []
    try:
        for c_ in node_:
            if c_.tag == "p":
                if attr_v_ is None:
                    attr_v_ = c_.attrib["v"]
                    attr_equal_ = True
                if attr_v_ != c_.attrib["v"]:
                    attr_equal_ = False
                rst_value_.append(c_.text.strip())
        if len(rst_value_) <= 1:
            attr_equal_ = None
        return rst_value_, attr_equal_
    except KeyError as e:
        # 错误的属性
        print(f"KeyError {e}!")
        return False
    except AttributeError as e:
        # node_ 不为 Element:
        print(f"AttributeError {e}!")
        return False


def set_node_multi_digital_value_v0(node_, values_):
    """
    编辑节点的值，节点包含多个子节点，v='6'，保持不变
    :param values_: 元素值列表
    :param node_:
    :return:
    """
    try:
        for c_ in node_:
            if c_.tag == "p":
                node_.remove(c_)
        for k_, v_ in enumerate(values_):
            item_ = create_etree_object_hex_text(v_, 6)
            node_.append(item_)
        return True
    except KeyError as e:
        # 错误的属性
        print(f"KeyError {e}!")
        return False
    except AttributeError as e:
        # node_ 不为 Element:
        print(f"AttributeError {e}!")
        return False


def set_node_multi_digital_value_v1(node_, values_):
    """
    编辑节点的值，节点包含多个子节点，v='6'，依次递增
    :param values_:
    :param node_:
    :return:
    """
    try:
        for c_ in node_:
            if c_.tag == "p":
                node_.remove(c_)
        for k_, v_ in enumerate(values_):
            item_ = create_etree_object_hex_text(v_, k_ + 6)
            node_.append(item_)
        return True
    except KeyError as e:
        # 错误的属性
        print(f"KeyError {e}!")
        return False
    except AttributeError as e:
        # node_ 不为 Element:
        print(f"AttributeError {e}!")
        return False


def set_node_multi_value(node_, values, attr_equal_=False):
    if not attr_equal_:
        return set_node_multi_digital_value_v1(node_, values)
    return set_node_multi_digital_value_v0(node_, values)


def inquire_node_single_digital_value(node_):
    """
    查询节点的值，返回数字（默认16进制，转换成十进制输出），
        且若节点包含多个子节点，返回第一个值
    :param node_:
    :return:
    """
    try:
        for c_ in node_:
            if c_.tag == "p":
                if c_.attrib["v"] == '6':
                    v_ = int(c_.text.strip(), 16)
                    return v_
        return False
    except KeyError as e:
        # 错误的属性
        print(f"KeyError {e}!")
        return False
    except AttributeError as e:
        # node_ 不为 Element:
        print(f"AttributeError {e}!")
        return False


def set_node_single_digital_value(node_, v_):
    """
    编辑 v="6" 节点的值，
    :param v_:
    :param node_:
    :return:
    """
    try:
        for c_ in node_:
            if c_.tag == "p":
                if c_.attrib["v"] == '6':
                    c_.text = hex(v_)
                    return True
    except KeyError as e:
        # 错误的属性
        print(f"KeyError {e}!")
        return False
    except AttributeError as e:
        # node_ 不为 Element:
        print(f"AttributeError {e}!")
        return False


def pretty_indent(elem, level=0, indent_size=2):
    """
    递归设置缩进：
    - 有子节点的元素：标签分散在多行
    - 无子节点的元素：单独成行
    - 结束标签后始终换行
    """
    indent = "\n" + " " * (level * indent_size)
    child_indent = "\n" + " " * ((level + 1) * indent_size)

    if len(elem) == 0:
        # 叶子节点：设置 tail 让下一个兄弟节点换行
        # 注意：这里不修改 elem.text，保留原有内容
        if elem.tail is None or not elem.tail.strip():
            elem.tail = indent
    else:
        # 有子节点的元素
        # 开始标签后的文本（第一个子节点前的缩进）
        if elem.text is None or not elem.text.strip():
            elem.text = child_indent

        # 处理每个子节点
        for i, child in enumerate(elem):
            pretty_indent(child, level + 1, indent_size)

            # 最后一个子节点的 tail 应该是当前层级的缩进
            # 其他子节点的 tail 是下一层级的缩进（即下一个子节点前的换行）
            if i == len(elem) - 1:
                child.tail = indent
            else:
                child.tail = child_indent


def create_etree_specific_object():
    p_text_ = "default text."
    p_obj_ = ET.Element('p', {'v': '6'})
    p_obj_.text = p_text_
    # p_obj_.tail = '\n'

    rst_obj_ = ET.Element('class', {'class_name': '0'})
    rst_obj_.append(p_obj_)
    rst_obj_.tail = '\n'
    pretty_indent(rst_obj_)
    return rst_obj_


def xml_append_specific_node(node):
    tag_obj_ = create_etree_specific_object()
    node.append(tag_obj_)
    return True


def create_etree_specific_object_v2():
    p_text_ = "default text."
    p_obj_ = ET.Element('p', {'v': '6'})
    p_obj_.text = p_text_

    rst_obj_ = ET.Element('attr', {'v': 'tel'})
    rst_obj_.append(p_obj_)
    rst_obj_.tail = '\n'
    pretty_indent(rst_obj_)
    return rst_obj_


def xml_insert_node_after(node_, atttr_name_, head_list_=None):
    """
    在指定子节点后，新增节点
    :param node_: 父节点
    :param atttr_name_: 属性名
    :param head_list_: 插入位置元素，按列表依次查询节点是否存在
    :return:
    """
    if not isinstance(head_list_, list):
        print("input error.")
        return False

    for attr_v_ in head_list_:
        c_idx = 0
        for c_ in node_:
            c_idx += 1
            if c_.attrib[atttr_name_] == attr_v_:
                tag_obj_ = create_etree_specific_object_v2()
                node_.insert(c_idx, tag_obj_)
                return True
    return False


# 通过现有文件查找节点，并保存在中，后续即可直接插入
def get_xml_etree_object_by_file():
    global g_etree_object
    tree_ = ET.parse(g_temp_xml_file)
    root_ = tree_.getroot()
    for child_ in root_:
        rst = enquire_and_operate_specific_node_dfs(child_, ["class 1", "张三", "tel"],
                                                    operator_=return_node)
        assert isinstance(rst, ET.Element)
        g_etree_object = rst
        return True
    return True


def xml_g_etree_object_after(node_, atttr_name_, head_list_=None):
    """
    在指定子节点后，新增节点
    :param node_: 父节点
    :param atttr_name_: 属性名
    :param head_list_: 插入位置元素，按列表依次查询节点是否存在
    :return:
    """
    if not isinstance(head_list_, list):
        print("input error.")
        return False

    if g_etree_object is None:
        get_xml_etree_object_by_file()

    for attr_v_ in head_list_:
        c_idx = 0
        for c_ in node_:
            c_idx += 1
            if c_.attrib[atttr_name_] == attr_v_:
                tag_obj_ = copy.deepcopy(g_etree_object)
                node_.insert(c_idx, tag_obj_)
                return True
    return False


# 0717： xml 节点值查询和更新
def xml_detect_node_c_type(node_):
    """
    检测节点子节点的 c2 是否增长/相等，仅支持节点属性 c1，子节点属性 c2
    要求子节点的 c2 严格增长或不变
    单个子节点，返回 False
    :param node_: 输入节点
    :return: 增长：True，不变：False，错误：None（非严格增长，顺序错误）
    """
    v_start_ = 6
    if not node_:
        return SeqTrend.ERROR
    if node_.tag != "attr":
        print("检测属性增长函数：不支持的场景！")
        return SeqTrend.ERROR
    v_list_ = [p_.get("v", "") for p_ in node_]
    if not v_list_:
        return SeqTrend.ERROR
    if len(v_list_) == 1:
        return SeqTrend.UNKNOWN
    v_list_ = [v_.strip() for v_ in v_list_]
    v_list_int_ = [int(v_) for v_ in v_list_]
    if v_list_int_[0] != v_start_:
        return SeqTrend.ERROR

    rst_ = SeqTrend.CONSTANT
    for v_ in v_list_int_:
        if v_start_ != v_:
            rst_ = SeqTrend.UNKNOWN
    if rst_ is SeqTrend.CONSTANT:
        return rst_
    rst_ = SeqTrend.INCREASE
    for v_ in v_list_int_:
        if v_start_ != v_:
            rst_ = SeqTrend.ERROR
        v_start_ += 1
    return rst_


def xml_get_node_str_values(node_, attr_name_, type_='str', ctype_=SeqTrend.UNKNOWN):
    """
    查询节点的值，节点为 tag 为 attr
    :param node_: 输入节点，节点为 tag 为 attr
    :param attr_name_: 节点属性值（校验使用）
    :param type_: 返回值类型
    :param ctype_: c2 是否增长，类型 SeqTrend
    :return: 查询结果
    """
    if not node_:
        return False
    if not isinstance(attr_name_, str):
        return False
    attr_v_ = node_.get("v", "")
    if attr_v_ != attr_name_:
        return None
    ctype_valid_ = False
    if (ctype_ is SeqTrend.CONSTANT) or (ctype_ is SeqTrend.INCREASE):
        ctype_valid_ = True
    c_ = 6
    res_vales_ = []
    for p_ in node_:
        str_c_ = str(c_)
        attr_v_ = p_.get("v", "")
        text_ = p_.text
        text_ = text_.strip()

        if ctype_valid_:
            if ctype_ is SeqTrend.INCREASE:
                c_ += 1
            if attr_v_ != str_c_:
                continue

        if type_ == 'int16':
            r_ = int(text_, 16)
            res_vales_.append(r_)
        elif type_ == 'int':
            r_ = int(text_)
            res_vales_.append(r_)
        else:
            res_vales_.append(text_)
    if res_vales_:
        return res_vales_
    return None


def xml_node_detect_get_str_value(node_, attr_name_):
    ctype_ = xml_detect_node_c_type(node_)
    rst_ = xml_get_node_str_values(node_, attr_name_, type_='str', ctype_=ctype_)
    return ctype_, rst_


def xml_reset_node_str_values(node_, attr_name_, value_list_=None, ctype_=SeqTrend.CONSTANT):
    """
    更新节点的值，操作时，会先清空原有子节点
    :param node_: 输入节点
    :param attr_name_: 节点属性值（校验使用）
    :param value_list_: 更新后的节点值
    :param ctype_: c2 是否增长，False: c2 = 6
    :return: 成功：True
    """
    if not node_:
        return False
    if not isinstance(attr_name_, str):
        return False
    if not isinstance(value_list_, list):
        return False
    attr_v_ = node_.get("v", "")
    if (ctype_ is not SeqTrend.CONSTANT) and (ctype_ is not SeqTrend.INCREASE):
        print(f"{attr_v_}增长类型错误！")
        ctype_ = SeqTrend.CONSTANT
    if attr_v_ != attr_name_:
        return False
    c_ = 6
    for chd_ in node_[:]:
        node_.remove(chd_)
    for v_ in value_list_:
        new_v_ = str(v_)
        new_p_ = create_etree_object_str_text(new_v_, c_)
        node_.append(new_p_)
        if ctype_ is SeqTrend.INCREASE:
            c_ += 1
    return True


def xml_get_node_attrib_and_str_values(node_, attr_name_, type_='str'):
    """
    查询节点的值，节点为 tag 为 attr
    :param node_: 输入节点，节点为 tag 为 attr
    :param attr_name_: 节点属性值（校验使用）
    :param type_: 返回值类型
    :return: 查询结果
    """
    if not node_:
        return False
    if not isinstance(attr_name_, str):
        return False
    attr_v_ = node_.get("v", "")
    if attr_v_ != attr_name_:
        return None

    attr_v_ = [p_.get("v", "") for p_ in node_]
    text_v_ = [p_.text for p_ in node_]
    attr_v_ = [v_.strip() for v_ in attr_v_]
    text_v_ = [v_.strip() for v_ in text_v_]

    if type_ == 'int16':
        text_v_ = [int(v_, 16) for v_ in text_v_]
    elif type_ == 'int':
        text_v_ = [int(v_) for v_ in text_v_]
    return attr_v_, text_v_


def xml_update_node_attrib_and_str_values(node_, attr_name_, attr_v_, text_v_):
    """
    重置节点子节点属性和内容的值
    :param node_:
    :param attr_name_:
    :param attr_v_:
    :param text_v_:
    :return:
    """
    if not node_:
        return False
    if not isinstance(attr_name_, str):
        return False
    p_attr_ = node_.get("v", "")
    if p_attr_ != attr_name_:
        return False

    if len(attr_v_) != len(text_v_):
        return False
    for chd_ in node_[:]:
        node_.remove(chd_)
    for k_ in range(len(attr_v_)):
        new_p_ = create_etree_object_str_text(text_v_[k_], attr_v_[k_])
        node_.append(new_p_)
    return True


def xml_node_append_specific_str_value_test(node_, attr_name_, attr_='6', text_=None):
    assert isinstance(text_, str)
    attr_vals_, values_ = xml_get_node_attrib_and_str_values(node_, attr_name_, type_='str')
    assert not attr_vals_
    assert not values_
    if (len(values_) == 1) and values_[0] == '0':
        values_[0] = text_
    else:
        attr_vals_.append(attr_)
        values_.append(text_)
    xml_update_node_attrib_and_str_values(node_, attr_name_, attr_vals_, values_)
    return True

