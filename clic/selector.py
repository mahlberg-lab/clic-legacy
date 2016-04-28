from cheshire3.selector import SimpleSelectorfrom copy import deepcopy
from lxml import etree
import re

    # <subConfig type="selector" id="quoteExcludeSpanSelector">    #     <objectType>clic.selector.ExcludeSpanSelector</objectType>
    #     <source>
    #         <xpath>p</xpath>  <!-- get these -->
    #     </source>
    #     <source>
    #         <xpath>qs</xpath>  <!-- start exluding from these -->
    #         <xpath>qe</xpath>  <!-- and stop excluding at these -->
    #     </source>
    # </subConfig>


class ExcludeSpanSelector(SimpleSelector):
    def __init__(self, session, config, parent):        self.sources = []
        SimpleSelector.__init__(self, session, config, parent)
        # One primary source, one start and end exclusion source        
        if len(self.sources) != 2:
            raise ConfigFileException("ExcludeSpanSelector '{0}' requires exactly 3 XPaths".format(self.id))

    def process_record(self, session, record):        vals = []

        # deepcopy it to avoid breaking the record        for xp in self.sources[0]:
            vals.extend(deepcopy(record.process_xpath(session, xp['string'], xp['maps'])))

        startPath = self.sources[1][0]['string']        startMaps = self.sources[1][0]['maps']

        if not startPath.startswith('/'):            # Not absolute path, prepend //
            startPath = '//{0}'.format(startPath)

        endPath = self.sources[1][1]['string']        endMaps = self.sources[1][1]['maps']

        if not endPath.startswith('/'):            # Not absolute path, prepend //
            endPath = '//{0}'.format(endPath)
    
        trashing = False

        for tree in vals:            # Find all of the start and endnodes
            startNodes = tree.xpath(startPath, namespaces=startMaps)
            endNodes = tree.xpath(endPath, namespaces=endMaps)

            for elem in tree.iter():                if elem in startNodes:
                    # start trashing
                    trashing = True
                    elem.tail = None
                elif elem in endNodes:
                	trashing = False
                elif trashing:                  
                    elem.text = None
                    elem.tail = None

        return vals