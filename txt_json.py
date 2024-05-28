import json
import os


current_path = os.getcwd()
dir_name_array = ["nky-chicken", "nky-chickenpig", "nky-pig"]
percent_array = [1, 10, 30]
for dir_name in dir_name_array:
    for percent in percent_array:
        text_dir_path = os.path.join(current_path, "data", "dataset", "NER", dir_name,"percent_{}".format(percent))
        print(text_dir_path)
        input_text_path = os.path.join(text_dir_path, "all.txt")
        output_json_path = os.path.join(text_dir_path, "all.json")
        train_json_path = os.path.join(text_dir_path, "train.json")
        dev_json_path = os.path.join(text_dir_path, "dev.json")
        test_json_path = os.path.join(text_dir_path, "test.json")
        output_labels_path = os.path.join(text_dir_path, "labels.txt")
        with open(input_text_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        label_list = []
        data = []
        sentence = {'text': [], 'label': []}

        for line in lines:
            line = line.strip()
            # 判断是不是段落
            if line:
                # 不是O
                if ' ' in line:
                    word, label = line.split(' ')
                    sentence['text'].append(word)
                    sentence['label'].append(label)
                    if label not in label_list:
                        label_list.append(label)
                # O
                else:
                    word = line
                    sentence['text'].append(word)
                    sentence['label'].append('O')  # 默认标签为 'O'
                    if "O" not in label_list:
                        label_list.append(label)
            # 段落结束
            else:
                if sentence['text']:
                    data.append(sentence)
                    sentence = {'text': [], 'label': []}

        if sentence['text']:
            data.append(sentence)

        # 生成labels.txt
        print("生成labels.txt")
        with open(output_labels_path, 'w', encoding='utf-8') as labels_file:
            str = '\n'
            labels_file.write(str.join(label_list))


        # 生成完整的json，按照7:2:1比例分割训练，验证，测试json
        count = len(data)
        train_count = int(count * 7 / 10)
        dev_count = int(count * 2 / 10)
        test_count = count - train_count - dev_count
        print("生成all.json")
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            for sentence in data:
                json.dump(sentence, json_file, ensure_ascii=False)
                json_file.write('\n')
        print("生成train.json")
        with open(train_json_path, 'w', encoding='utf-8') as json_file:
            for sentence in data[:train_count]:
                json.dump(sentence, json_file, ensure_ascii=False)
                json_file.write('\n')
        print("生成dev.json")
        with open(dev_json_path, 'w', encoding='utf-8') as json_file:
            for sentence in data[train_count:train_count+dev_count]:
                json.dump(sentence, json_file, ensure_ascii=False)
                json_file.write('\n')
        print("生成test.json")
        with open(test_json_path, 'w', encoding='utf-8') as json_file:
            for sentence in data[train_count+dev_count:]:
                json.dump(sentence, json_file, ensure_ascii=False)
                json_file.write('\n')
