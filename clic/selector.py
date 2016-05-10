from cheshire3.selector import SimpleSelector
from lxml import etree
import re

    # <subConfig type="selector" id="quoteExcludeSpanSelector">
    #     <source>
    #         <xpath>p</xpath>  <!-- get these -->
    #     </source>
    #     <source>
    #         <xpath>qs</xpath>  <!-- start exluding from these -->
    #         <xpath>qe</xpath>  <!-- and stop excluding at these -->
    #     </source>
    # </subConfig>


class ExcludeSpanSelector(SimpleSelector):
    def __init__(self, session, config, parent):
        SimpleSelector.__init__(self, session, config, parent)
        # One primary source, one start and end exclusion source        
        if len(self.sources) != 2:
            raise ConfigFileException("ExcludeSpanSelector '{0}' requires exactly 3 XPaths".format(self.id))

    def process_record(self, session, record):

        # deepcopy it to avoid breaking the record
            vals.extend(deepcopy(record.process_xpath(session, xp['string'], xp['maps'])))

        startPath = self.sources[1][0]['string']

        if not startPath.startswith('/'):
            startPath = '//{0}'.format(startPath)

        endPath = self.sources[1][1]['string']

        if not endPath.startswith('/'):
            endPath = '//{0}'.format(endPath)
    
        trashing = False

        for tree in vals:
            startNodes = tree.xpath(startPath, namespaces=startMaps)
            endNodes = tree.xpath(endPath, namespaces=endMaps)

            for elem in tree.iter():
                    # start trashing
                    trashing = True
                    elem.tail = None
                elif elem in endNodes:
                	trashing = False
                elif trashing:                  
                    elem.text = None
                    elem.tail = None

        return vals