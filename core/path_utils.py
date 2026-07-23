import os
import sys


def resource_path(relative_path):
    """
    assets, locales gibi uygulamayla birlikte gelen
    salt okunur dosyaların yolunu döndürür.
    """

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

    return os.path.join(base_path, relative_path)


def user_data_path(filename):
    """
    Kullanıcının değiştirilebilir verilerini
    AppData/Local/NagomiDesk içinde saklar.
    """

    base_path = os.path.join(
        os.environ.get(
            "LOCALAPPDATA",
            os.path.expanduser("~")
        ),
        "NagomiDesk"
    )

    os.makedirs(base_path, exist_ok=True)

    return os.path.join(base_path, filename)