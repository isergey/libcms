<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>
<xsl:key name="nk" match="holdingsAndCirc/nucCode" use="."/>
<xsl:key name="lk" match="holdingsAndCirc/localLocation" use="."/>


<xsl:include href="marc-eposd.xsl"/>

<!--
<xsl:param name="fmt" select="'B'"/>
<xsl:param name="lang" select="'eng'"/>
-->

<xsl:template name="record.opac">
  <xsl:for-each select="bibliographicRecord/record">
    <xsl:call-template name="record.selector"/>
  </xsl:for-each>
  <xsl:if test="$fmt = 'F'">
    <xsl:apply-templates select="holdingsData"/>
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
        <xsl:for-each select="holdingsAndCirc[generate-id(nucCode)=generate-id(key('nk', nucCode))]">
          <xsl:apply-templates select="nucCode"/>
          <xsl:variable name="n" select="nucCode"/>
          <xsl:for-each select="../holdingsAndCirc[nucCode=$n and generate-id(localLocation)=generate-id(key('lk', localLocation))]">
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
