

class Information:
    def __init__(self, **kwargs):
        self.structure = kwargs.pop('structure', None)

        self.fromLevel = kwargs.pop('fromLevel', None)
        self.toLevel = kwargs.pop('toLevel', None)

        self.destroyed = self.toLevel == 0 if self.toLevel is not None else False
        self.damaged = max(self.destroyed,
                           self.fromLevel > self.toLevel if self.fromLevel is not None and
                                                            self.toLevel is not None else False)

        self.ram = self.structure in walls
        self.catapult = self.structure in buildings

        self.troopsFreed = kwargs.pop('troopsFreed', None)
        self.couldSave = kwargs.pop('couldSave', None)

        self.note = kwargs.pop('note', None)

    def __str__(self):
        string = ''

        if self.structure is not None:
            string += f'{self.structure} '

            if self.destroyed:
                if self.fromLevel is not None:
                    string += f'level {self.fromLevel} '

                string += 'was destroyed.'

            elif self.damaged:
                string += f'was damaged from level {self.fromLevel} to level {self.toLevel}.'

            else:
                string += 'was not damaged.'

            string += '\n'

        elif self.troopsFreed is not None:
            string += f'Troops freed: {self.troopsFreed}'
            string += f'Could\'ve saved: {self.couldSave}'

        elif self.note is not None:
            string += f'{self.note}'

        return string


troops = { 'Gauls': [ 'Phalanx', 'Swordsman', 'Theutates Thunder',
                      'Pathfinder', 'Druidrider', 'Haeduan',
                      'Ram', 'Trebuchet',
                      'Chieftain', 'Settler',
                      'Hero' ],

           'Romans': [ 'Legionnaire', 'Praetorian', 'Imperian',
                       'Equites Legati', 'Equites Imperatoris', 'Equites Caesaris',
                       'Battering ram', 'Fire Catapult',
                       'Senator', 'Settler',
                       'Hero' ],

           'Teutons': [ 'Clubswinger', 'Spearman', 'Axeman',
                        'Scout', 'Paladin', 'Teutonic Knight',
                        'Ram', 'Catapult',
                        'Chief', 'Settler',
                        'Hero' ] }

infrastructure = [ 'Warehouse', 'Granary', 'Main Building', 'Marketplace',
                   'Embassy', 'Cranny', 'Town Hall', 'Residence', 'Palace',
                   'Treasury', 'Trade Office', 'Stonemason\'s Lodge',
                   'Brewery', 'Great Warehouse', 'Great Granary',
                   'Wonder Of The World', 'Horse Drinking Trough' ]

military = [ 'Smithy', 'Tournament Square', 'Rally Point',
             'Barracks', 'Stable', 'Workshop', 'Academy',
             'Great Barracks', 'Great Stable',
             'Trapper', 'Hero\'s Mansion', 'Hospital' ]

resources = [ 'Woodcutter', 'Clay Pit', 'Iron Mine', 'Cropland',
              'Sawmill', 'Brickyard', 'Iron Foundry',
              'Grain Mill', 'Bakery' ]

walls = [ 'City Wall', 'Earth Wall', 'Palisade' ]

buildings = infrastructure + military + resources

structures = buildings + walls
