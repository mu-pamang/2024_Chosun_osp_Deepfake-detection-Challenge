import torch.nn as nn
import torch.optim as optim

# 모델 정의 (예: 앙상블 모델 사용)
model = ensemble_model  # 이미 정의된 ensemble_model을 사용

# BCEWithLogitsLoss를 사용
criterion = nn.BCEWithLogitsLoss()  # BCEWithLogitsLoss로 변경

# 옵티마이저 설정: Adam + L2 정규화
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)  # L2 정규화 추가

# 손실 함수와 옵티마이저 확인
print("Loss Function:", criterion)
print("Optimizer:", optimizer)
