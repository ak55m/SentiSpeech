# save as data/download_squad.py
from datasets import load_dataset
import json
import os

def download_squad():
    # Create data directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Download SQuAD dataset
    squad = load_dataset('rajpurkar/squad')
    
    print(f"Dataset loaded. Available splits: {squad.keys()}")
    print(f"Training examples: {len(squad['train'])}")
    print(f"Validation examples: {len(squad['validation'])}")
    
    # Print an example to understand the structure
    print("\nExample from training set:")
    example = squad['train'][0]
    for key, value in example.items():
        print(f"{key}: {value}")
    
    # Save dataset to disk for local access
    squad['train'].to_json('data/raw/squad_train.json')
    squad['validation'].to_json('data/raw/squad_validation.json')
    
    return squad

if __name__ == "__main__":
    download_squad()