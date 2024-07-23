# pdcner
 A Pig Disease Chinese Named Entity Recognition (PDCNER) model

 #    A Pig Disease Chinese Named Entity Recognition (PDCNER) model

The model integrates external lexicon knowledge of pig disease by employing Lexicon-enhanced BERT and enhance feature representation by incorporating contrastive learning.

https://github.com/tufeifei923/pdcner

# Requirement

* Python 3.8.0
* apex 0.1
* Transformer 3.4.0
* Numpy 1.19.2
* Packaging 23.2
* skicit-learn 0.23.2
* torch 1.6.0+cu101
* torchvision  0.7.0+cu101
* tqdm 4.66.2
* multiprocess 0.70.10
* tensorflow-gpu 2.0.0
* tensorboardX 2.1
* seqeval 1.2.1

# Input Format

CoNLL format (prefer BIOES tag scheme), with each character its label for one line. Sentences are splited with a null line.

```cpp
猪 B-disease
蓝 M-disease
耳 M-disease
病 E-disease
曾 O
称 O
为 O
“ O
神 B-disease
秘 M-disease
猪 M-disease
病 E-disease
” O
、 O
“ O

体 O
温 O
一 O
般 O
正 O
常 O
， O
如 O
有 O
继 B-symptom
发 I-symptom
感 I-symptom
染 E-symptom
则 O
```

# Chinese BERT，Chinese Word Embedding, and Checkpoints

### Chinese BERT

Chinese BERT: https://huggingface.co/bert-base-chinese/tree/main [!--https://cdn.huggingface.co/bert-base-chinese-pytorch_model.bin--](!--https://cdn.huggingface.co/bert-base-chinese-pytorch_model.bin--)

### Chinese word embedding:

Word Embedding: https://ai.tencent.com/ailab/nlp/en/data/tencent-ailab-embedding-zh-d200-v0.2.0.tar.gz



# Directory Structure of data

* berts
  * bert
    * config.json
    * vocab.txt,the vocab of pig disease word embedding table
    * pytorch_model.bin
* dataset, you can download from [here](https://drive.google.com/file/d/1QUn7ssSah2KbFQkWZEL5LWENpyqT2TM0/view?usp=sharing)
  * NER
    * nky-pig   
* vocab
  * tencent_vocab.txt, the vocab of pre-trained word embedding table, download from [here](https://drive.google.com/file/d/1UmtbCSPVrXBX_y4KcovCknJFu9bXXp12/view?usp=sharing).
* embedding
  * word_embedding.txt
* result
  * NER
    * nky-pig  
* log

# Run

* 1.split samples by percent radio ,`python3 split_txt.py`
* 2.convert .txt file to .json file, `python3 txt_json.py`
* 3.run the shell us single thread, `sh run_nky_pig.sh`
* 4.run the shell us multi thread, `sh run_nky_pig_multi.sh`



# Cite

```

```

