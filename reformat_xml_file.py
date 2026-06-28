
FIRST_LINE = r"<?xml version='1.0' encoding='utf-8'?>"
XML_TAG_CASCADE = ["<ParaTable", "<school", "<class", "<student", "<attr", "<p",
                   "</ParaTable", "</school", "</class", "</student", "</attr", "</p",]
XML_TAG_TAB_NUM_MAPPING = {"<ParaTable": 0, "<school": 1, "<class": 2, "<student": 3, "<attr": 4, "<p": 5,
                           "</ParaTable": 0, "</school": 1, "</class": 2, "</student": 3, "</attr": 4, "</p": 5}


def reformat_xml_file(src_f_, dst_f_):
    l_id_ = 0
    with open(src_f_, 'r', encoding='utf-8') as src_fp_:
        with open(dst_f_, 'w', encoding='utf-8') as dst_fp_:
            lines_ = src_fp_.readlines()
            for l_ in lines_:
                if l_id_ == 0:
                    dst_fp_.write(FIRST_LINE + '\n')
                    l_id_ += 1
                    continue
                line_ = l_.strip()
                for t_ in XML_TAG_CASCADE:
                    if t_ in line_:
                        line_ = '\t' * XML_TAG_TAB_NUM_MAPPING[t_] + line_
                        break
                dst_fp_.write(line_ + '\n')
                l_id_ += 1
    return True
