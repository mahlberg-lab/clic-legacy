import re
import unittest
from functools import partial

from clic.concordance import Concordance

"""
Currently, the results from the concordance view look like this
(showing only one line in the concordance):

[94,                     # the total count
 [[' points ',           # the left text
   ' tenaciously ',
   ' to ',
   ' the ',
   ' pavement,',
   ' and ',
   ' accumulating ',
   ' at ',
   ' compound ',
   ' interest.'],
  ['Fog '],             # the search term or phrase
  [' everywhere.',      # the right text
   'Fog ',
   ' up ',
   ' the ',
   ' river,',
   ' where ',
   ' it ',
   ' flows ',
   ' among ',
   ' green '],
  ['BH', u'Bleak House', '1', '2', '9', '169', '2615'],   # book abbr, title, chapter, paragraph, sentence,  word, ???
  ['2', '9', '169', '354362']],                           # paragraph, sentence, word, ???
...

Because the list of results also contains an element that
is not a hit (the first element, namely the total count).
We need to manually correct each result list
with this element this should be fixed by using a dictionary.
"""
correction = 1

# Ignore any space in a match
def strip_space(m):
    m = [re.sub(r'\W', '', x) for x in m]
    m = [x for x in m if len(x) > 0]
    return m

class PhraseSearchOneTerm(unittest.TestCase):

    def setUp(self):
        concordance = Concordance()
        self.create_concordance = partial(concordance.create_concordance,
                                             terms="fog",
                                             idxName="chapter-idx",
                                             Materials=["dickens"],
                                             selectWords="whole")

    def test_basic_query(self):
        # WordSmith (WS) has 96 because it includes compound nouns
        fog = self.create_concordance()
        self.assertEqual(len(fog) - correction, 94)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

        self.assertEqual([[strip_space(x[0]), strip_space(x[1]), strip_space(x[2]), x[3], x[4]] for x in fog[1:]], [
            [['points', 'tenaciously', 'to', 'the', 'pavement', 'and', 'accumulating', 'at', 'compound', 'interest'], ['Fog'], ['everywhere', 'Fog', 'up', 'the', 'river', 'where', 'it', 'flows', 'among', 'green'], ['BH', u'Bleak House', '1', '2', '9', '169', '2615'], ['2', '9', '169', '354362']],
            [['to', 'the', 'pavement', 'and', 'accumulating', 'at', 'compound', 'interest', 'Fog', 'everywhere'], ['Fog'], ['up', 'the', 'river', 'where', 'it', 'flows', 'among', 'green', 'aits', 'and'], ['BH', u'Bleak House', '1', '2', '10', '171', '2615'], ['2', '10', '171', '354362']],
            [['and', 'the', 'waterside', 'pollutions', 'of', 'a', 'great', 'and', 'dirty', 'city'], ['Fog'], ['on', 'the', 'Essex', 'marshes', 'fog', 'on', 'the', 'Kentish', 'heights', 'Fog'], ['BH', u'Bleak House', '1', '2', '11', '206', '2615'], ['2', '11', '206', '354362']],
            [['Fog', 'on', 'the', 'Essex', 'marshes', 'fog', 'on', 'the', 'Kentish', 'heights'], ['Fog'], ['creeping', 'into', 'the', 'cabooses', 'of', 'collierbrigs', 'fog', 'lying', 'out', 'on'], ['BH', u'Bleak House', '1', '2', '12', '216', '2615'], ['2', '12', '216', '354362']],
            [['fog', 'drooping', 'on', 'the', 'gunwales', 'of', 'barges', 'and', 'small', 'boats'], ['Fog'], ['in', 'the', 'eyes', 'and', 'throats', 'of', 'ancient', 'Greenwich', 'pensioners', 'wheezing'], ['BH', u'Bleak House', '1', '2', '13', '247', '2615'], ['2', '13', '247', '354362']],
            [['the', 'river', 'where', 'it', 'flows', 'among', 'green', 'aits', 'and', 'meadows'], ['fog'], ['down', 'the', 'river', 'where', 'it', 'rolls', 'deified', 'among', 'the', 'tiers'], ['BH', u'Bleak House', '1', '2', '10', '183', '2615'], ['2', '10', '183', '354362']],
            [['a', 'great', 'and', 'dirty', 'city', 'Fog', 'on', 'the', 'Essex', 'marshes'], ['fog'], ['on', 'the', 'Kentish', 'heights', 'Fog', 'creeping', 'into', 'the', 'cabooses', 'of'], ['BH', u'Bleak House', '1', '2', '11', '211', '2615'], ['2', '11', '211', '354362']],
            [['the', 'Kentish', 'heights', 'Fog', 'creeping', 'into', 'the', 'cabooses', 'of', 'collierbrigs'], ['fog'], ['lying', 'out', 'on', 'the', 'yards', 'and', 'hovering', 'in', 'the', 'rigging'], ['BH', u'Bleak House', '1', '2', '12', '223', '2615'], ['2', '12', '223', '354362']],
            [['the', 'yards', 'and', 'hovering', 'in', 'the', 'rigging', 'of', 'great', 'ships'], ['fog'], ['drooping', 'on', 'the', 'gunwales', 'of', 'barges', 'and', 'small', 'boats', 'Fog'], ['BH', u'Bleak House', '1', '2', '12', '237', '2615'], ['2', '12', '237', '354362']],
            [['ancient', 'Greenwich', 'pensioners', 'wheezing', 'by', 'the', 'firesides', 'of', 'their', 'wards'], ['fog'], ['in', 'the', 'stem', 'and', 'bowl', 'of', 'the', 'afternoon', 'pipe', 'of'], ['BH', u'Bleak House', '1', '2', '13', '264', '2615'], ['2', '13', '264', '354362']],
            [['pipe', 'of', 'the', 'wrathful', 'skipper', 'down', 'in', 'his', 'close', 'cabin'], ['fog'], ['cruelly', 'pinching', 'the', 'toes', 'and', 'fingers', 'of', 'his', 'shivering', 'little'], ['BH', u'Bleak House', '1', '2', '13', '283', '2615'], ['2', '13', '283', '354362']],
            [['bridges', 'peeping', 'over', 'the', 'parapets', 'into', 'a', 'nether', 'sky', 'of'], ['fog'], ['with', 'fog', 'all', 'round', 'them', 'as', 'if', 'they', 'were', 'up'], ['BH', u'Bleak House', '1', '2', '14', '312', '2615'], ['2', '14', '312', '354362']],
            [['over', 'the', 'parapets', 'into', 'a', 'nether', 'sky', 'of', 'fog', 'with'], ['fog'], ['all', 'round', 'them', 'as', 'if', 'they', 'were', 'up', 'in', 'a'], ['BH', u'Bleak House', '1', '2', '14', '314', '2615'], ['2', '14', '314', '354362']],
            [['and', 'hanging', 'in', 'the', 'misty', 'clouds', 'Gas', 'looming', 'through', 'the'], ['fog'], ['in', 'divers', 'places', 'in', 'the', 'streets', 'much', 'as', 'the', 'sun'], ['BH', u'Bleak House', '1', '3', '15', '336', '2615'], ['3', '15', '336', '354362']],
            [['unwilling', 'look', 'The', 'raw', 'afternoon', 'is', 'rawest', 'and', 'the', 'dense'], ['fog'], ['is', 'densest', 'and', 'the', 'muddy', 'streets', 'are', 'muddiest', 'near', 'that'], ['BH', u'Bleak House', '1', '4', '17', '392', '2615'], ['4', '17', '392', '354362']],
            [['in', 'Lincolns', 'Inn', 'Hall', 'at', 'the', 'very', 'heart', 'of', 'the'], ['fog'], ['sits', 'the', 'Lord', 'High', 'Chancellor', 'in', 'his', 'High', 'Court', 'of'], ['BH', u'Bleak House', '1', '4', '18', '433', '2615'], ['4', '18', '433', '354362']],
            [['in', 'his', 'High', 'Court', 'of', 'Chancery', 'Never', 'can', 'there', 'come'], ['fog'], ['too', 'thick', 'never', 'can', 'there', 'come', 'mud', 'and', 'mire', 'too'], ['BH', u'Bleak House', '1', '5', '19', '449', '2615'], ['5', '19', '449', '354362']],
            [['lantern', 'in', 'the', 'roof', 'where', 'he', 'can', 'see', 'nothing', 'but'], ['fog'], ['On', 'such', 'an', 'afternoon', 'some', 'score', 'of', 'members', 'of', 'the'], ['BH', u'Bleak House', '1', '6', '20', '556', '2615'], ['6', '20', '556', '354362']],
            [['dim', 'with', 'wasting', 'candles', 'here', 'and', 'there', 'well', 'may', 'the'], ['fog'], ['hang', 'heavy', 'in', 'it', 'as', 'if', 'it', 'would', 'never', 'get'], ['BH', u'Bleak House', '1', '6', '23', '727', '2615'], ['6', '23', '727', '354362']],
            [['midst', 'of', 'the', 'mud', 'and', 'at', 'the', 'heart', 'of', 'the'], ['fog'], ['sits', 'the', 'Lord', 'High', 'Chancellor', 'in', 'his', 'High', 'Court', 'of'], ['BH', u'Bleak House', '1', '11', '59', '2017', '2615'], ['11', '59', '2017', '354362']],
            [['voice', 'arises', 'fully', 'inflated', 'in', 'the', 'back', 'settlements', 'of', 'the'], ['fog'], ['and', 'says', 'Will', 'your', 'lordship', 'allow', 'me', 'I', 'appear', 'for'], ['BH', u'Bleak House', '1', '25', '79', '2365', '2615'], ['25', '79', '2365', '354362']],
            [['of', 'the', 'roof', 'the', 'very', 'little', 'counsel', 'drops', 'and', 'the'], ['fog'], ['knows', 'him', 'no', 'more', 'Everybody', 'looks', 'for', 'him', 'Nobody', 'can'], ['BH', u'Bleak House', '1', '26', '83', '2430', '2615'], ['26', '83', '2430', '354362']],
            [['particular', 'I', 'had', 'never', 'heard', 'of', 'such', 'a', 'thing', 'A'], ['fog'], ['miss', 'said', 'the', 'young', 'gentleman', 'Oh', 'indeed', 'said', 'I', 'We'], ['BH', u'Bleak House', '3', '115', '286', '5841', '7896'], ['178', '502', '11357', '354362']],
            [['moment', 'to', 'ask', 'a', 'question', 'and', 'left', 'us', 'in', 'the'], ['fog'], ['with', 'the', 'Lord', 'Chancellors', 'carriage', 'and', 'servants', 'waiting', 'for', 'him'], ['BH', u'Bleak House', '3', '158', '366', '7479', '7896'], ['221', '582', '12995', '354362']],
            [['He', 'seemed', 'quite', 'delighted', 'with', 'it', 'on', 'my', 'account', 'The'], ['fog'], ['is', 'very', 'dense', 'indeed', 'said', 'I', 'Not', 'that', 'it', 'affects'], ['BH', u'Bleak House', '4', '15', '32', '590', '4894'], ['251', '670', '14002', '354362']],
            [['of', 'high', 'houses', 'like', 'an', 'oblong', 'cistern', 'to', 'hold', 'the'], ['fog'], ['There', 'was', 'a', 'confused', 'little', 'crowd', 'of', 'people', 'principally', 'children'], ['BH', u'Bleak House', '4', '17', '35', '694', '4894'], ['253', '673', '14106', '354362']],
            [['no', 'one', 'The', 'purblind', 'day', 'was', 'feebly', 'struggling', 'with', 'the'], ['fog'], ['when', 'I', 'opened', 'my', 'eyes', 'to', 'encounter', 'those', 'of', 'a'], ['BH', u'Bleak House', '4', '109', '249', '4848', '4894'], ['345', '887', '18260', '354362']],
            [['Although', 'the', 'morning', 'was', 'raw', 'and', 'although', 'the'], ['fog'], ['still', 'seemed', 'heavy', 'I', 'say', 'seemed', 'for', 'the', 'windows', 'were'], ['BH', u'Bleak House', '5', '1', '1', '8', '5700'], ['346', '889', '18314', '354362']],
            [['trusting', 'when', 'I', 'first', 'saw', 'it', 'in', 'that', 'memorable', 'November'], ['fog'], ['how', 'much', 'more', 'did', 'it', 'seem', 'now', 'when', 'I', 'knew'], ['BH', u'Bleak House', '17', '52', '124', '1988', '5682'], ['1746', '4992', '93573', '354362']],
            [['These', 'may', 'not', 'be', 'desirable', 'characteristics', 'when', 'November', 'comes', 'with'], ['fog'], ['and', 'sleet', 'or', 'January', 'with', 'ice', 'and', 'snow', 'but', 'they'], ['BH', u'Bleak House', '22', '1', '2', '39', '5191'], ['2343', '6592', '122363', '354362']],
            [['ever', 'saw', 'The', 'sea', 'was', 'heaving', 'under', 'a', 'thick', 'white'], ['fog'], ['and', 'nothing', 'else', 'was', 'moving', 'but', 'a', 'few', 'early', 'ropemakers'], ['BH', u'Bleak House', '45', '28', '81', '1756', '5378'], ['4968', '13529', '248218', '354362']],
            [['ships', 'cabin', 'and', 'that', 'delighted', 'Charley', 'very', 'much', 'Then', 'the'], ['fog'], ['began', 'to', 'rise', 'like', 'a', 'curtain', 'and', 'numbers', 'of', 'ships'], ['BH', u'Bleak House', '45', '29', '84', '1847', '5378'], ['4969', '13532', '248309', '354362']],
            [['the', 'dark', 'little', 'parlour', 'had', 'been', 'filled', 'with', 'a', 'dense'], ['fog'], ['which', 'clearing', 'away', 'in', 'an', 'instant', 'left', 'it', 'all', 'radiance'], ['BR', u'Barnaby Rudge', '26', '21', '62', '1076', '1900'], ['1529', '3755', '78869', '254127']],
            [['wind', 'getting', 'up', 'out', 'at', 'sea', 'to', 'know', 'that', 'the'], ['fog'], ['was', 'creeping', 'over', 'the', 'desolate', 'flat', 'outside', 'and', 'to', 'look'], ['DC', u'David Copperfield', '3', '23', '59', '1851', '6392'], ['253', '597', '12584', '356233']],
            [['recollect', 'the', 'kind', 'of', 'day', 'it', 'was', 'I', 'smell', 'the'], ['fog'], ['that', 'hung', 'about', 'the', 'place', 'I', 'see', 'the', 'hoar', 'frost'], ['DC', u'David Copperfield', '9', '3', '8', '170', '4929'], ['1016', '2541', '49283', '356233']],
            [['anything', 'but', 'regal', 'in', 'a', 'drizzling', 'rain', 'and', 'a', 'darkbrown'], ['fog'], ['until', 'I', 'was', 'admonished', 'by', 'the', 'waiter', 'that', 'the', 'gentleman'], ['DC', u'David Copperfield', '20', '1', '3', '149', '3636'], ['2284', '5784', '118140', '356233']],
            [['we', 'went', 'on', 'together', 'through', 'the', 'frosty', 'air', 'and', 'gathering'], ['fog'], ['towards', 'the', 'twinkling', 'lights', 'of', 'the', 'town', 'One', 'dark', 'evening'], ['DC', u'David Copperfield', '22', '7', '29', '990', '9190'], ['2517', '6435', '130830', '356233']],
            [['A', 'man', 'sitting', 'in', 'a', 'pigeonholeplace', 'looked', 'out', 'of', 'the'], ['fog'], ['and', 'took', 'money', 'from', 'somebody', 'inquiring', 'if', 'I', 'was', 'one'], ['DC', u'David Copperfield', '24', '37', '143', '2639', '3516'], ['2874', '7416', '147652', '356233']],
            [['evening', 'It', 'was', 'dark', 'and', 'raining', 'and', 'I', 'saw', 'more'], ['fog'], ['and', 'mud', 'in', 'a', 'minute', 'than', 'I', 'had', 'seen', 'in'], ['DC', u'David Copperfield', '59', '1', '2', '18', '6516'], ['6573', '17311', '333421', '356233']],
            [['they', 'had', 'been', 'small', 'suns', 'looking', 'at', 'you', 'through', 'a'], ['fog'], ['and', 'a', 'newlyawakened', 'manner', 'such', 'as', 'he', 'might', 'have', 'acquired'], ['DS', u'Dombey and Son', '4', '6', '18', '794', '4877'], ['361', '775', '15098', '356405']],
            [['old', 'Sol', 'looking', 'wistfully', 'at', 'his', 'nephew', 'out', 'of', 'the'], ['fog'], ['that', 'always', 'seemed', 'to', 'hang', 'about', 'him', 'and', 'laying', 'an'], ['DS', u'Dombey and Son', '4', '33', '87', '1810', '4877'], ['388', '844', '16114', '356405']],
            [['run', 'my', 'child', 'My', 'love', 'to', 'you', 'Some', 'of', 'the'], ['fog'], ['that', 'hung', 'about', 'old', 'Sol', 'seemed', 'to', 'have', 'got', 'into'], ['DS', u'Dombey and Son', '4', '47', '114', '2238', '4877'], ['402', '871', '16542', '356405']],
            [['made', 'his', 'way', 'up', 'the', 'little', 'staircase', 'through', 'an', 'artificial'], ['fog'], ['occasioned', 'by', 'the', 'washing', 'which', 'covered', 'the', 'banisters', 'with', 'a'], ['DS', u'Dombey and Son', '9', '60', '171', '3485', '5418'], ['1103', '2466', '49994', '356405']],
            [['with', 'Alexander', 'still', 'upon', 'the', 'pavingstone', 'dimly', 'looming', 'through', 'a'], ['fog'], ['of', 'dust', 'and', 'so', 'absorbed', 'was', 'Mrs', 'MacStinger', 'in', 'her'], ['DS', u'Dombey and Son', '23', '102', '232', '6272', '9281'], ['2856', '6412', '137199', '356405']],
            [['December', 'afternoon', 'towards', 'six', 'oclock', 'when', 'it', 'was', 'filled', 'with'], ['fog'], ['and', 'candles', 'shed', 'murky', 'and', 'blurred', 'rays', 'through', 'the', 'windows'], ['ED', u'The Mystery of Edwin Drood', '11', '3', '7', '276', '5263'], ['978', '2219', '37294', '94126']],
            [['them', 'for', 'the', 'night', 'what', 'is', 'in', 'the', 'wind', 'besides'], ['fog'], ['Mr', 'Drood', 'said', 'Bazzard', 'What', 'of', 'him', 'Has', 'called', 'said'], ['ED', u'The Mystery of Edwin Drood', '11', '11', '36', '1030', '5263'], ['986', '2248', '38048', '94126']],
            [['you', 'do', 'Mr', 'Edwin', 'Dear', 'me', 'youre', 'choking', 'Its', 'this'], ['fog'], ['returned', 'Edwin', 'and', 'it', 'makes', 'my', 'eyes', 'smart', 'like', 'Cayenne'], ['ED', u'The Mystery of Edwin Drood', '11', '19', '47', '1095', '5263'], ['994', '2259', '38113', '94126']],
            [['chair', 'Edwin', 'took', 'the', 'easychair', 'in', 'the', 'corner', 'and', 'the'], ['fog'], ['he', 'had', 'brought', 'in', 'with', 'him', 'and', 'the', 'fog', 'he'], ['ED', u'The Mystery of Edwin Drood', '11', '23', '56', '1188', '5263'], ['998', '2268', '38206', '94126']],
            [['the', 'fog', 'he', 'had', 'brought', 'in', 'with', 'him', 'and', 'the'], ['fog'], ['he', 'took', 'off', 'with', 'his', 'greatcoat', 'and', 'neck', 'shawl', 'was'], ['ED', u'The Mystery of Edwin Drood', '11', '23', '56', '1197', '5263'], ['998', '2268', '38215', '94126']],
            [['cried', 'Mr', 'Grewgious', 'excuse', 'my', 'interrupting', 'you', 'do', 'stop', 'The'], ['fog'], ['may', 'clear', 'in', 'an', 'hour', 'or', 'two', 'We', 'can', 'have'], ['ED', u'The Mystery of Edwin Drood', '11', '25', '59', '1240', '5263'], ['1000', '2271', '38258', '94126']],
            [['waiter', 'and', 'the', 'three', 'brought', 'in', 'with', 'them', 'as', 'much'], ['fog'], ['as', 'gave', 'a', 'new', 'roar', 'to', 'the', 'fire', 'The', 'flying'], ['ED', u'The Mystery of Edwin Drood', '11', '60', '122', '2058', '5263'], ['1035', '2334', '39076', '94126']],
            [['reproached', 'on', 'his', 'return', 'by', 'the', 'immovable', 'waiter', 'for', 'bringing'], ['fog'], ['with', 'him', 'and', 'being', 'out', 'of', 'breath', 'At', 'the', 'conclusion'], ['ED', u'The Mystery of Edwin Drood', '11', '60', '126', '2208', '5263'], ['1035', '2338', '39226', '94126']],
            [['hung', 'on', 'the', 'line', 'in', 'the', 'National', 'Gallery', 'As', 'the'], ['fog'], ['had', 'been', 'the', 'proximate', 'cause', 'of', 'this', 'sumptuous', 'repast', 'so'], ['ED', u'The Mystery of Edwin Drood', '11', '62', '131', '2344', '5263'], ['1037', '2343', '39362', '94126']],
            [['been', 'the', 'proximate', 'cause', 'of', 'this', 'sumptuous', 'repast', 'so', 'the'], ['fog'], ['served', 'for', 'its', 'general', 'sauce', 'To', 'hear', 'the', 'outdoor', 'clerks'], ['ED', u'The Mystery of Edwin Drood', '11', '62', '131', '2356', '5263'], ['1037', '2343', '39374', '94126']],
            [['his', 'outer', 'clothing', 'muttering', 'something', 'about', 'time', 'and', 'appointments', 'The'], ['fog'], ['was', 'reported', 'no', 'clearer', 'by', 'the', 'flying', 'waiter', 'who', 'alighted'], ['ED', u'The Mystery of Edwin Drood', '11', '121', '254', '4864', '5263'], ['1096', '2466', '41882', '94126']],
            [['place', 'apparently', 'and', 'its', 'rays', 'looked', 'solid', 'substance', 'on', 'the'], ['fog'], ['We', 'were', 'noticing', 'this', 'and', 'saying', 'how', 'that', 'the', 'mist'], ['GE', u'Great Expectations', '15', '76', '195', '3603', '4254'], ['921', '2280', '44212', '185199']],
            [['in', 'and', 'out', 'opening', 'more', 'red', 'eyes', 'in', 'the', 'gathering'], ['fog'], ['than', 'my', 'rushlight', 'tower', 'at', 'the', 'Hummums', 'had', 'opened', 'white'], ['GE', u'Great Expectations', '48', '11', '16', '284', '2711'], ['3066', '7535', '147239', '185199']],
            [['sky', 'it', 'might', 'have', 'been', 'midnight', 'There', 'was', 'a', 'dense'], ['fog'], ['too', 'as', 'if', 'it', 'were', 'a', 'city', 'in', 'the', 'clouds'], ['MC', u'Martin Chuzzlewit', '8', '60', '141', '2641', '4500'], ['895', '2338', '50548', '335750']],
            [['of', 'not', 'being', 'overlooked', 'as', 'they', 'would', 'see', 'when', 'the'], ['fog'], ['cleared', 'off', 'Nor', 'was', 'this', 'a', 'vainglorious', 'boast', 'for', 'it'], ['MC', u'Martin Chuzzlewit', '8', '87', '203', '4230', '4500'], ['922', '2400', '52137', '335750']],
            [['at', 'the', 'same', 'time', 'fell', 'discreetly', 'back', 'and', 'surveyed', 'the'], ['fog'], ['above', 'him', 'with', 'an', 'appearance', 'of', 'attentive', 'interest', 'My', 'dear'], ['MC', u'Martin Chuzzlewit', '14', '4', '12', '372', '4671'], ['1811', '4694', '95999', '335750']],
            [['and', 'beholding', 'Mr', 'Tapley', 'more', 'intent', 'than', 'ever', 'on', 'the'], ['fog'], ['it', 'would', 'be', 'strange', 'if', 'I', 'did', 'not', 'for', 'my'], ['MC', u'Martin Chuzzlewit', '14', '10', '21', '801', '4671'], ['1817', '4703', '96428', '335750']],
            [['one', 'near', 'and', 'that', 'Mark', 'was', 'still', 'intent', 'upon', 'the'], ['fog'], ['not', 'only', 'looked', 'at', 'her', 'lips', 'too', 'but', 'kissed', 'them'], ['MC', u'Martin Chuzzlewit', '14', '31', '76', '1622', '4671'], ['1838', '4758', '97249', '335750']],
            [['upon', 'Mark', 'which', 'he', 'brought', 'his', 'eyes', 'down', 'from', 'the'], ['fog'], ['to', 'encounter', 'and', 'received', 'with', 'immense', 'satisfaction', 'She', 'said', 'in'], ['MC', u'Martin Chuzzlewit', '14', '47', '117', '2338', '4671'], ['1854', '4799', '97965', '335750']],
            [['too', 'And', 'a', 'mist', 'upon', 'the', 'Hollow', 'Not', 'a', 'dull'], ['fog'], ['that', 'hides', 'it', 'but', 'a', 'light', 'airy', 'gauzelike', 'mist', 'which'], ['MC', u'Martin Chuzzlewit', '36', '40', '135', '2908', '8861'], ['4716', '11863', '225332', '335750']],
            [['from', 'time', 'to', 'time', 'but', 'all', 'seemed', 'muffled', 'by', 'the'], ['fog'], ['and', 'to', 'be', 'rendered', 'almost', 'as', 'indistinct', 'to', 'the', 'ear'], ['NN', u'Nicholas Nickleby', '22', '2', '5', '259', '6107'], ['2584', '4610', '102739', '321378']],
            [['on', 'amidst', 'the', 'congenial', 'accompaniments', 'of', 'rain', 'mud', 'dirt', 'damp'], ['fog'], ['and', 'rats', 'until', 'late', 'in', 'the', 'day', 'when', 'summoning', 'his'], ['OCS', u'The Old Curiosity Shop', '51', '1', '1', '19', '2246'], ['2671', '6141', '147658', '217447']],
            [['cold', 'and', 'gloomy', 'In', 'that', 'low', 'and', 'marshy', 'spot', 'the'], ['fog'], ['filled', 'every', 'nook', 'and', 'corner', 'with', 'a', 'thick', 'dense', 'cloud'], ['OCS', u'The Old Curiosity Shop', '67', '3', '10', '343', '3370'], ['3655', '8571', '196054', '217447']],
            [['have', 'lost', 'my', 'way', 'in', 'coming', 'here', 'through', 'this', 'thick'], ['fog'], ['Let', 'me', 'dry', 'myself', 'at', 'the', 'fire', 'for', 'five', 'minutes'], ['OCS', u'The Old Curiosity Shop', '67', '17', '43', '941', '3370'], ['3669', '8604', '196652', '217447']],
            [['with', 'his', 'hands', 'it', 'had', 'grown', 'so', 'dark', 'and', 'the'], ['fog'], ['had', 'so', 'much', 'increased', 'he', 'returned', 'to', 'his', 'lair', 'and'], ['OCS', u'The Old Curiosity Shop', '67', '46', '140', '2200', '3370'], ['3698', '8701', '197911', '217447']],
            [['then', 'with', 'torches', 'going', 'on', 'before', 'because', 'of', 'the', 'heavy'], ['fog'], ['But', 'as', 'they', 'get', 'farther', 'from', 'the', 'river', 'and', 'leave'], ['OCS', u'The Old Curiosity Shop', '68', '7', '36', '617', '2707'], ['3722', '8798', '199698', '217447']],
            [['the', 'light', 'of', 'its', 'kilnfires', 'made', 'lurid', 'smears', 'on', 'the'], ['fog'], ['R', 'Wilfer', 'sighed', 'and', 'shook', 'his', 'head', 'Ah', 'me', 'said'], ['OMF', u'Our Mutual Friend', '4', '8', '22', '686', '4703'], ['313', '687', '12740', '326116']],
            [['kitchengarden', 'brick', 'viaduct', 'archspanned', 'canal', 'and', 'disorder', 'of', 'frowziness', 'and'], ['fog'], ['As', 'if', 'the', 'child', 'had', 'given', 'the', 'table', 'a', 'kick'], ['OMF', u'Our Mutual Friend', '18', '31', '86', '1940', '7418'], ['2139', '4903', '85532', '326116']],
            [['It', 'was', 'a', 'foggy', 'day', 'in', 'London', 'and', 'the'], ['fog'], ['was', 'heavy', 'and', 'dark', 'Animate', 'London', 'with', 'smarting', 'eyes', 'and'], ['OMF', u'Our Mutual Friend', '34', '1', '1', '9', '4916'], ['4253', '9858', '166320', '326116']],
            [['for', 'a', 'few', 'moments', 'dimly', 'indicated', 'through', 'circling', 'eddies', 'of'], ['fog'], ['showed', 'as', 'if', 'it', 'had', 'gone', 'out', 'and', 'were', 'collapsing'], ['OMF', u'Our Mutual Friend', '34', '1', '3', '89', '4916'], ['4253', '9860', '166400', '326116']],
            [['surrounding', 'country', 'it', 'was', 'a', 'foggy', 'day', 'but', 'there', 'the'], ['fog'], ['was', 'grey', 'whereas', 'in', 'London', 'it', 'was', 'at', 'about', 'the'], ['OMF', u'Our Mutual Friend', '34', '1', '4', '116', '4916'], ['4253', '9861', '166427', '326116']],
            [['in', 'the', 'counting', 'house', 'window', 'and', 'a', 'burglarious', 'stream', 'of'], ['fog'], ['creeping', 'in', 'to', 'strangle', 'it', 'through', 'the', 'keyhole', 'of', 'the'], ['OMF', u'Our Mutual Friend', '34', '2', '6', '279', '4916'], ['4254', '9863', '166590', '326116']],
            [['of', 'coming', 'out', 'at', 'the', 'door', 'Riah', 'went', 'into', 'the'], ['fog'], ['and', 'was', 'lost', 'to', 'the', 'eyes', 'of', 'Saint', 'Mary', 'Axe'], ['OMF', u'Our Mutual Friend', '34', '3', '8', '326', '4916'], ['4255', '9865', '166637', '326116']],
            [['be', 'some', 'ordinary', 'figure', 'indistinctly', 'seen', 'which', 'fancy', 'and', 'the'], ['fog'], ['had', 'worked', 'into', 'that', 'passing', 'likeness', 'Arrived', 'at', 'the', 'house'], ['OMF', u'Our Mutual Friend', '34', '3', '10', '406', '4916'], ['4255', '9867', '166717', '326116']],
            [['and', 'Lammle', 'strode', 'out', 'pondering', 'Fledgeby', 'saw', 'him', 'into', 'the'], ['fog'], ['and', 'returning', 'to', 'the', 'fire', 'and', 'musing', 'with', 'his', 'face'], ['OMF', u'Our Mutual Friend', '34', '92', '199', '3067', '4916'], ['4344', '10056', '169378', '326116']],
            [['the', 'only', 'sages', 'he', 'believed', 'in', 'besides', 'usurers', 'the', 'murky'], ['fog'], ['closed', 'about', 'him', 'and', 'shut', 'him', 'up', 'in', 'its', 'sooty'], ['OMF', u'Our Mutual Friend', '34', '145', '318', '4876', '4916'], ['4397', '10175', '171187', '326116']],
            [['by', 'that', 'of', 'Westminster', 'and', 'so', 'ever', 'wading', 'through', 'the'], ['fog'], ['waded', 'to', 'the', 'doorstep', 'of', 'the', 'dolls', 'dressmaker', 'Miss', 'Wren'], ['OMF', u'Our Mutual Friend', '35', '1', '3', '71', '4014'], ['4398', '10179', '171298', '326116']],
            [['o', 'purpose', 'With', 'that', 'they', 'began', 'their', 'plodding', 'through', 'the'], ['fog'], ['Yes', 'it', 'was', 'truly', 'sharp', 'of', 'you', 'godmother', 'resumed', 'Miss'], ['OMF', u'Our Mutual Friend', '35', '9', '21', '362', '4014'], ['4406', '10197', '171589', '326116']],
            [['on', 'the', 'fender', 'Its', 'a', 'cold', 'cold', 'night', 'and', 'the'], ['fog'], ['clings', 'so', 'As', 'Miss', 'Abbey', 'helped', 'her', 'to', 'turn', 'her'], ['OMF', u'Our Mutual Friend', '35', '64', '155', '2347', '4014'], ['4461', '10331', '173574', '326116']],
            [['it', 'asked', 'Miss', 'Abbey', 'Its', 'summut', 'run', 'down', 'in', 'the'], ['fog'], ['maam', 'answered', 'Bob', 'Theres', 'ever', 'so', 'many', 'people', 'in', 'the'], ['OMF', u'Our Mutual Friend', '35', '74', '187', '3046', '4014'], ['4471', '10363', '174273', '326116']],
            [['a', 'steamer', 'Miss', 'Abbey', 'cried', 'one', 'blurred', 'figure', 'in', 'the'], ['fog'], ['It', 'always', 'IS', 'a', 'steamer', 'Miss', 'Abbey', 'cried', 'another', 'Thems'], ['OMF', u'Our Mutual Friend', '35', '79', '199', '3218', '4014'], ['4476', '10375', '174445', '326116']],
            [['off', 'her', 'steam', 'Miss', 'Abbey', 'and', 'thats', 'what', 'makes', 'the'], ['fog'], ['and', 'the', 'noise', 'worse', 'dont', 'you', 'see', 'explained', 'another', 'Boats'], ['OMF', u'Our Mutual Friend', '35', '82', '202', '3252', '4014'], ['4479', '10378', '174479', '326116']],
            [['river', 'for', 'every', 'boat', 'that', 'put', 'off', 'sculled', 'into', 'the'], ['fog'], ['and', 'was', 'lost', 'to', 'view', 'at', 'a', 'boats', 'length', 'Nothing'], ['OMF', u'Our Mutual Friend', '35', '83', '207', '3332', '4014'], ['4480', '10383', '174559', '326116']],
            [['manner', 'of', 'all', 'her', 'kind', 'The', 'whole', 'bulk', 'of', 'the'], ['fog'], ['teemed', 'with', 'such', 'taunts', 'uttered', 'in', 'tones', 'of', 'universal', 'hoarseness'], ['OMF', u'Our Mutual Friend', '35', '83', '210', '3432', '4014'], ['4480', '10386', '174659', '326116']],
            [['luminous', 'patch', 'about', 'her', 'as', 'if', 'she', 'had', 'set', 'the'], ['fog'], ['on', 'fire', 'and', 'in', 'the', 'patch', 'the', 'cries', 'changing', 'their'], ['OMF', u'Our Mutual Friend', '35', '83', '213', '3484', '4014'], ['4480', '10389', '174711', '326116']],
            [['by', 'keeping', 'close', 'ward', 'over', 'a', 'long', 'days', 'work', 'in'], ['fog'], ['and', 'rain', 'Silas', 'would', 'have', 'just', 'crawled', 'to', 'bed', 'and'], ['OMF', u'Our Mutual Friend', '64', '3', '11', '265', '4951'], ['8001', '18585', '309175', '326116']],
            [['the', 'reeking', 'bodies', 'of', 'the', 'cattle', 'and', 'mingling', 'with', 'the'], ['fog'], ['which', 'seemed', 'to', 'rest', 'upon', 'the', 'chimneytops', 'hung', 'heavily', 'above'], ['OT', u'Oliver Twist', '21', '4', '14', '415', '2162'], ['1421', '3034', '57493', '157020']],
            [['was', 'soon', 'asleep', 'again', 'It', 'was', 'now', 'intensely', 'dark', 'The'], ['fog'], ['was', 'much', 'heavier', 'than', 'it', 'had', 'been', 'in', 'the', 'early'], ['OT', u'Oliver Twist', '22', '38', '71', '1205', '2465'], ['1499', '3190', '60445', '157020']],
            [['Hunt', 'which', 'wrote', 'other', 'sweet', 'poem', 'what', 'is', 'that', 'name'], ['Fog'], ['Perspiring', 'Fog', 'ver', 'good', 'ver', 'good', 'indeed', 'And', 'the', 'count'], ['PP', u'Pickwick Papers', '15', '127', '211', '3707', '5048'], ['1852', '3744', '75633', '299674']],
            [['wrote', 'other', 'sweet', 'poem', 'what', 'is', 'that', 'name', 'Fog', 'Perspiring'], ['Fog'], ['ver', 'good', 'ver', 'good', 'indeed', 'And', 'the', 'count', 'put', 'up'], ['PP', u'Pickwick Papers', '15', '127', '211', '3709', '5048'], ['1852', '3744', '75635', '299674']],
        ])

    def test_specific_book(self):
        # WS has 33 (because it includes fog-bank)
        fog = self.create_concordance(Materials=["BH"])
        self.assertEqual(len(fog) - correction, 32)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

    def test_specific_corpus(self):
        fog = self.create_concordance(Materials=["ntc"])
        self.assertEqual(len(fog) - correction, 88)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

    def test_quotes(self):
        fog = self.create_concordance(idxName="quote-idx")
        self.assertEqual(len(fog) - correction, 11)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])
        #TODO test whether the results in quotes are really in quotes

    def test_quotes_specific_book(self):
        fog = self.create_concordance(idxName="quote-idx",
                                            Materials=["ED"])
        self.assertEqual(len(fog) - correction, 3)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

    def test_non_quotes(self):
        fog = self.create_concordance(idxName="non-quote-idx")
        # i.e. 11 (test_quotes) + 83 (test_non_quotes) == 94 (test_basic_query)
        self.assertEqual(len(fog) - correction, 83)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

    def test_short_sus(self):
        fog = self.create_concordance(idxName="shortsus-idx")
        self.assertEqual(len(fog) - correction, 0)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

    def test_long_sus(self):
        fog = self.create_concordance(idxName="longsus-idx")
        self.assertEqual(len(fog) - correction, 1)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])

    def test_long_sus(self):
        fog = self.create_concordance(idxName="longsus-idx",
                                      Materials="BH")
        self.assertEqual(len(fog) - correction, 0)
        self.assertEqual(fog[0], len(fog) - correction)
        self.assertEqual(["Fail" for x in fog[1:] if "fog" not in "".join(x[1]).lower()], [])


