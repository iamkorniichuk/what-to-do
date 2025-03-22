from django.db.models.signals import pre_save
from django.dispatch import receiver

from sentence_transformers import SentenceTransformer
import numpy as np

from .models import Activity


model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


@receiver(pre_save, sender=Activity)
def set_activity_embedding(sender, instance, **kwargs):
    # TODO: Avoid when name and description aren't changed
    text = f"{instance.name} {instance.description}"
    embedding = model.encode(text)

    binary_embedding = np.array(embedding, dtype=np.float32).tobytes()
    instance.embedding = binary_embedding
