<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:exsl="http://exslt.org/common"
	exclude-result-prefixes="exsl"> 
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>
<xsl:key name="nk" match="nucCode" use="concat(generate-id(../../..), '-', .)"/>
<xsl:key name="lk" match="localLocation" use="concat(generate-id(../../..), '-', .)"/>
<xsl:key name="mk" match="field[@id='999']/subfield[@id='p']" use="."/>


<xsl:include href="marc.xsl"/>

<!--
<xsl:param name="fmt" select="'B'"/>
<xsl:param name="lang" select="'eng'"/>
-->

<xsl:template name="record.opac">
  <xsl:for-each select="bibliographicRecord/record">
    <xsl:call-template name="record.selector">
      <xsl:with-param name="class" select="'opacbr'"/>
    </xsl:call-template>
  </xsl:for-each>
  <xsl:if test="$fmt = 'F'">
    <xsl:choose>
      <xsl:when test="not(holdingsData/holdingsAndCirc) and $opac.holdings.reconstruction">
        <xsl:variable name="h">
          <holdingsData>
          <xsl:for-each select="bibliographicRecord/record/field[@id='999'][generate-id(subfield[@id='p'])=generate-id(key('mk', subfield[@id='p']))]">
            <holdingsAndCirc>
              <nucCode><xsl:value-of select="subfield[@id='a']"/></nucCode>
              <localLocation><xsl:value-of select="subfield[@id='b']"/></localLocation>
              <callNumber><xsl:value-of select="subfield[@id='p']"/></callNumber>
              <shelvingData><xsl:value-of select="subfield[@id='h']"/><xsl:text> </xsl:text><xsl:value-of select="subfield[@id='i']"/></shelvingData>
              <circulationData>
                <xsl:for-each select="../field[@id='999' and subfield[@id='p'] = current()/subfield[@id='p']]/subfield[@id='y']">
                <circRecord>
                  <availableNow>1</availableNow>
                  <itemId><xsl:value-of select="."/></itemId>
                  <renewable>1</renewable>
                  <onHold>0</onHold>
                </circRecord>
                </xsl:for-each>
              </circulationData>
            </holdingsAndCirc>
          </xsl:for-each>
          </holdingsData>
        </xsl:variable>
        <xsl:apply-templates select="exsl:node-set($h)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="holdingsData"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:if>
</xsl:template>

<xsl:template match="holdingsData">
  <table class="location">
    <caption>
    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_HOLDINGS']"/>
    </caption>
    <tr>
      <th class="location"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_LOCAL_LOC']"/></th>
      <th class="location"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ITEMS_TOTAL']"/></th>
      <th class="location"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ITEMS_AVAIL']"/></th>
      <th class="location"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_CALL_NUM']"/></th>
      <th class="location"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_SH_DATA']"/></th>
    </tr>
    <xsl:choose>
      <xsl:when test="holdingsAndCirc">
        <xsl:for-each select="holdingsAndCirc[generate-id(nucCode)=generate-id(key('nk', concat(generate-id(../..), '-', nucCode)))]">
          <xsl:apply-templates select="nucCode"/>
          <xsl:variable name="n" select="nucCode"/>
          <xsl:for-each select="../holdingsAndCirc[nucCode=$n and generate-id(localLocation)=generate-id(key('lk', concat(generate-id(../..), '-', localLocation)))]">
            <xsl:variable name="l" select="localLocation"/>
            <tr>
            <xsl:apply-templates select="localLocation"/>
            <td class="location">
              <xsl:if test="../holdingsAndCirc[nucCode=$n][localLocation=$l]/circulationData/circRecord">
                <xsl:value-of select="count(../holdingsAndCirc[nucCode=$n][localLocation=$l]/circulationData/circRecord)"/>
              </xsl:if>
            </td>
            <td class="location">
              <xsl:if test="../holdingsAndCirc[nucCode=$n][localLocation=$l]/circulationData/circRecord">
                <xsl:value-of select="count(../holdingsAndCirc[nucCode=$n][localLocation=$l]/circulationData/circRecord[availableNow='1'])"/>
              </xsl:if>
            </td>
            <td class="location">
              <xsl:for-each select="../holdingsAndCirc[nucCode=$n][localLocation=$l][circulationData/circRecord/availableNow='1']">
                <xsl:if test="position() != 1"><xsl:text>, </xsl:text></xsl:if>
                <xsl:value-of select="callNumber"/>
              </xsl:for-each>
            </td>
            <td class="location">
              <xsl:value-of select="../holdingsAndCirc[nucCode=$n][localLocation=$l][circulationData/circRecord/availableNow='1'][1]/shelvingData"/>
            </td>
            </tr>
          </xsl:for-each>
        </xsl:for-each>
      </xsl:when>
      <xsl:otherwise>
        <xsl:for-each select="record">
          <tr><td colspan="5" class="location"><xsl:apply-templates select="."/></td></tr>
        </xsl:for-each>
      </xsl:otherwise>
    </xsl:choose>
  </table>
</xsl:template>

<xsl:template match="nucCode">
  <tr><td colspan="5" class="location">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="."/>
  </xsl:call-template>
  </td></tr>
</xsl:template>

<xsl:template match="localLocation">
  <td class="location">
  <xsl:call-template name="unit.by.code">
    <xsl:with-param name="uname" select="."/>
  </xsl:call-template>
  </td>
</xsl:template>

</xsl:stylesheet>
