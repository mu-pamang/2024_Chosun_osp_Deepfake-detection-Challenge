import torch
import torch.nn as nn
import timm

# EfficientNet-B0 모델 (num_classes=1로 설정)
class EfficientNetB0(nn.Module):
    def __init__(self, num_classes=1, dropout_prob=0.3):
        super(EfficientNetB0, self).__init__()
        self.model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=num_classes)
        in_features = self.model.get_classifier().in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(dropout_prob),
            nn.Linear(in_features, num_classes)  # 출력 크기 1로 설정
        )

    def forward(self, x):
        return self.model(x)

# ConvNeXt Tiny 모델 (num_classes=1로 설정)
class ConvNeXtTiny(nn.Module):
    def __init__(self, num_classes=1, dropout_prob=0.3):
        super(ConvNeXtTiny, self).__init__()
        self.model = timm.create_model('convnext_tiny', pretrained=True, num_classes=num_classes)
        in_features = self.model.get_classifier().in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(dropout_prob),
            nn.Linear(in_features, num_classes)  # 출력 크기 1로 설정
        )

    def forward(self, x):
        return self.model(x)

# 앙상블 모델
class EnsembleModel(nn.Module):
    def __init__(self, model1, model2):
        super(EnsembleModel, self).__init__()
        self.model1 = model1
        self.model2 = model2

    def forward(self, x):
        output1 = self.model1(x)
        output2 = self.model2(x)
        output = (output1 + output2) / 2  # 평균 앙상블
        return output  # BCEWithLogitsLoss는 로짓을 그대로 사용

# 모델 인스턴스 생성
effnet_model = EfficientNetB0(num_classes=1, dropout_prob=0.3)
convnext_model = ConvNeXtTiny(num_classes=1, dropout_prob=0.3)
ensemble_model = EnsembleModel(effnet_model, convnext_model)

# 모델 요약 출력
from torchsummary import summary
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ensemble_model = ensemble_model.to(device)

print("\nEnsemble Model Summary:")
summary(ensemble_model, input_size=(3, 224, 224), device=device.type)

