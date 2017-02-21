Chapter View
============

The chapter view relies on a series of XSLT transformers created that process our search results and highlight the selected term. The transformer is loaded in to the cheshire installation as part of the provisioning/bootstrap script and is part of the liveconfig.xml file.

```
<!-- clic/dbs/dickens/xsl/chapterView.xsl -->
<subConfig type="transformer" id="chapterView-Txr">
    <objectType>cheshire3.transformer.LxmlXsltTransformer</objectType>
    <paths>
        <path type="xsltPath">xsl/chapterView.xsl</path>
    </paths>
</subConfig>
```

The transformer takes the XML returned from cheshires underlying technology and then turns it into the html you find on a chapter view page. This is currently responsible for the highlighting in yellow of the search term and work was being carried out to make it highlight all identical terms. Though this was proving tricky via the pure xslt route.
