from datetime import datetime
from os import listdir
from pathlib import Path
from pickle import dump as pickleDump, load as pickleLoad
from tools import assertListOfObj, getIndex


DATABASE_DIR = 'database/'
DATABASE_BACKUP_DIR = f'{DATABASE_DIR}backups/'
DATABASE_FILE = 'database.bin'
DATABASE_FULL_FILE = f'{DATABASE_DIR}{DATABASE_FILE}'

FILE_DIR = "files/"
FILE_BACKUP_DIR = f'{FILE_DIR}backups/'


def loadDatabase():
    if Path(DATABASE_FULL_FILE).exists():
        with open(DATABASE_FULL_FILE, 'rb') as f:
            database = pickleLoad(f)

        return database

    return None


def dumpDatabase(database):
    if Path(DATABASE_FULL_FILE).exists():
        Path(DATABASE_BACKUP_DIR).mkdir(parents=True, exist_ok=True)

        newFileName = f'{DATABASE_BACKUP_DIR}{datetime.now().strftime("%Y%m%d%H%M%S%f")}{DATABASE_FILE}'

        i = 0
        while Path(newFileName).exists():
            newFileName = f'{DATABASE_BACKUP_DIR}{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{i}{DATABASE_FILE}'
            i += 1

        Path(DATABASE_FULL_FILE).rename(newFileName)

    Path(DATABASE_DIR).mkdir(parents=True, exist_ok=True)

    with open(DATABASE_FULL_FILE, 'wb') as f:
        pickleDump(database, f)


def backupProcessed(processed: list[Path]) -> None:
    assertListOfObj(processed, Path)

    if not processed:
        return

    Path(FILE_BACKUP_DIR).mkdir(parents=True, exist_ok=True)

    for file in processed:
        newFileName = f'{FILE_BACKUP_DIR}{datetime.now().strftime("%Y%m%d%H%M%S%f")}.txt'

        file.rename(newFileName)


def getFiles() -> list[Path]:
    if not Path(FILE_DIR).exists():
        return []

    return [Path(f'{FILE_DIR}{file}').resolve() for file in listdir(FILE_DIR) if Path(f'{FILE_DIR}{file}').is_file()]


def getLines(file: Path = None) -> list[str]:
    assert file.exists()

    with open(file) as f:
        lines = f.read().splitlines()

    return lines


def getLinesType(lines: list[str] = None) -> str:
    assert assertListOfObj(lines, str)

    if getIndex(' scouts ', lines, full=False) >= 0:
        return 'report'

    elif getIndex(' raids ', lines, full=False) >= 0:
        return 'report'

    elif getIndex(' attacks ', lines, full=False) >= 0:
        return 'report'

    else:
        return 'unknown'


def cleanLines(lines: list[str] = None) -> list[str]:
    assert assertListOfObj(lines, str)

    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]

    rtn = []

    for line in lines:
        rtn.append(line.replace('\t', ' '))

    return rtn
