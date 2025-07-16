#!/bin/bash

set -e  # Dừng script nếu có lỗi xảy ra

VENV_NAME=".venv"

echo "✅ Bắt đầu cài đặt môi trường CPU..."

# 1. Tạo virtual environment nếu chưa có
if [ ! -d "$VENV_NAME" ]; then
  echo "📦 Tạo virtual environment: $VENV_NAME"
  python3 -m venv $VENV_NAME
fi

# 2. Kích hoạt virtualenv
source $VENV_NAME/bin/activate

# 3. Cập nhật pip
echo "🔄 Cập nhật pip..."
pip install --upgrade pip

# 4. Cài đặt PyTorch bản CPU
echo "⚙️  Cài đặt PyTorch (CPU)..."
pip install torch torchvision torchaudio

# 5. Cài các thư viện trong requirements-cpu.txt
echo "📚 Cài đặt thư viện từ requirements-cpu.txt..."
pip install -r requirements-cpu.txt

pip install hyperpyyaml
pip install -U openai-whisper
pip install omegaconf
pip install conformer


echo "✅ Hoàn tất cài đặt!"
echo "👉 Kích hoạt môi trường: source $VENV_NAME/bin/activate"
