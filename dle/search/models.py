from typing import NamedTuple
from django.db import models

# Create your models here.
class MockLabel(NamedTuple):
    manufacturer: str
    name: str
    label_text: str
