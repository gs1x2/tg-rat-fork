import os
import shutil
import tempfile
import zipfile
import sys

BROWSERS = {
    'chrome': {
        'win_path': os.path.expandvars(r'%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\History'),
        'files': ['History']
    },
    'edge': {
        'win_path': os.path.expandvars(r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\History'),
        'files': ['History']
    }
}

def export_history(browser: str = 'chrome'):
    """
    Экспортирует raw-файл(ы) истории выбранного браузера (chrome или edge).
    Возвращает путь к архиву или файлу для отправки.
    """
    browser = browser.lower()
    if browser not in BROWSERS:
        raise ValueError('Browser must be "chrome" or "edge"')
    files_to_export = []
    for fname in BROWSERS[browser]['files']:
        fpath = BROWSERS[browser]['win_path']
        if os.path.exists(fpath):
            # Копируем файл, чтобы не блокировать браузер
            tmp_dir = tempfile.mkdtemp()
            dst = os.path.join(tmp_dir, fname)
            shutil.copy2(fpath, dst)
            files_to_export.append(dst)
    if not files_to_export:
        raise FileNotFoundError('History file(s) not found')
    if len(files_to_export) == 1:
        return files_to_export[0]
    # Если файлов несколько, архивируем
    archive_path = os.path.join(tempfile.gettempdir(), f'browser_history_{browser}.zip')
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_export:
            zf.write(f, os.path.basename(f))
    return archive_path 