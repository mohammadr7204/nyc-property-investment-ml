"""
NYC Property Investment ML System
A comprehensive system for analyzing NYC property investments using real data and machine learning.
"""

__version__ = "1.0.0"
__author__ = "Mohammad R"
__description__ = "AI-powered NYC property investment analysis system"

from .analyzer import NYCPropertyInvestmentAnalyzer
from .data_pipeline import NYCPropertyDataPipeline, PropertyData
from .ml_model import NYCRevenuePredictor

__all__ = [
    'NYCPropertyInvestmentAnalyzer',
    'NYCPropertyDataPipeline',
    'PropertyData',
    'NYCRevenuePredictor'
]
