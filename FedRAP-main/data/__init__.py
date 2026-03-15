"""
Data processing module for FedRAP fitness recommendation system
"""
from .fitness_data_loader import load_fitness_data, create_fitness_plan
from .fitness_data_generator import FitnessDataGenerator

__all__ = ['load_fitness_data', 'create_fitness_plan', 'FitnessDataGenerator']
