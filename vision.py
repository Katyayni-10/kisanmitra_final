"""Crop-disease image classifier (EfficientNet-B0 trained by train.py)."""
import json
import os
from functools import lru_cache
from pathlib import Path

MODEL_DIR = Path(os.environ.get("KISANMITRA_MODEL_DIR", Path(__file__).resolve().parent / "model"))
MEAN, STD = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]


def model_available() -> bool:
    return (MODEL_DIR / "model.pt").is_file() and (MODEL_DIR / "classes.json").is_file()


def parse_label(label: str):
    """'Tomato___Early_blight' -> ('Tomato', 'Early blight')"""
    crop, _, disease = label.partition("___")
    crop = crop.replace("_", " ").replace(",", "").strip()
    disease = disease.replace("_", " ").strip() or "unknown"
    return crop, disease


@lru_cache(maxsize=1)
def _load():
    import torch
    import torch.nn as nn
    from torchvision import models, transforms

    with open(MODEL_DIR / "classes.json") as f:
        classes = json.load(f)
    m = models.efficientnet_b0()
    m.classifier[1] = nn.Linear(m.classifier[1].in_features, len(classes))
    m.load_state_dict(torch.load(MODEL_DIR / "model.pt", map_location="cpu"))
    m.eval()
    tf = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224),
                             transforms.ToTensor(), transforms.Normalize(MEAN, STD)])
    return m, classes, tf


def predict(img, k: int = 3) -> dict:
    """PIL image -> {"label","crop","condition","confidence","alternatives":[(crop, condition, prob), ...]}"""
    import torch

    model, classes, tf = _load()
    with torch.no_grad():
        probs = torch.softmax(model(tf(img.convert("RGB")).unsqueeze(0)), 1)[0]
    top = torch.topk(probs, min(k, len(classes)))
    alts = []
    for p, i in zip(top.values.tolist(), top.indices.tolist()):
        c, d = parse_label(classes[i])
        alts.append((c, d, p))
    best_label = classes[top.indices[0].item()]
    crop, condition = parse_label(best_label)
    return {"label": best_label, "crop": crop, "condition": condition,
            "confidence": alts[0][2], "alternatives": alts}
