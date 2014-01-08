from cheshire3.normalizer import SimpleNormalizer

class NovelNormalizer(SimpleNormalizer):
  
    def __init__(self, session, config, parent):
        SimpleNormalizer.__init__(self, session, config, parent)
        self.novels = ['BH', 'BR', 'DC',
                        'DS', 'ED', 'GE', 'HT', 'LD', 'MC', 'NN',
                        'OCS', 'OMF', 'OT', 'PP', 'TTC']
          
    def process_string(self, session, data):
        if data in self.novels:
            return 'novel'
        else:
            return 'other'


class CorpusNormalizer(SimpleNormalizer):
  
    def __init__(self, session, config, parent):
        SimpleNormalizer.__init__(self, session, config, parent)
        self.dickens = ['AN', 'BH', 'BL', 'BR', 'CC', 'CHI', 'CH', 'DC',
                        'DS', 'ED', 'GE', 'HM', 'HT', 'LD', 'MC', 'NN',
                        'OCS', 'OMF', 'OT', 'PP', 'SB', 'TTC', 'UT']
          
    def process_string(self, session, data):
        if data in self.dickens:
            return 'dickens'
        else:
            return 'ntc'
