from data import structures, troops, Information
from dateutil.parser import parse
from tools import assertListOfObj, getIndex


class Report:
    def __init__(self, type_: str = None, **kwargs):
        assert isinstance(type_, str)

        self.type_ = type_

        self.attVill = kwargs.pop('attVill', None)
        self.attAlly = kwargs.pop('attAlly', None)
        self.attTroops = kwargs.pop('attTroops', None)
        self.attDeaths = kwargs.pop('attDeaths', None)

        self.defVill = kwargs.pop('defVill', None)
        self.defAlly = kwargs.pop('defAlly', None)
        self.defTroops = kwargs.pop('defTroops', None)
        self.defDeaths = kwargs.pop('defDeaths', None)

        self.dateTime = kwargs.pop('datetime', None)

        self.lumberBounty = kwargs.pop('lumberBounty', None)
        self.clayBounty = kwargs.pop('clayBounty', None)
        self.ironBounty = kwargs.pop('ironBounty', None)
        self.cropBounty = kwargs.pop('cropBounty', None)

        self.lumberScout = kwargs.pop('lumberScout', None)
        self.clayScout = kwargs.pop('clayScout', None)
        self.ironScout = kwargs.pop('ironScout', None)
        self.cropScout = kwargs.pop('cropScout', None)

        self.rallyLvl = kwargs.pop('rallyLvl', None)
        self.wallLvl = kwargs.pop('wallLvl', None)

        self.infos = kwargs.pop('infos', None)

    def __str__(self):
        string = ''

        string += '{}'

        return string

    def __eq__(self, other):
        return self.type_ == other.type_ \
               and self.dateTime == other.datetime \
               and self.lumberBounty == other.lumberBounty \
               and self.clayBounty == other.clayBounty \
               and self.ironBounty == other.ironBounty \
               and self.cropBounty == other.cropBounty \
               and self.lumberScout == other.lumberScout \
               and self.clayScout == other.clayScout \
               and self.ironScout == other.ironScout \
               and self.cropScout == other.cropScout \
               and self.rallyLvl == other.rallyLvl \
               and self.wallLvl == other.wallLvl


def processReport(lines: list[str]) -> Report:
    assertListOfObj(lines, str)

    type_ = getReportType(lines)

    if type_ == 'raid':
        kwargs = getBasicReportData(lines, type_)

        index = getIndex('Bounty', lines)

        kwargs['lumberBounty'] = int(lines[index + 1])
        kwargs['clayBounty'] = int(lines[index + 2])
        kwargs['ironBounty'] = int(lines[index + 3])
        kwargs['cropBounty'] = int(lines[index + 4])

        kwargs['infos'] = infos if (infos := getInfo(lines)) else None

    elif type_ == 'attack':
        kwargs = getBasicReportData(lines, type_)

        index = getIndex('Bounty', lines)

        kwargs['lumberBounty'] = int(lines[index + 1])
        kwargs['clayBounty'] = int(lines[index + 2])
        kwargs['ironBounty'] = int(lines[index + 3])
        kwargs['cropBounty'] = int(lines[index + 4])

        kwargs['infos'] = infos if (infos := getInfo(lines)) else None

    elif type_ == 'resources':
        kwargs = getBasicReportData(lines, type_)

        index = getIndex('Resources', lines)

        kwargs['lumberScout'] = int(lines[index + 1])
        kwargs['clayScout'] = int(lines[index + 2])
        kwargs['ironScout'] = int(lines[index + 3])
        kwargs['cropScout'] = int(lines[index + 4])

    elif type_ == 'defences':
        kwargs = getBasicReportData(lines, type_)

        index = getIndex('Information', lines)

        kwargs['rallyLvl'] = int(lines[index + 1].split('level')[-1])
        kwargs['wallLvl'] = int(lines[index + 2].split('level')[-1])

    else:
        raise ValueError(f'Do not know report type {type_}.')

    return Report(type_=type_, **kwargs)


def getReportType(lines: list[str]) -> str:
    assertListOfObj(lines, str)

    if getIndex(' raids ', lines, full=False) >= 0:
        return 'raid'

    elif getIndex(' attacks ', lines, full=False) >= 0:
        return 'attack'

    elif getIndex('Rally Point', lines, full=False) >= 0:
        return 'defences'

    elif getIndex('Resources', lines, full=False) >= 0:
        return 'resources'

    else:
        raise ValueError('Can\'t determine report type.')


