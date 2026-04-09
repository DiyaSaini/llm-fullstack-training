"""
Routers package.

All routers are imported here so main.py can do:
    from app.api.v1.routers import summarize, classify, keywords, ...
"""

from app.api.v1.routers import (
    classify,
    keywords,
    paraphrase,
    qa,
    sentiment,
    summarize,
    translate,
)

__all__ = [
    "summarize",
    "classify",
    "keywords",
    "sentiment",
    "qa",
    "paraphrase",
    "translate",
]
