from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch
import os
import wandb

result_dir="/raid/telugu_pretrain_results"

run = wandb.init(project="Telugu_PreTrain", dir=result_dir, name=result_dir)

#if os.environ["LOCAL_RANK"] == 0:
#    run = wandb.init(
#        project="Telugu_PreTrain",
#        dir=result_dir, 
#        name=result_dir,
#    )

df_train = load_dataset("parquet", data_files="/raid/final_dataset/Train_Final.parquet")["train"]
df_test = load_dataset("parquet", data_files="/raid/final_dataset/Telugu_test.parquet")["train"]

if os.environ["LOCAL_RANK"] == 0:
    print(df_train)
    print(df_test)

model = AutoModelForCausalLM.from_pretrained("/raid/final_model/telugu_test_results_5", attn_implementation = "flash_attention_2", torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained("/raid/final_model/telugu_test_results_5")

training_args = TrainingArguments(
    output_dir=result_dir,
    overwrite_output_dir=True,

    num_train_epochs=10,       ### Keep as it is
    logging_steps=100,
    learning_rate=5e-4,

    bf16=True,

    do_train=True,
    do_eval=True,

    per_device_train_batch_size=14,
    per_device_eval_batch_size =14,

    gradient_accumulation_steps = 2,

    save_steps=1500,
    save_total_limit=-1,

    lr_scheduler_type = "cosine",
    warmup_steps = 3000,

    max_grad_norm = 1,

    optim='adamw_hf',
    adam_epsilon = 5e-5,
    adam_beta2 = 0.94,

    eval_strategy="steps",
    eval_steps=1500,

    use_cpu=False,
    ddp_find_unused_parameters=False,

    report_to="wandb",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=df_train,
    eval_dataset=df_test,
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()

if os.environ["LOCAL_RANK"] == 0:
    trainer.save_model("/raid/final_model_r0/" + result_dir.split("/")[-1])
    tokenizer.save_pretrained("/raid/final_model_r0/" + result_dir.split("/")[-1])


trainer.save_model("/raid/final_model/" + result_dir.split("/")[-1])
tokenizer.save_pretrained("/raid/final_model/" + result_dir.split("/")[-1])
