import os
import struct

# ================== НАСТРОЙКИ ==================
INCLUDE_SUBFOLDERS = False
SHOW_EXTENSIONS    = False
SHOW_FULL_PATH     = False
EXPORT_TO_TXT      = False
# ===============================================

OUTPUT_FILE = "folder_analysis.txt"
ROOT_DIR = os.getcwd()

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}

results = []

# Для анализа
image_resolutions = []
total_width = 0
total_height = 0


def format_name(path):
    name = os.path.basename(path)

    if not SHOW_EXTENSIONS and os.path.isfile(path):
        name = os.path.splitext(name)[0]

    if SHOW_FULL_PATH:
        return os.path.abspath(path)

    return name


# ===== ЧТЕНИЕ РАЗМЕРА БЕЗ БИБЛИОТЕК =====
def get_image_size(path):
    try:
        with open(path, "rb") as f:
            header = f.read(24)

            # PNG
            if header.startswith(b'\211PNG\r\n\032\n'):
                width, height = struct.unpack(">II", header[16:24])
                return width, height

            # JPG
            elif header[0:2] == b'\xff\xd8':
                f.seek(2)
                while True:
                    byte = f.read(1)
                    if not byte:
                        break
                    if byte == b'\xff':
                        marker = f.read(1)

                        # SOF0 / SOF2 — там лежит размер
                        if marker in [b'\xc0', b'\xc2']:
                            f.read(3)
                            h, w = struct.unpack(">HH", f.read(4))
                            return w, h
                        else:
                            size_bytes = f.read(2)
                            if len(size_bytes) != 2:
                                break
                            size = struct.unpack(">H", size_bytes)[0]
                            f.seek(size - 2, 1)

    except Exception as e:
        print(f"Ошибка чтения: {path} ({e})")

    return None


def process_image(path):
    global total_width, total_height

    ext = os.path.splitext(path)[1].lower()

    if ext in IMAGE_EXTENSIONS:
        size = get_image_size(path)
        if size:
            w, h = size
            image_resolutions.append((w, h))
            total_width += w
            total_height += h


# ===== ОБХОД ФАЙЛОВ =====
if INCLUDE_SUBFOLDERS:
    for root, dirs, files in os.walk(ROOT_DIR):
        for d in dirs:
            results.append(format_name(os.path.join(root, d)))
        for f in files:
            full_path = os.path.join(root, f)
            results.append(format_name(full_path))
            process_image(full_path)
else:
    for item in os.listdir(ROOT_DIR):
        full_path = os.path.join(ROOT_DIR, item)
        results.append(format_name(full_path))

        if os.path.isfile(full_path):
            process_image(full_path)


# ===== ВЫВОД =====
for item in results:
    print(item)


# ===== АНАЛИЗ =====
if image_resolutions:
    count = len(image_resolutions)
    avg_width = total_width / count
    avg_height = total_height / count

    print("\n=== АНАЛИЗ ИЗОБРАЖЕНИЙ ===")
    print(f"Количество: {count}")
    print(f"Среднее разрешение: {int(avg_width)} x {int(avg_height)}")

else:
    print("\nИзображения не найдены.")


# ===== ЭКСПОРТ =====
if EXPORT_TO_TXT:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in results:
            f.write(item + "\n")

    print(f"\nСохранено в файл: {OUTPUT_FILE}")
