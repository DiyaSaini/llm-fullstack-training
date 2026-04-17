"""
Internal dataclasses for the Keywords service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass


@dataclass
class KeywordsInput:
    
    #Populated KeywordsInput in validate_input() and validated max_keywords. 
    #Added defensive checks to ensure input integrity before prompt construction.
    
    text: str
    max_keywords: int = 10
