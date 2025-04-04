# save as evaluation/benchmark.py
import json
import time
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

class BenchmarkFramework:
    def __init__(self):
        self.results = defaultdict(dict)
        
    def add_result(self, model_name, dataset_name, metrics):
        """
        Add benchmark result for a model on a dataset
        
        Args:
            model_name: Name of the model
            dataset_name: Name of the dataset
            metrics: Dictionary of metrics (accuracy, f1, etc.)
        """
        # Add timestamp
        metrics['timestamp'] = time.time()
        self.results[model_name][dataset_name] = metrics
        
    def save_results(self, filepath='evaluation/benchmark_results.json'):
        """Save results to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filepath}")
        
    def load_results(self, filepath='evaluation/benchmark_results.json'):
        """Load results from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.results = json.load(f)
            print(f"Results loaded from {filepath}")
        except FileNotFoundError:
            print(f"No results file found at {filepath}")
            
    def visualize_results(self, metric='f1', save_path='visualization/benchmark_comparison.png'):
        """
        Visualize benchmark results for a specific metric
        
        Args:
            metric: Metric to visualize (e.g., 'f1', 'accuracy')
            save_path: Path to save the visualization
        """
        # Extract data for visualization
        models = []
        datasets = []
        values = []
        
        for model_name, model_results in self.results.items():
            for dataset_name, dataset_results in model_results.items():
                if metric in dataset_results:
                    models.append(model_name)
                    datasets.append(dataset_name)
                    values.append(dataset_results[metric])
        
        # Create DataFrame for seaborn
        import pandas as pd
        df = pd.DataFrame({
            'Model': models,
            'Dataset': datasets,
            metric.capitalize(): values
        })
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Model', y=metric.capitalize(), hue='Dataset', data=df)
        plt.title(f'Model Comparison by {metric.capitalize()} Score')
        plt.xlabel('Model')
        plt.ylabel(metric.capitalize())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        print(f"Visualization saved to {save_path}")
        
    def calculate_average_performance(self, metric='f1'):
        """
        Calculate average performance of each model across datasets
        
        Args:
            metric: Metric to use for average calculation
        
        Returns:
            Dictionary of model names to average performance
        """
        averages = {}
        
        for model_name, model_results in self.results.items():
            values = []
            for dataset_results in model_results.values():
                if metric in dataset_results:
                    values.append(dataset_results[metric])
            
            if values:
                averages[model_name] = sum(values) / len(values)
            
        return averages

# Example usage
if __name__ == "__main__":
    # Sample benchmark test
    benchmark = BenchmarkFramework()
    
    # Add some mock results
    benchmark.add_result(
        model_name="BERT-base",
        dataset_name="SQuAD",
        metrics={
            "exact_match": 80.5,
            "f1": 88.7,
            "inference_time": 0.15
        }
    )
    
    benchmark.add_result(
        model_name="LSTM-baseline",
        dataset_name="SQuAD",
        metrics={
            "exact_match": 65.3,
            "f1": 75.2,
            "inference_time": 0.08
        }
    )
    
    # Save and visualize results
    benchmark.save_results()
    benchmark.visualize_results(metric='f1')
    benchmark.visualize_results(metric='exact_match')
    
    # Calculate averages
    averages = benchmark.calculate_average_performance(metric='f1')
    print("Average F1 scores:")
    for model, avg in averages.items():
        print(f"{model}: {avg:.2f}")