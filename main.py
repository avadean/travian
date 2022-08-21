from inout import backupProcessed, cleanLines, dumpDatabase, loadDatabase, getFiles, getLines, getLinesType
from database import Database
from report import processReport


def main() -> int:
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

    database = loadDatabase()

    if database is None:
        database = Database(reports=reports)
    else:
        database.addReports(reports)

    dumpDatabase(database)

    backupProcessed(processed)

    return analyse()


def analyse() -> int:
    database: Database = loadDatabase()

    if database is None:
        return 1

    print(database)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
    #raise SystemExit(analyse())
