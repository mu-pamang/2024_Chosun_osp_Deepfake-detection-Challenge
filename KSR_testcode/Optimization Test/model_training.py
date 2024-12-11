import copy
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

# LogLoss 계산 함수
def calculate_log_loss(predictions, labels):
    epsilon = 1e-12  # 안전 클램핑
    predictions = torch.sigmoid(predictions)  # 로짓 -> 확률 변환
    predictions = torch.clamp(predictions, epsilon, 1. - epsilon)  # 클램핑

    log_loss = -torch.mean(labels * torch.log(predictions) + (1 - labels) * torch.log(1 - predictions))
    
    # NaN 체크
    if torch.isnan(log_loss).any():
        print(f"LogLoss NaN Debug - Predictions: {predictions}, Labels: {labels}")
        return torch.tensor(float('nan')).to(labels.device)  # NaN 반환
    
    return log_loss


# 학습 함수 (LogLoss 포함)
def train_one_epoch_with_logloss(model, dataloader, criterion, optimizer, device, log_interval=100):
    model.train()  # 모델을 학습 모드로 설정
    running_loss = 0.0
    correct = 0
    total = 0
    batch_losses = []  # 배치별 손실 저장
    log_losses = []  # LogLoss 값을 위한 리스트 추가

    for batch_idx, (inputs, labels) in enumerate(dataloader):
        # 데이터 GPU로 이동
        inputs, labels = inputs.to(device), labels.to(device)
        labels = labels.unsqueeze(1).float()  # 이진 분류이므로 labels의 형태를 (batch_size, 1)로 맞춤

        optimizer.zero_grad()

        # 모델에 입력 전달
        outputs = model(inputs)

        # BCEWithLogitsLoss 계산
        loss = criterion(outputs, labels)  # 손실 계산
        loss.backward()
        optimizer.step()

        # LogLoss 계산
        log_loss = calculate_log_loss(outputs, labels)
        if torch.isnan(log_loss):
            print("NaN detected in LogLoss calculation! Skipping this batch.")
            continue  # NaN 감지 시 해당 배치 생략

        log_losses.append(log_loss.item())  # 배치별 LogLoss 저장

        # 손실 및 정확도 계산
        running_loss += loss.item() * inputs.size(0)
        batch_losses.append(loss.item())  # 배치 손실 추가
        preds_prob = torch.sigmoid(outputs)  # 시그모이드 적용하여 확률로 변환
        preds_prob = torch.clamp(preds_prob, 0.0, 1.0)  # 예측 확률 클램핑
        preds = (preds_prob >= 0.5).float()  # 예측값을 0 또는 1로 변환
        correct += (preds == labels).sum().item()
        total += labels.size(0)

        # 로그 간격마다 출력
        if (batch_idx + 1) % log_interval == 0:
            print(f'Batch [{batch_idx + 1}/{len(dataloader)}], Loss: {loss.item():.4f}, LogLoss: {log_loss.item():.4f}')

    epoch_loss = running_loss / len(dataloader.dataset)
    epoch_accuracy = 100 * correct / total
    average_log_loss = np.mean(log_losses)  # 전체 에포크에 대한 평균 LogLoss 계산
    return epoch_loss, epoch_accuracy, batch_losses, average_log_loss


# 테스트 함수 (LogLoss 포함)
def test_model_with_logloss(model, dataloader, criterion, device):
    model.eval()  # 모델을 평가 모드로 설정
    predictions = []
    true_labels = []
    test_losses = []  # 테스트 손실 저장
    log_losses = []  # 테스트 LogLoss 값 저장

    with torch.no_grad():
        for inputs, labels in dataloader:
            # 데이터 GPU로 이동
            inputs, labels = inputs.to(device), labels.to(device)
            labels = labels.unsqueeze(1).float()  # 테스트 데이터도 이진 분류에 맞게 변경

            outputs = model(inputs)
            preds_prob = torch.sigmoid(outputs)  # 시그모이드 적용 후 확률로 변환
            preds_prob = torch.clamp(preds_prob, 0.0, 1.0)  # 예측 확률 클램핑
            preds = (preds_prob >= 0.5).float()  # 0 또는 1로 변환
            predictions.append(preds)
            true_labels.append(labels)

            # 손실 계산
            loss = criterion(outputs, labels)
            test_losses.append(loss.item())

            # LogLoss 계산
            log_loss = calculate_log_loss(outputs, labels)
            if not torch.isnan(log_loss):
                log_losses.append(log_loss.item())

    predictions = torch.cat(predictions, dim=0).cpu().numpy()
    true_labels = torch.cat(true_labels, dim=0).cpu().numpy()
    avg_test_loss = np.mean(test_losses)
    avg_log_loss = np.mean(log_losses) if log_losses else float('nan')  # LogLoss가 비어있을 경우 처리
    return true_labels, predictions, avg_test_loss, avg_log_loss


# 학습 및 테스트 설정
num_epochs = 20
train_losses = []  # 에포크별 손실 저장
train_accuracies = []  # 에포크별 정확도 저장
train_log_losses = []  # 에포크별 LogLoss 저장
best_model_wts = copy.deepcopy(ensemble_model.state_dict())  # 초기 모델 가중치 저장
best_acc = 0.0  # 최적 정확도 기준 설정

for epoch in range(num_epochs):
    print(f"Epoch {epoch + 1}/{num_epochs}")

    # Train 데이터셋 학습
    train_loss, train_acc, _, avg_log_loss = train_one_epoch_with_logloss(
        ensemble_model, train_loader, criterion, optimizer, device
    )
    train_losses.append(train_loss)
    train_accuracies.append(train_acc)
    train_log_losses.append(avg_log_loss)
    print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, Train LogLoss: {avg_log_loss:.4f}")

    # 최적 모델 가중치 업데이트 (정확도가 이전보다 향상되었을 때)
    if train_acc > best_acc:
        best_acc = train_acc
        best_model_wts = copy.deepcopy(ensemble_model.state_dict())  # 최적 가중치 저장

# 최적 모델 로드
ensemble_model.load_state_dict(best_model_wts)

# 테스트 데이터셋 평가
test_true_labels, test_predictions, test_loss, test_log_loss = test_model_with_logloss(
    ensemble_model, test_loader, criterion, device
)

# 정확도 계산
test_true_labels = np.array(test_true_labels).astype(int)
test_predictions = np.array(test_predictions).astype(int)
test_acc = np.mean(test_true_labels == test_predictions) * 100
print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.4f}%, Test LogLoss: {test_log_loss:.4f}")

# 손실 및 정확도 시각화
def plot_metrics(train_losses, train_accuracies, test_loss, test_acc, train_log_losses, test_log_loss):
    epochs = range(1, len(train_losses) + 1)

    # 손실 시각화
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_losses, 'bo-', label='Train Loss')
    plt.scatter([len(epochs)], [test_loss], color='red', label='Test Loss (Final)')
    plt.title('Loss Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # 정확도 시각화
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accuracies, 'go-', label='Train Accuracy')
    plt.scatter([len(epochs)], [test_acc], color='red', label='Test Accuracy (Final)')
    plt.title('Accuracy Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # LogLoss 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(epochs, train_log_losses, 'bo-', label='Train LogLoss')
    plt.scatter([len(epochs)], [test_log_loss], color='red', label='Test LogLoss (Final)')
    plt.title('LogLoss Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('LogLoss')
    plt.legend()

    plt.tight_layout()
    plt.show()

# 결과 시각화 호출
plot_metrics(train_losses, train_accuracies, test_loss, test_acc, train_log_losses, test_log_loss)
