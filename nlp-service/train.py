"""
Train intent classifier and save model.
Run: python train.py
"""
from app.core.classifier import train_and_save

if __name__ == "__main__":
    train_and_save()
    print("Training complete.")
