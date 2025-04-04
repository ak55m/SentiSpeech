# save as main.py
import os
import subprocess
import argparse

def setup_environment():
    """Set up project environment"""
    # Create directories
    dirs = [
        'data/raw',
        'data/processed',
        'models',
        'evaluation',
        'visualization',
        'notebooks'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    # Install dependencies if not already installed
    try:
        import torch
        import transformers
        import datasets
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import scikit_learn
        print("All dependencies already installed")
    except ImportError:
        print("Installing dependencies...")
        subprocess.run(["pip", "install", "torch", "transformers", "datasets", "pandas", "numpy", 
                       "matplotlib", "seaborn", "scikit-learn"])
        print("Dependencies installed")

def run_pipeline(args):
    """Run the complete pipeline or specific steps"""
    if args.all or args.download:
        print("\n=== Downloading SQuAD Dataset ===")
        from data.download_squad import download_squad
        download_squad()
    
    if args.all or args.preprocess:
        print("\n=== Preprocessing Dataset ===")
        from data.preprocess_squad import preprocess_squad
        for model_type in ["bert", "gpt", "lstm"]:
            print(f"\nPreprocessing for {model_type}...")
            preprocess_squad(model_type)
    
    if args.all or args.benchmark:
        print("\n=== Setting up Benchmarking Framework ===")
        from evaluation.benchmark import BenchmarkFramework
        benchmark = BenchmarkFramework()
        
        # Add mock results for demonstration
        benchmark.add_result(
            model_name="BERT-base (Mock)",
            dataset_name="SQuAD",
            metrics={
                "exact_match": 80.5,
                "f1": 88.7,
                "inference_time": 0.15
            }
        )
        
        benchmark.save_results()
        print("Benchmark framework set up with sample data")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NLP Model Benchmarking Project")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    parser.add_argument("--download", action="store_true", help="Download dataset")
    parser.add_argument("--preprocess", action="store_true", help="Preprocess data")
    parser.add_argument("--benchmark", action="store_true", help="Set up benchmark framework")
    
    args = parser.parse_args()
    
    # If no arguments provided, run all steps
    if not (args.all or args.download or args.preprocess or args.benchmark):
        args.all = True
    
    # Setup environment
    setup_environment()
    
    # Run pipeline
    run_pipeline(args)
    
    print("\n=== Pipeline completed successfully ===")