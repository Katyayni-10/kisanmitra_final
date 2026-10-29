"""
Train a plant-disease classifier (EfficientNet-B0, transfer learning).
"""
import argparse
import json
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, models, transforms

MEAN, STD = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]


def get_transforms():
    train_tf = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.6, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(25),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD),
    ])
    return train_tf, eval_tf


def run_epoch(model, loader, criterion, device, optimizer=None):
    training = optimizer is not None
    model.train(training)
    total_loss, correct, n = 0.0, 0, 0
    start = time.time()
    with torch.set_grad_enabled(training):
        for b, (x, y) in enumerate(loader, 1):
            x, y = x.to(device), y.to(device)
            out = model(x)
            loss = criterion(out, y)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * x.size(0)
            correct += (out.argmax(1) == y).sum().item()
            n += x.size(0)
            if training and (b % 10 == 0 or b == len(loader)):
                el = time.time() - start
                print(f"    batch {b}/{len(loader)}  loss {total_loss / n:.3f}  acc {correct / n:.3f}  "
                      f"{el:.0f}s elapsed, ~{el / b * (len(loader) - b):.0f}s left in this epoch", flush=True)
    return total_loss / n, correct / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="model")
    ap.add_argument("--epochs-head", type=int, default=3)
    ap.add_argument("--epochs-ft", type=int, default=7)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--val-split", type=float, default=0.15)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--max-per-class", type=int, default=0,
                    help="use at most N images per class (0 = use all). Smaller = faster and lighter")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", device)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    train_tf, eval_tf = get_transforms()
    full_train = datasets.ImageFolder(args.data, transform=train_tf)
    full_eval = datasets.ImageFolder(args.data, transform=eval_tf)
    classes = full_train.classes
    print(f"{len(full_train)} images, {len(classes)} classes")

    g = torch.Generator().manual_seed(42)
    perm = torch.randperm(len(full_train), generator=g).tolist()
    if args.max_per_class > 0:
        counts, kept = {}, []
        for i in perm:
            c = full_train.targets[i]
            if counts.get(c, 0) < args.max_per_class:
                counts[c] = counts.get(c, 0) + 1
                kept.append(i)
        perm = kept
        print(f"Using {len(perm)} images (max {args.max_per_class} per class)")
    n_val = int(len(perm) * args.val_split)
    val_idx, train_idx = perm[:n_val], perm[n_val:]
    train_loader = DataLoader(Subset(full_train, train_idx), batch_size=args.batch_size,
                              shuffle=True, num_workers=args.workers, pin_memory=(device == "cuda"))
    val_loader = DataLoader(Subset(full_eval, val_idx), batch_size=args.batch_size,
                            shuffle=False, num_workers=args.workers, pin_memory=(device == "cuda"))

    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(classes))
    model = model.to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)

    best_acc = 0.0

    def fit(epochs, optimizer, tag):
        nonlocal best_acc
        for ep in range(1, epochs + 1):
            tl, ta = run_epoch(model, train_loader, criterion, device, optimizer)
            vl, va = run_epoch(model, val_loader, criterion, device)
            print(f"[{tag}] epoch {ep}/{epochs}  train {ta:.3f}  val {va:.3f}  val_loss {vl:.3f}")
            if va > best_acc:
                best_acc = va
                torch.save(model.state_dict(), out_dir / "model.pt")

    for p in model.features.parameters():
        p.requires_grad = False
    fit(args.epochs_head, torch.optim.AdamW(model.classifier.parameters(), lr=1e-3), "head")

    for p in model.features.parameters():
        p.requires_grad = True
    fit(args.epochs_ft, torch.optim.AdamW(model.parameters(), lr=1e-4), "finetune")

    model.load_state_dict(torch.load(out_dir / "model.pt", map_location=device))
    model.eval()
    preds, labels = [], []
    with torch.no_grad():
        for x, y in val_loader:
            preds += model(x.to(device)).argmax(1).cpu().tolist()
            labels += y.tolist()

    report = classification_report(labels, preds, target_names=classes, output_dict=True, zero_division=0)
    cm = confusion_matrix(labels, preds)
    plt.figure(figsize=(14, 12))
    plt.imshow(cm, cmap="Blues")
    plt.title(f"Confusion matrix (val acc {best_acc:.3f})")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.savefig(out_dir / "confusion_matrix.png", dpi=120)

    json.dump(classes, open(out_dir / "classes.json", "w"), indent=2)
    json.dump({"val_accuracy": best_acc,
               "macro_f1": report["macro avg"]["f1-score"],
               "per_class": {c: report[c] for c in classes}},
              open(out_dir / "metrics.json", "w"), indent=2)
    print(f"Done. Best val accuracy: {best_acc:.4f}. Files saved in {out_dir}/")


if __name__ == "__main__":
    main()