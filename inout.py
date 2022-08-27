from datetime import datetime
from os import listdir
from pathlib import Path
from pickle import dump as pickleDump, load as pickleLoad
from tools import assertListOfObj, getIndex


DATABASE_DIR = 'database/'
SAVES_DIR = 'saves/'
REPORTS_DIR = 'reports/'
WORLD_FILE = 'current.bin'

FILE_DIR = "files/"


def loadWorld(worldName: str = None):
    assert isinstance(worldName, str)

    if Path(saveFile := f'{DATABASE_DIR}{worldName}/{WORLD_FILE}').exists():

        with open(saveFile, 'rb') as f:
            world = pickleLoad(f)

        return world

    return None


def dumpWorld(world, worldName: str = None):
    assert isinstance(worldName, str)

    save = f'{DATABASE_DIR}{worldName}/{WORLD_FILE}'

    if Path(save).exists():
        Path(f'{DATABASE_DIR}{worldName}/{SAVES_DIR}').mkdir(parents=True, exist_ok=True)

        newName = f'{DATABASE_DIR}{worldName}/{SAVES_DIR}{datetime.now().strftime("%Y%m%d%H%M%S%f")}.bin'

        i = 0
        while Path(newName).exists():
            newName = f'{DATABASE_DIR}{worldName}/{SAVES_DIR}{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{i}.bin'
            i += 1

        Path(save).rename(newName)

    Path(f'{DATABASE_DIR}{worldName}').mkdir(parents=True, exist_ok=True)

    with open(save, 'wb') as saveFile:
        pickleDump(world, saveFile)


def backupProcessed(processed: list[Path], worldName: str = None) -> None:
    assertListOfObj(processed, Path)
    assert isinstance(worldName, str)

    if not processed:
        return

    reportDir = f'{DATABASE_DIR}{worldName}/{REPORTS_DIR}'

    Path(reportDir).mkdir(parents=True, exist_ok=True)

    for file in processed:
        newFileName = f'{reportDir}{datetime.now().strftime("%Y%m%d%H%M%S%f")}.txt'

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
