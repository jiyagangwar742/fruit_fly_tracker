
# ============================================================================
# FILE: storage/file_storage.py
# Handles saving and loading experiments from JSON files
# ============================================================================

import json
from pathlib import Path
import config
from models.experiment import Experiment

class ExperimentStorage:
    """
    Handles persistent storage of experiments to/from JSON files.
    """
    
    def __init__(self, storage_dir=None):
        """
        Initialize storage handler.
        
        Args:
            storage_dir: Directory to store experiments (uses config default if None)
        """
        self.storage_dir = storage_dir or config.EXPERIMENTS_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save_experiment(self, experiment):
        """
        Save experiment to JSON file.
        
        Args:
            experiment: Experiment object to save
            
        Returns:
            Path to saved file
        """
        filename = f"{experiment.experiment_id}.json"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(experiment.to_dict(), f, indent=2)
        
        return filepath
    
    def load_experiment(self, experiment_id):
        """
        Load experiment from JSON file.
        
        Args:
            experiment_id: ID of experiment to load
            
        Returns:
            Experiment object, or None if not found
        """
        filename = f"{experiment_id}.json"
        filepath = self.storage_dir / filename
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return Experiment.from_dict(data)
    
    def list_all_experiments(self):
        """
        List all experiment IDs.
        
        Returns:
            List of experiment IDs
        """
        json_files = self.storage_dir.glob("*.json")
        return [f.stem for f in json_files]
    
    def load_all_experiments(self):
        """
        Load all experiments.
        
        Returns:
            List of Experiment objects
        """
        experiment_ids = self.list_all_experiments()
        experiments = []
        
        for exp_id in experiment_ids:
            exp = self.load_experiment(exp_id)
            if exp:
                experiments.append(exp)
        
        return experiments
    
    def delete_experiment(self, experiment_id):
        """
        Delete an experiment file.
        
        Args:
            experiment_id: ID of experiment to delete
            
        Returns:
            True if deleted, False if not found
        """
        filename = f"{experiment_id}.json"
        filepath = self.storage_dir / filename
        
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    def search_experiments(self, query, field="name"):
        """
        Search experiments by field value.
        
        Args:
            query: Search term
            field: Field to search in ("name", "notes", etc.)
            
        Returns:
            List of matching Experiment objects
        """
        all_experiments = self.load_all_experiments()
        matches = []
        
        query_lower = query.lower()
        for exp in all_experiments:
            field_value = getattr(exp, field, "")
            if query_lower in str(field_value).lower():
                matches.append(exp)
        
        return matches
