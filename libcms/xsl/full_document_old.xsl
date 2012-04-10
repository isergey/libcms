<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="marc"> 
<xsl:include href="rusmarc.xsl"/>
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>

<xsl:param name="lang" select="'rus'"/>
<xsl:param name="fmt" select="'F'"/>
<xsl:param name="start" select="1"/>
<xsl:param name="ht" select="false()"/>
<xsl:param name="abstract" select="false()"/>
<xsl:param name="subject" select="false()"/>
<xsl:param name="class" select="false()"/>
<xsl:param name="record.source" select="false()"/>
<xsl:param name="holdings" select="false()"/>
<xsl:param name="syntax" select="'RUSmarc'"/>
<xsl:param name="org" select="''"/>
<xsl:param name="msg" select="''"/>
<xsl:param name="process_holdings" select="false()"/>

<!--
MARC
-->
<xsl:template name="dump">
  <xsl:param name="r"/>
  <xsl:param name="break" select="true()"/>
  <xsl:for-each select="datafield | controlfield">
    <xsl:variable name="label" select="@id"/>
    <span class="fieldlabel"><xsl:value-of select="$label"/></span>
    <xsl:choose>
      <xsl:when test="@ind1 or @ind2">
        <xsl:variable name="i1" select="@ind1"/>
        <xsl:variable name="i2" select="@ind2"/>
        <span class="indicator">
          <xsl:value-of select="translate($i1, ' ', '#')"/>
          <xsl:value-of select="translate($i2, ' ', '#')"/>
        </span>
        <xsl:for-each select="subfield">
          <span class="subfieldlabel"><xsl:text>$</xsl:text><xsl:value-of select="@id"/></span>
          <xsl:choose>
            <xsl:when test="datafield or controlfield">
              <xsl:call-template name="dump">
                <xsl:with-param name="r" select="datafield"/>
                <xsl:with-param name="break" select="false()"/>
              </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <xsl:variable name="data" select="."/>
              <span class="data">
              <xsl:choose>
                <xsl:when test="substring($label, 1, 1)='1'">
                  <xsl:value-of select="translate($data, ' ', '#')"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="$data"/>
                </xsl:otherwise>
              </xsl:choose>
              </span>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </xsl:when>
      <xsl:otherwise>
        <span class="data"><xsl:value-of select="."/></span>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="$break">
      <br/>
    </xsl:if>
  </xsl:for-each>
</xsl:template>

<xsl:template name="org.by.code">
  <xsl:param name="oname"/>
  <xsl:choose>
    <xsl:when test="$org/organizations/localization[@language=$lang]/org[@id=$oname]">
      <xsl:choose>
        <xsl:when test="$process_holdings">
          <a href="javascript:setValue('{$org/organizations/localization[@language=$lang]/org[@id=$oname]/@id}');">
            <xsl:value-of select="$org/organizations/localization[@language=$lang]/org[@id=$oname]"/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$org/organizations/localization[@language=$lang]/org[@id=$oname]"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$oname"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="record">
  <xsl:choose>
    <xsl:when test="$syntax = 'RUSmarc'">
      <xsl:call-template name="record.rusmarc"/>
    </xsl:when>
  </xsl:choose>
  <xsl:choose>
    <xsl:when test="$fmt = 'B'">
      <div><xsl:text>[</xsl:text>
      <a href="sb.php?start={position() div 2 + $start -1}&amp;ps=1&amp;esname=F">&gt;&gt;</a>
      <xsl:text>]</xsl:text></div>
    </xsl:when>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
