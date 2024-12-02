import torch
import torch.nn.functional as F
from torchvision import transforms
import matplotlib.pyplot as plt

def train_one_epoch(model, dataloader, criterion, optimizer, device, log_interval=100):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1).to(device)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1).to(device)

    for i, (inputs, labels) in enumerate(dataloader):
        inputs = inputs.to(device)
        labels = labels.to(device).unsqueeze(1).float()

        if i == 0:
            for k in range(min(5, inputs.size(0))):
                img = (inputs[k] * std + mean).clamp(0, 1).cpu()
                plt.imshow(img.permute(1, 2, 0).numpy())
                plt.show()

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        preds = (torch.sigmoid(outputs) >= 0.5).float()
        running_loss += loss.item() * inputs.size(0)
        correct += preds.eq(labels.view(-1, 1)).sum().item()
        total += labels.size(0)

        if (i + 1) % log_interval == 0:
            print(f"Batch {i+1}/{len(dataloader)} - Loss: {loss.item():.4f}")

    return running_loss / len(dataloader.dataset), 100.0 * correct / total


def evaluate(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device).unsqueeze(1).float()
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # 이진화
            preds = (torch.sigmoid(outputs) >= 0.5).float()  # Sigmoid 후 이진화
            running_loss += loss.item() * inputs.size(0)
            correct += preds.eq(labels).sum().item()
            total += labels.size(0)

    return running_loss / len(dataloader.dataset), 100 * correct / total
