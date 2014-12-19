<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: xml.xsl,v $
 * Revision 1.3  2006/03/06 13:11:38  rustam
 * Further improvements
 *
 * Revision 1.2  2006/02/14 10:00:59  rustam
 * Further improvements
 *
 * Revision 1.1  2005/09/27 07:09:01  rustam
 * Added XML records representation
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:er="http://science.viniti.ru/er/"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:dcterms="http://purl.org/dc/terms/"
	exclude-result-prefixes="rdf dc er xsi dcterms"
>
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>

<xsl:template name="record.xml">
   <xsl:choose>
    <xsl:when test="$fmt='M'">
      <xsl:call-template name="dumpxml"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates select="."/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="rdf:Description">
  <xsl:choose>
    <xsl:when test="$fmt='B'">
      <xsl:apply-templates select="dc:creator"/>
      <xsl:apply-templates select="dc:title"/>
      <xsl:apply-templates select="dc:relation[@xsi:type='dcterms:isPartOf']"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates select="dc:*"/>
      <xsl:apply-templates select="dcterms:*"/>
      <xsl:apply-templates select="er:member"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="dc:title">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_TITLE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:creator">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_CREATOR']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:subject">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_SUBJECT']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:subject[@xsi:type='dcterms:UDC']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:subject[@xsi:type='dcterms:DDC']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_DDC']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:subject[@xsi:type='er:GRNTI']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:description">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_DESCRIPTION']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dcterms:abstract">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DCTERMS_ABSTRACT']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:publisher">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_PUBLISHER']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:contributor">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_CONTRIBUTOR']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:date">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_DATE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:type">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_TYPE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:format">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_FORMAT']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:identifier">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_IDENTIFIER']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data">
  <xsl:choose>
    <xsl:when test="starts-with(., 'http://')or starts-with(., 'ftp://')">
      <a href="{.}"><xsl:value-of select="."/></a>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="."/>
    </xsl:otherwise>
  </xsl:choose>
  </span>
  <br/>
</xsl:template>

<xsl:template match="dc:source">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_SOURCE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data">
  <xsl:choose>
    <xsl:when test="starts-with(., 'http://') or starts-with(., 'ftp://')">
      <a href="{.}"><xsl:value-of select="."/></a>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="."/>
    </xsl:otherwise>
  </xsl:choose>
  </span>
  <br/>
</xsl:template>

<xsl:template match="dc:language">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_LANGUAGE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:relation">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_RELATION']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data">
  <xsl:choose>
    <xsl:when test="starts-with(., 'http://') or starts-with(., 'ftp://')">
      <a href="{.}"><xsl:value-of select="."/></a>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="."/>
    </xsl:otherwise>
  </xsl:choose>
  </span>
  <br/>
</xsl:template>

<xsl:template match="dc:relation[@xsi:type='dcterms:isPartOf']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_SOURCE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:relation[@xsi:type='dcterms:hasPart']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DCTERMS_HASPART']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:coverage">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_COVERAGE']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dc:rights">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DC_RIGHTS']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dcterms:extent">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DCTERMS_EXTENT']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/>
    <xsl:if test="@er:records">
      <xsl:text> </xsl:text>
      <xsl:value-of select="@er:records"/><xsl:text> </xsl:text><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_RECORDS']"/>
    </xsl:if>
    <xsl:if test="@er:size">
      <xsl:text> </xsl:text>
      <xsl:value-of select="@er:size"/><xsl:text> </xsl:text><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_KB']"/>
    </xsl:if>
  </span>
  <br/>
</xsl:template>

<xsl:template match="dcterms:modified">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DCTERMS_MODIFIED']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dcterms:accrualPeriodicity">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DCTERMS_AP']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="dcterms:mediator">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_HOLDER']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data">
    <xsl:call-template name="org.by.code">
      <xsl:with-param name="oname" select="."/>
     </xsl:call-template>
  </span>
  <br/>
</xsl:template>

<xsl:template match="er:member">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_MEMBER']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data">
    <xsl:call-template name="org.by.code">
      <xsl:with-param name="oname" select="."/>
     </xsl:call-template>
  </span>
  <br/>
</xsl:template>

<xsl:template match="er:*"/>

<xsl:template name="dumpxml">
</xsl:template>

</xsl:stylesheet>
