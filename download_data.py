"""Скачивает три файла соревнования H&M с Kaggle в папку data/.

Нужно:
1. Принять правила соревнования на странице
   https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/rules
2. Задать токен Kaggle: переменная окружения KAGGLE_API_TOKEN
   (или файл ~/.kaggle/access_token / ~/.kaggle/kaggle.json).

Запуск из корня репозитория:  python scripts/download_data.py
"""
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

COMPETITION = "h-and-m-personalized-fashion-recommendations"
FILES = ["articles.csv", "customers.csv", "transactions_train.csv"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    if shutil.which("kaggle") is None:
        sys.exit("Не найден kaggle CLI: pip install kaggle")
    DATA_DIR.mkdir(exist_ok=True)
    for name in FILES:
        if (DATA_DIR / name).exists():
            print(f"{name}: уже есть")
            continue
        print(f"{name}: скачиваю...")
        subprocess.run(["kaggle", "competitions", "download", "-c", COMPETITION,
                        "-f", name, "-p", str(DATA_DIR)], check=True)
        archive = DATA_DIR / f"{name}.zip"
        if archive.exists():
            with zipfile.ZipFile(archive) as z:
                z.extractall(DATA_DIR)
            archive.unlink()
        if not (DATA_DIR / name).exists():
            sys.exit(f"{name}: файл не появился, проверьте токен и принятие правил соревнования")
    print("Готово:", ", ".join(FILES))


if __name__ == "__main__":
    main()
