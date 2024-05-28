# -*- coding: utf-8 -*-
import numpy as np
from seqeval.metrics import f1_score, precision_score, recall_score, accuracy_score
import os


# 获取labels.txt中的type
# BIOES标注
# BMEO标注
def get_label_type(label_txt_path):
    type_list = []
    with open(label_txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line != "O":
                type = line.replace("B-", "").replace("M-", "").replace("E-", "").replace("I-", "")
                if type not in type_list:
                    type_list.append(type)
    return type_list


def write_text(result_txt_path, need_labels, need_metrics):
    with open(result_txt_path, 'w', encoding='utf-8') as f:
        for l, m in zip(need_labels, need_metrics):
            f.write("%s--->\t%s\t\n" % (l, m))


def seq_f1_with_mask(description, global_step, output_dir, label_file, all_true_labels, all_pred_labels, all_label_mask,
                     label_vocab):
    print("lable_file:{}".format(label_file))
    """
    For Chinese, since label is given to each character, do not exists subtoken,
    so we can evaluate in character level directly, extra processing

    Args:
        all_true_labels: true label ids
        all_pred_labels: predict label ids
        all_label_mask: the valid of each position
        label_vocab: from id to labels
    """
    assert len(all_true_labels) == len(all_pred_labels), (len(all_true_labels), len(all_pred_labels))
    assert len(all_true_labels) == len(all_label_mask), (len(all_true_labels), len(all_label_mask))

    true_labels = []
    pred_labels = []

    sample_num = len(all_true_labels)

    for i in range(sample_num):
        tmp_true = []
        tmp_pred = []

        assert len(all_true_labels[i]) == len(all_pred_labels[i]), (len(all_true_labels[i]), len(all_pred_labels[i]))
        assert len(all_true_labels[i]) == len(all_label_mask[i]), (len(all_true_labels[i]), len(all_label_mask[i]))

        real_seq_length = np.sum(all_label_mask[i])
        for j in range(1, real_seq_length - 1):  # remove the label of [CLS] and [SEP]
            if all_label_mask[i][j] == 1:
                if label_vocab.convert_id_to_item(all_pred_labels[i][j]) is not None:
                    tmp_true.append(label_vocab.convert_id_to_item(all_true_labels[i][j]).replace("M-", "I-"))
                    tmp_pred.append(label_vocab.convert_id_to_item(all_pred_labels[i][j]).replace("M-", "I-"))

        true_labels.append(tmp_true)
        pred_labels.append(tmp_pred)

    # 整体
    acc = accuracy_score(true_labels, pred_labels)
    p = precision_score(true_labels, pred_labels)
    r = recall_score(true_labels, pred_labels)
    f1 = f1_score(true_labels, pred_labels)

    # 按标签种类
    # BMEO
    # BIOES
    label_type_list = get_label_type(label_file)

    need_labels = []
    need_metrics = []

    # 原来的all计算，把标签匹配结果为空的也包含进去了，现在要排除掉，只计算有结果的标签
    new_all_true_labels = []
    new_all_pred_labels = []
    #  循环各个标签的结果
    for label_type in label_type_list:
        need_labels.append(label_type)
        need_true_labels = []
        need_pred_labels = []
        for index in range(len(true_labels)):
            tmp_true_list = true_labels[index]
            tmp_pred_list = pred_labels[index]
            need_true_list = []
            need_pred_list = []
            for index2 in range(len(tmp_true_list)):
                tmp_true = tmp_true_list[index2]
                tmp_pred = tmp_pred_list[index2]
                tem_type = tmp_true.replace("B-", "").replace("M-", "").replace("E-", "").replace("I-", "")
                if label_type == tem_type:
                    need_true_list.append(tmp_true)
                    need_pred_list.append(tmp_pred)
            if len(need_true_list) > 0:
                need_true_labels.append(need_true_list)
                need_pred_labels.append(need_pred_list)
        print("label is {}".format(label_type))
        result_str = ""
        if len(need_true_labels) > 0:
            tmp_acc = accuracy_score(need_true_labels, need_pred_labels)
            tmp_p = precision_score(need_true_labels, need_pred_labels)
            tmp_r = recall_score(need_true_labels, need_pred_labels)
            tmp_f1 = f1_score(need_true_labels, need_pred_labels)
            result_str = "Result: acc: %.4f, p: %.4f, r: %.4f, f1: %.4f\n" % (tmp_acc, tmp_p, tmp_r, tmp_f1)
            # print("Result: acc: %.4f, p: %.4f, r: %.4f, f1: %.4f\n" %
            #       (tmp_acc, tmp_p, tmp_r, tmp_f1))
            new_all_true_labels += need_true_labels
            new_all_pred_labels += need_pred_labels
        else:
            # print("No Result")
            result_str = "No Result\n"
        if description == "Test":
            print(result_str)
        need_metrics.append(result_str)
    # 旧的整体的结果
    need_labels.append("old all")
    result_str = "Result: acc: %.4f, p: %.4f, r: %.4f, f1: %.4f\n" % (acc, p, r, f1)
    need_metrics.append(result_str)
    # 新的整体的结果
    new_all_acc = accuracy_score(new_all_true_labels, new_all_pred_labels)
    new_all_p = precision_score(new_all_true_labels, new_all_pred_labels)
    new_all_r = recall_score(new_all_true_labels, new_all_pred_labels)
    new_all_f1 = f1_score(new_all_true_labels, new_all_pred_labels)
    need_labels.append("new all")
    result_str = "Result: acc: %.4f, p: %.4f, r: %.4f, f1: %.4f\n" % (new_all_acc, new_all_p, new_all_r, new_all_f1)
    need_metrics.append(result_str)

    if description == "Test":
        if not os.path.exists(output_dir):
            os.mkdirs(output_dir)
        file_path = os.path.join(output_dir, "{}-{}-{}.txt".format("Label-Metrics", description, str(global_step)))
        write_text(file_path, need_labels, need_metrics)

    return acc, p, r, f1, true_labels, pred_labels
