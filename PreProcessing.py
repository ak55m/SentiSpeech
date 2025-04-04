# save as data/preprocess_squad.py
import json
import os
import pandas as pd
import numpy as np
from datasets import load_from_disk, Dataset
import torch
from transformers import BertTokenizer, AutoTokenizer

def preprocess_squad(model_type="bert"):
    """
    Preprocess SQuAD dataset for different model types
    
    Args:
        model_type: Type of model ("bert", "gpt", "lstm")
    
    Returns:
        Processed datasets
    """
    # Load dataset
    try:
        with open('data/raw/squad_train.json', 'r') as f:
            train_data = json.load(f)
        with open('data/raw/squad_validation.json', 'r') as f:
            val_data = json.load(f)
        
        train_dataset = Dataset.from_dict(train_data)
        val_dataset = Dataset.from_dict(val_data)
    except:
        # If local files don't exist, download from Hugging Face
        from datasets import load_dataset
        dataset = load_dataset('rajpurkar/squad')
        train_dataset = dataset['train']
        val_dataset = dataset['validation']
    
    # Create output directory
    os.makedirs(f'data/processed/{model_type}', exist_ok=True)
    
    # Apply different preprocessing based on model type
    if model_type == "bert":
        return preprocess_for_bert(train_dataset, val_dataset)
    elif model_type == "gpt":
        return preprocess_for_gpt(train_dataset, val_dataset)
    elif model_type == "lstm":
        return preprocess_for_lstm(train_dataset, val_dataset)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

def preprocess_for_bert(train_dataset, val_dataset):
    """Preprocess for BERT-based models"""
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    def preprocess_function(examples):
        questions = [q.strip() for q in examples["question"]]
        contexts = [c.strip() for c in examples["context"]]
        
        # Tokenize inputs
        inputs = tokenizer(
            questions,
            contexts,
            max_length=384,
            truncation="only_second",
            stride=128,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length",
        )
        
        # Get answer positions
        offset_mapping = inputs.pop("offset_mapping")
        sample_map = inputs.pop("overflow_to_sample_mapping")
        
        start_positions = []
        end_positions = []
        
        for i, offset in enumerate(offset_mapping):
            sample_idx = sample_map[i]
            answer = examples["answers"][sample_idx]
            start_char = answer["answer_start"][0] if len(answer["answer_start"]) > 0 else 0
            end_char = start_char + len(answer["text"][0]) if len(answer["text"]) > 0 else 0
            
            # Find token positions that correspond to the answer
            token_start_index = 0
            while token_start_index < len(offset) and offset[token_start_index][0] <= start_char:
                token_start_index += 1
            token_start_index -= 1
            
            token_end_index = token_start_index
            while token_end_index < len(offset) and offset[token_end_index][1] <= end_char:
                token_end_index += 1
            token_end_index -= 1
            
            # If answer is out of bounds or truncated
            if token_start_index >= 384 or token_end_index >= 384:
                start_positions.append(0)
                end_positions.append(0)
            else:
                start_positions.append(token_start_index)
                end_positions.append(token_end_index)
        
        inputs["start_positions"] = start_positions
        inputs["end_positions"] = end_positions
        return inputs
    
    # Apply preprocessing
    train_processed = train_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=train_dataset.column_names,
    )
    
    val_processed = val_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=val_dataset.column_names,
    )
    
    # Save processed datasets
    train_processed.save_to_disk('data/processed/bert/train')
    val_processed.save_to_disk('data/processed/bert/validation')
    
    print(f"BERT preprocessing complete. Examples: {len(train_processed)}")
    return train_processed, val_processed

def preprocess_for_gpt(train_dataset, val_dataset):
    """Preprocess for GPT-based models"""
    tokenizer = AutoTokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token
    
    def preprocess_function(examples):
        # Format for GPT: "Context: {context} Question: {question} Answer:"
        texts = [
            f"Context: {context} Question: {question} Answer: {answer['text'][0] if len(answer['text']) > 0 else 'No answer'}"
            for context, question, answer in zip(examples["context"], examples["question"], examples["answers"])
        ]
        
        # Tokenize
        encodings = tokenizer(
            texts,
            truncation=True,
            max_length=512,
            padding="max_length",
            return_tensors="pt"
        )
        
        return encodings
    
    # Apply preprocessing
    train_processed = train_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=train_dataset.column_names,
    )
    
    val_processed = val_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=val_dataset.column_names,
    )
    
    # Save processed datasets
    train_processed.save_to_disk('data/processed/gpt/train')
    val_processed.save_to_disk('data/processed/gpt/validation')
    
    print(f"GPT preprocessing complete. Examples: {len(train_processed)}")
    return train_processed, val_processed

def preprocess_for_lstm(train_dataset, val_dataset):
    """Preprocess for LSTM-based models"""
    # For LSTM, we'll convert text to indices and create embeddings
    # This is a simplified version - in practice, you'd build a vocabulary
    
    def preprocess_function(examples):
        # Extract features - simplified for this example
        features = {
            "context": examples["context"],
            "question": examples["question"],
            "answer_text": [answer["text"][0] if len(answer["text"]) > 0 else "" for answer in examples["answers"]],
            "answer_start": [answer["answer_start"][0] if len(answer["answer_start"]) > 0 else -1 for answer in examples["answers"]]
        }
        
        return features
    
    # Apply preprocessing
    train_processed = train_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=["id", "title"],
    )
    
    val_processed = val_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=["id", "title"],
    )
    
    # Save processed datasets
    train_processed.to_pandas().to_csv('data/processed/lstm/train.csv', index=False)
    val_processed.to_pandas().to_csv('data/processed/lstm/validation.csv', index=False)
    
    print(f"LSTM preprocessing complete. Examples: {len(train_processed)}")
    return train_processed, val_processed

if __name__ == "__main__":
    for model_type in ["bert", "gpt", "lstm"]:
        print(f"\nPreprocessing for {model_type}...")
        preprocess_squad(model_type)