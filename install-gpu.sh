#!/bin/bash

set -e  # Dừng ngay khi có lỗi

VENV_NAME=".venv"

echo "✅ Bắt đầu cài đặt môi trường GPU..."

# 1. Tạo virtual environment nếu chưa có
if [ ! -d "$VENV_NAME" ]; then
  echo "📦 Tạo virtual environment: $VENV_NAME"
  python3 -m venv $VENV_NAME
fi

# 2. Kích hoạt virtualenv
source $VENV_NAME/bin/activate

# 3. Cập nhật pip
echo "🔄 Đang cập nhật pip..."
pip install --upgrade pip

# 4. Cài đặt PyTorch GPU (CUDA 11.8)
echo "⚙️  Cài đặt PyTorch + CUDA 11.8..."
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118

# 5. Kiểm tra torch đã cài
echo "🧪 Kiểm tra torch..."
python -c "import torch; print('✅ Torch version:', torch.__version__)"


# 7. Cài đặt các thư viện phụ thuộc còn lại
echo "📚 Cài đặt thư viện trong requirements-gpu.txt..."
pip install -r requirements-gpu.txt

pip install hyperpyyaml
pip install -U openai-whisper
pip install omegaconf
pip install conformer

pip install loguru


git clone https://github.com/duyvo26/Vinorm
cd Vinorm
pip install .


echo ""
echo "✅ Hoàn tất cài đặt môi trường GPU!"
echo "👉 Để kích hoạt môi trường: source $VENV_NAME/bin/activate"
