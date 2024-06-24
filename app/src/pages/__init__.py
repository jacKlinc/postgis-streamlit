from .post_gis import PostGIS
from ..types import Page

from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {"Post GIS": PostGIS}

__all__ = ["PAGE_MAP"]
