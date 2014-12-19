<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml"/>

    <!--<xsl:template match="/">
        <add>
            <xsl:for-each select="record">
                <xsl:apply-templates select="record"/>
            </xsl:for-each>
        </add>
    </xsl:template>-->


    <xsl:output indent="yes" method="xml" version="1.0" encoding="UTF-8"/>

    <!-- disable all default text node output -->
    <xsl:template match="text()"/>

    <xsl:template match="/">
        <xsl:if test="collection">
            <collection>
                <xsl:apply-templates select="collection/record"/>
            </collection>
        </xsl:if>
        <xsl:if test="record">
            <xsl:apply-templates select="record"/>
        </xsl:if>
    </xsl:template>

    <!-- match on marcxml record -->
    <xsl:template match="record">
        <doc>
            <xsl:call-template name="bib1_rules"/>
        </doc>
    </xsl:template>
    <xsl:template name="bib1_rules">
        <!-- att 1               Personal-name -->
        <!-- att 2               Corporate-name -->
        <!-- att 3               Conference-name -->
        <!-- att 4               Title -->
        <xsl:call-template name="Title"/>
        <!-- att 5               Title-series -->
        <!-- att 6               Title-uniform -->
        <!-- att 7               ISBN -->
        <!-- <xsl:call-template name="ISBN"/>-->
        <!-- att 8               ISSN -->
        <!-- <xsl:call-template name="ISSN"/>-->
        <!-- att 9               LC-card-number -->
        <!-- att 10              BNB-card-number -->
        <!-- att 11              BGF-number -->
        <!-- att 12              Local-number -->
        <xsl:call-template name="Local-number"/>
        <!-- att 13              Dewey-classification -->
        <!-- att 14              UDC-classification -->
        <!-- att 15              Bliss-classification -->
        <!-- att 16              LC-call-number -->
        <!-- att 17              NLM-call-number -->
        <!-- att 18              NAL-call-number -->
        <!-- att 19              MOS-call-number -->
        <!-- att 20              Local-classification -->
        <!-- att 21              Subject-heading -->
        <!-- <xsl:call-template name="Subject-heading"/>-->
        <!-- att 22              Subject-Rameau -->
        <!-- att 23              BDI-index-subject -->
        <!-- att 24              INSPEC-subject -->
        <!-- att 25              MESH-subject -->
        <!-- att 26              PA-subject -->
        <!-- att 27              LC-subject-heading -->
        <!-- att 28              RVM-subject-heading -->
        <!-- att 29              Local-subject-index -->
        <!-- att 30              Date -->
        <!-- att 31              Date-of-publication -->
        <!-- att 32              Date-of-acquisition -->
        <!-- att 33              Title-key -->
        <!-- att 34              Title-collective -->
        <!-- att 35              Title-parallel -->
        <!-- att 36              Title-cover -->
        <!-- att 37              Title-added-title-page -->
        <!-- att 38              Title-caption -->
        <!-- att 39              Title-running -->
        <!-- att 40              Title-spine -->
        <!-- att 41              Title-other-variant -->
        <!-- att 42              Title-former -->
        <!-- att 43              Title-abbreviated -->
        <!-- att 44              Title-expanded -->
        <!-- att 45              Subject-precis -->
        <!-- att 46              Subject-rswk -->
        <!-- att 47              Subject-subdivision -->
        <!-- att 48              Number-natl-biblio -->
        <!-- att 49              Number-legal-deposit -->
        <!-- att 50              Number-govt-pub -->
        <!-- att 51              Number-music-publisher -->
        <!-- att 52              Number-db -->
        <!-- att 53              Number-local-call -->
        <!-- att 54              Code-language -->
        <!-- att 55              Code-geographic -->
        <!-- att 56              Code-institution -->
        <!-- att 57              Name-and-title -->
        <!-- att 58              Name-geographic -->
        <!-- att 59              Place-publication -->
        <xsl:call-template name="Place-publication"/>
        <!-- att 60              CODEN -->
        <!-- att 61              Microform-generation -->
        <!-- att 62              Abstract -->
        <!-- <xsl:call-template name="Abstract"/>-->
        <!-- att 63              Note -->
        <!-- att 1000            Author-title -->
        <!-- <xsl:call-template name="Author-title"/>-->
        <!-- att 1001            Record-type -->
        <!-- att 1002            Name -->
        <!-- att 1003            Author -->
        <!-- <xsl:call-template name="Author"/>-->
        <!-- att 1004            Author-name-personal -->
        <!-- <xsl:call-template name="Author-name-personal"/>-->
        <!-- att 1005            Author-name-corporate -->
        <!-- <xsl:call-template name="Author-name-corporate"/>-->
        <!-- att 1006            Author-name-conference -->
        <!-- <xsl:call-template name="Author-name-conference"/>-->
        <!-- att 1007            Identifier-standard -->
        <!-- att 1008            Subject-LC-childrens -->
        <!-- att 1009            Subject-name-personal -->
        <!-- att 1010            Body-of-text -->
        <!-- att 1011            Date/time-added-to-db -->
        <!-- att 1012            Date/time-last-modified -->
        <!-- att 1013            Authority/format-id -->
        <!-- att 1014            Concept-text -->
        <!-- att 1015            Concept-reference -->
        <!-- att 1016            Any -->
        <!-- att 1017            Server-choice -->
        <!-- att 1018            Publisher -->
        <!-- att 1019            Record-source -->
        <!-- att 1020            Editor -->
        <!-- att 1021            Bib-level -->
        <!-- att 1022            Geographic-class -->
        <!-- att 1023            Indexed-by -->
        <!-- att 1024            Map-scale -->
        <!-- att 1025            Music-key -->
        <!-- att 1026            Related-periodical -->
        <!-- att 1027            Report-number -->
        <!-- att 1028            Stock-number -->
        <!-- att 1030            Thematic-number -->
        <!-- att 1031            Material-type -->
        <!-- att 1032            Doc-id -->
        <!-- att 1033            Host-item -->
        <!-- att 1034            Content-type -->
        <!-- att 1035            Anywhere -->
        <!-- att 1036            Author-Title-Subject -->
    </xsl:template>


    <xsl:template name="facets">

    </xsl:template>


    <xsl:template name="Place-publication">
        <xsl:for-each select="field[@id='210']/subfield[@id='a']">
            <field name="place-publication_s">
                <xsl:value-of select="."/>
            </field>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="Title">
        <xsl:for-each select="field[@id='200']/subfield[@id='a']">
            <field name="title_t">
                <xsl:value-of select="."/>
            </field>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="Local-number">
        <xsl:for-each select="field[@id='001']">
            <field name="id">
                <xsl:value-of select="."/>
            </field>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>

