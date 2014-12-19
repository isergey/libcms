<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: marc.xsl,v $
 * Revision 1.9  2010/11/03 10:59:04  rustam
 * Linking from organisation ID
 *
 * Revision 1.8  2004/07/01 07:02:23  rustam
 * Improved fixed-length fields representation
 *
 * Revision 1.7  2004/05/18 10:12:20  rustam
 * Errors corrected
 *
 * Revision 1.6  2004/04/29 10:00:28  rustam
 * Added human-readable country names representation
 *
 * Revision 1.5  2004/03/03 09:04:51  rustam
 * Added MARC record leader representation
 *
 * Revision 1.4  2003/05/15 07:27:35  rustam
 * Implemented profiles
 *
 * Revision 1.3  2002/09/24 09:02:05  rustam
 * Better organizational units representation
 *
 * Revision 1.2  2002/09/23 09:38:09  rustam
 * Added support for localLocation representation
 *
 * Revision 1.1  2002/08/14 08:39:52  rustam
 * Reworked stylesheets
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:include href="rusmarc.xsl"/>
<xsl:include href="usmarc.xsl"/>
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>

<!--
MARC
-->
<xsl:template name="dump">
  <xsl:param name="r"/>
  <xsl:param name="break" select="true()"/>
  <xsl:variable name="stx" select="@syntax"/>
  <span class="data"><xsl:for-each select="leader/*"><xsl:value-of select="translate(., ' ', '#')"/></xsl:for-each></span><br/>
  <xsl:for-each select="field">
    <xsl:variable name="label" select="@id"/>
    <span class="fieldlabel"><xsl:value-of select="$label"/></span>
    <xsl:choose>
      <xsl:when test="indicator">
        <xsl:variable name="i1" select="indicator[@id='1']"/>
        <xsl:variable name="i2" select="indicator[@id='2']"/>
        <span class="indicator">
          <xsl:value-of select="translate($i1, ' ', '#')"/>
          <xsl:value-of select="translate($i2, ' ', '#')"/>
        </span>
        <xsl:for-each select="subfield">
          <span class="subfieldlabel"><xsl:text>$</xsl:text><xsl:value-of select="@id"/></span>
          <xsl:choose>
            <xsl:when test="field">
              <xsl:call-template name="dump">
                <xsl:with-param name="r" select="field"/>
                <xsl:with-param name="break" select="false()"/>
              </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <xsl:variable name="data" select="."/>
              <span class="data">
              <xsl:choose>
                <xsl:when test="substring($label, 1, 1)='1' and
($stx='1.2.840.10003.5.1' or $stx='Unimarc' or $stx='1.2.840.10003.5.28' or $stx='RUSmarc')">
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

<xsl:template name="country.by.code">
  <xsl:param name="cname"/>
  <xsl:choose>
    <xsl:when test="$country/countries/localization[@language=$lang]/country[@id=$cname]">
      <xsl:value-of select="$country/countries/localization[@language=$lang]/country[@id=$cname]"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$cname"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="org.by.code">
  <xsl:param name="oname"/>
  <xsl:choose>
    <xsl:when test="$org/organizations/localization[@language=$lang]/org[@id=$oname]">
      <xsl:choose>
        <xsl:when test="string-length($org.link.URL) &gt; 0">
          <a href="{$org.link.URL}{$oname}"><xsl:value-of select="$org/organizations/localization[@language=$lang]/org[@id=$oname]"/></a>
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

<xsl:template name="unit.by.code">
  <xsl:param name="uname"/>
  <xsl:choose>
    <xsl:when test="$units/units/localization[@language=$lang]/unit[@id=$uname]">
      <xsl:value-of select="$units/units/localization[@language=$lang]/unit[@id=$uname]"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$uname"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
