CUDA_VISIBLE_DEVICES=1 python3 -m torch.distributed.launch --master_port 13517 --nproc_per_node=1 \
       pdcner_trainer.py --do_train --do_eval --do_predict --evaluate_during_training \
                  --data_dir="data/dataset/NER/nky-pig" \
                  --output_dir="data/result/NER/nky-pig/pdcncercrf_20240511-2" \
                  --config_name="data/berts/bert/config.json" \
                  --model_name_or_path="data/berts/bert/pytorch_model.bin" \
                  --vocab_file="data/berts/bert/vocab.txt" \
                  --word_vocab_file="data/vocab/tencent_vocab.txt" \
                  --max_scan_num=1000000 \
                  --max_word_num=5 \
                  --label_file="data/dataset/NER/nky-pig/labels.txt" \
                  --word_embedding="data/embedding/word_embedding.txt" \
                  --saved_embedding_dir="data/dataset/NER/nky-pig" \
                  --model_type="WCBertCRF_Token" \
                  --seed=106524 \
                  --per_gpu_train_batch_size=4 \
                  --per_gpu_eval_batch_size=16 \
                  --learning_rate=1e-5 \
                  --max_steps=-1 \
                  --max_seq_length=256 \
                  --num_train_epochs=20 \
                  --warmup_steps=190 \
                  --save_steps=600 \
                  --logging_steps=100
