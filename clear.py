import os
import ast


# Đọc requirements-gpu.txt
def read_requirements(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    raw_lines = []
    packages = set()
    for line in lines:
        raw_lines.append(line)
        line = line.strip()
        if line and not line.startswith("#"):
            pkg = line.split("==")[0].split(">=")[0].split("<")[0].strip()
            packages.add(pkg.lower())
    return packages, raw_lines


# Tìm tất cả import trong code
def find_imported_modules(source_dir):
    imported = set()
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imported.add(alias.name.split(".")[0].lower())
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imported.add(node.module.split(".")[0].lower())
                except Exception as e:
                    print(f"Lỗi khi đọc {path}: {e}")
    return imported


# Lọc và tạo file _clear
def create_clean_requirements(requirements_file, source_code_path, output_file):
    used_packages, original_lines = read_requirements(requirements_file)
    imports = find_imported_modules(source_code_path)

    with open(output_file, "w", encoding="utf-8") as f:
        for line in original_lines:
            line_strip = line.strip()
            if not line_strip or line_strip.startswith("#"):
                f.write(line)
                continue
            pkg = line_strip.split("==")[0].split(">=")[0].split("<")[0].strip().lower()
            if pkg in imports:
                f.write(line)

    print(f"✅ Đã tạo file '{output_file}' chứa các thư viện thực sự được sử dụng.")


# Ví dụ dùng:
requirements_path = "requirements-gpu.txt"
source_code_folder = r"C:\\Users\\Admin\\Downloads\\viet-tts\\"  # Thay bằng thư mục chứa code của bạn
output_file = "requirements-gpu_clear.txt"

create_clean_requirements(requirements_path, source_code_folder, output_file)