def getBasicReportData(lines: list[str], type_: str) -> dict:
    assertListOfObj(lines, str)
    assert isinstance(type_, str)

    # (1) Villages.
    if type_ in ('resources', 'defences'):
        keyWord = ' scouts '
    elif type_ == 'raid':
        keyWord = ' raids '
    elif type_ == 'attack':
        keyWord = ' attacks '
    else:
        raise ValueError(f'Do not know type {type_}.')

    index = getIndex(keyWord, lines)

    vills = lines[index].split(keyWord.strip())

    assert len(vills) == 2, 'Error when parsing file #1.'

    attVill, defVill = vills

    dateAndTime = parse(lines[index + 1])

    # (2) Attacker.
    index = getIndex('ATTACKER', lines)

    attAlly = getAlliance(lines[index + 1])

    attAlly = None if not attAlly else attAlly

    troopNumsAtt, deathNumsAtt = getTroops(lines[index + 2:index + 5])

    # (3) Defender.
    index = getIndex('DEFENDER', lines)

    defAlly = getAlliance(lines[index + 1])

    defAlly = None if not defAlly else defAlly

    troopNumsDef, deathNumsDef = getTroops(lines[index + 2:index + 5])

    return {'attVill': attVill,
            'defVill': defVill,
            'attAlly': attAlly,
            'defAlly': defAlly,
            'attTroops': troopNumsAtt,
            'attDeaths': deathNumsAtt,
            'defTroops': troopNumsDef,
            'defDeaths': deathNumsDef,
            'datetime': dateAndTime}


def getAlliance(line: str = None):
    assert isinstance(line, str)

    # '[IA-Rh] ava from village 00 Air' ---> ('[IA-Rh] ava', '00 Air')
    info = line.split('from village')

    assert len(info) == 2, 'Error when parsing file #3.'

    # ('[IA-Rh] ava', '00 Air') ---> '[IA-Rh] ava'
    info = info[0]

    assert info.startswith('['), 'Error when parsing file #4.'

    # '[IA-Rh] ava' ---> 'IA-Rh] ava'
    info = info[1:]

    try:
        index = info.index(']')
    except ValueError:
        raise ValueError('Error when parsing file #5.')

    alliance = info[:index].strip()

    return alliance


def getTroops(lines: list[str] = None):
    assertListOfObj(lines, str)
    assert len(lines) == 3

    troopLine = lines[0]

    if troopLine.startswith('Legionnaire'):
        attTribe = 'Romans'
    elif troopLine.startswith('Clubswinger'):
        attTribe = 'Teutons'
    elif troopLine.startswith('Phalanx'):
        attTribe = 'Gauls'
    else:
        raise ValueError('Error when parsing file #2.')

    troopNums = lines[1].split(' ')
    troopNums = dict(zip(troops[attTribe], [int(num) for num in troopNums if num]))

    deathNums = lines[2].split(' ')
    deathNums = dict(zip(troops[attTribe], [int(num) for num in deathNums if num]))

    return troopNums, deathNums


def getInfo(lines: list[str] = None):
    index = getIndex('Information', lines)

    hits = []

    while 'Bounty' not in (line := lines[index]) and 'DEFENDER' not in line:  # Two checks for extra safety.
        line = line[len('Information'):].strip() if line.startswith('Information') else line

        if 'destroyed' in line:

            if 'village has been completely destroyed' in line:
                # e.g The village has been completely destroyed.
                hits.append(Information(structure='village', toLevel=0))

            elif 'no building in the target village that can be destroyed by catapults' in line:
                # e.g There is no building in the target village that can be destroyed by catapults.
                hits.append(Information(note='No building for catapults to destroy.'))

            elif 'level' in line:
                # e.g Marketplace level 20 destroyed.
                structure = getStructure(line)

                if structure is None:
                    print('Cannot determine structure in line \'{line}\'')
                    continue

                level = int(line[line.index('level') + len('level'):line.index('destroyed')].strip().strip('.').strip())

                hits.append(Information(structure=structure, fromLevel=level, toLevel=0))

            else:
                # e.g City wall destroyed.
                structure = getStructure(line)

                if structure is None:
                    print('Cannot determine structure in line \'{line}\'')
                    continue

                hits.append(Information(structure=structure, toLevel=0))

        elif 'damaged' in line:

            if 'not damaged' in line:
                # e.g Marketplace was not damaged.
                structure = getStructure(line)

                if structure is None:
                    print('Cannot determine structure in line \'{line}\'')
                    continue

                hits.append(Information(structure=structure))

            elif 'level' in line:
                # e.g City wall damaged from level 15 to level 8.
                structure = getStructure(line)

                if structure is None:
                    print('Cannot determine structure in line \'{line}\'')
                    continue

                fromLevel = int(line[line.index('from level') + len('from level'):].strip().strip('.').strip().split()[0])
                toLevel = int(line[line.index('to level') + len('to level'):].strip().strip('.').strip().split()[0])

                hits.append(Information(structure=structure, fromLevel=fromLevel, toLevel=toLevel))

            else:
                print('Cannot determine Information in line \'{line}\'')
                continue

        elif 'own troops' in line:
            # e.g You freed 146 own troops. You could save 109 own troops.

            troopsFreed = int(line[line.index('You freed') + len('You freed'):].strip().strip('.').strip().split()[0])
            couldSave = int(line[line.index('You could save') + len('You could save'):].strip().strip('.').strip().split()[0])

            hits.append(Information(troopsFreed=troopsFreed, couldSave=couldSave))

        elif 'Random target was selected' in line:
            # e.g Random target was selected.

            hits.append(Information(note='Random target was selected.'))

        else:
            print('Cannot determine Information in line \'{line}\'')
            continue


        index += 1

    return hits


def getStructure(line: str = None) -> str:
    assert isinstance(line, str)

    for structure in structures:
        if structure.lower() in line.lower():
            return structure