class PhraseSearchOneTermQuotes(unittest.TestCase):
    pass


class PhraseSearchOneTermNonQuotes(unittest.TestCase):
    pass


class PhraseSearchOneTermShortSus(unittest.TestCase):
    pass


class PhraseSearchOneTermLongSus(unittest.TestCase):
    pass


class OrSearchMultipleTerms(unittest.TestCase):

    def setUp(self):
        self.concordance = Concordance()


    def test_create_concordance(self):
        fog = self.concordance.create_concordance(terms="dense fog",
                                             idxName="chapter-idx",
                                             Materials=["dickens"],
                                             selectWords="any")

        # the only the thing that changes is the order of the terms
        # which should not affect the results
        dense = self.concordance.create_concordance(terms="fog dense",
                                             idxName="chapter-idx",
                                             Materials=["dickens"],
                                             selectWords="any")

        self.assertEqual(fog, dense)


class PhraseSearchMultipleTerms(unittest.TestCase):

    def test_create_concordance(self):
        concordance = Concordance()
        fog = concordance.create_concordance(terms="dense fog",
                                             idxName="chapter-idx",
                                             Materials=["dickens"],
                                             selectWords="whole")

        assert len(fog) - correction == 3


class PhraseSearchOneTermQuoteIndex(unittest.TestCase):

    def test_create_concordance(self):
        """
        This is another naive test focusing on searching in quotes

        It also uses a hard-coded example
        """
        concordance = Concordance()
        maybe = concordance.create_concordance(terms="maybe",
                                             idxName="quote-idx",
                                             Materials=["dickens"],
                                             selectWords="whole")

        assert len(maybe) - correction == 45 # 45 hits + one variable total_count in the list


class OrSearchOneTerm:
    pass

if __name__ == '__main__':
    unittest.main()
