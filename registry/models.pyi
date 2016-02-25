from typing import Tuple
from django.db import models

class Hospital(models.Model):
    def get_location(self) -> str: ...
    def get_coordinates(self) -> Tuple[float, float]: ...