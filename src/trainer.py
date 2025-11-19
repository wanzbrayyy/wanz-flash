import os
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TextDataset, 
    DataCollatorForLanguageModeling, 
    Trainer, 
    TrainingArguments
)
import config

class ModelTrainer:
    def __init__(self):
        self.model_name = config.BASE_MODEL_NAME
        self.train_file = config.TRAIN_FILE
        self.output_dir = config.MODEL_OUTPUT_DIR

    def train(self):
        print(f"Loading tokenizer and model: {self.model_name}...")
        
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(self.model_name)

        print("Preparing dataset...")
        dataset = TextDataset(
            tokenizer=tokenizer,
            file_path=self.train_file,
            block_size=config.BLOCK_SIZE
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, 
            mlm=False
        )

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,
            num_train_epochs=config.NUM_EPOCHS,
            per_device_train_batch_size=config.BATCH_SIZE,
            save_steps=500,
            save_total_limit=2,
            learning_rate=config.LEARNING_RATE,
            logging_steps=50,
            prediction_loss_only=True,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset,
        )

        print("Starting training...")
        trainer.train()
        
        print(f"Saving model to {self.output_dir}...")
        trainer.save_model(self.output_dir)
        tokenizer.save_pretrained(self.output_dir)