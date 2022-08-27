from inout import backupProcessed, cleanLines, dumpWorld, loadWorld, getFiles, getLines, getLinesType
from report import processReport
from world import World


def main(worldName: str = 'testing') -> int:
    files = getFiles()

    reports = []

    processed = []

    for file in files:
        lines = getLines(file)

        lines = cleanLines(lines)

        type_ = getLinesType(lines)

        if type_ == 'report':
            reports.append(processReport(lines))

        else:
            print(f'Do not know file type {type_}. Skipping.')
            continue

        processed.append(file)

    world = loadWorld(worldName)

    if world is None:
        world = World(name=worldName, reports=reports)
    else:
        world.addReports(reports)

    err = dumpWorld(world, worldName=world.name)

    backupProcessed(processed, worldName)

    return analyse(worldName)


def analyse(worldName: str = 'testing') -> int:
    world: World = loadWorld(worldName)

    if world is None:
        return 1

    # print(world.reports[0].infos[1])

    return 0


if __name__ == '__main__':
    raise SystemExit(main(worldName='ts8'))
    #raise SystemExit(analyse())
