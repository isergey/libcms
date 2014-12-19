<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: expand.xsl,v $
 * Revision 1.6  2007/03/01 14:30:57  rustam
 * Improved personal name expansion
 *
 * Revision 1.5  2004/04/22 06:58:39  rustam
 * Corrected bugs
 *
 * Revision 1.4  2003/10/31 13:02:21  rustam
 * Minor corrections
 *
 * Revision 1.3  2002/08/28 11:01:21  rustam
 * Minor changes
 *
 * Revision 1.2  2002/04/08 11:55:58  rustam
 * Minor changes
 *
 * Revision 1.1  2001/09/27 09:22:22  web
 * Improved query expansion
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output
	method="text"
	indent="no"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>

<xsl:param name="term" select="''"/>
<xsl:param name="attr" select="''"/>

<xsl:variable name="nterm" select="normalize-space($term)"/>

<xsl:template match="record[@syntax='1.2.840.10003.5.28']">
<!--
  <xsl:for-each select="field[@id='210']">
    <xsl:for-each select="subfield[@id='b']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
  </xsl:for-each>
  <xsl:for-each select="field[@id='215']">
    <xsl:for-each select="subfield[@id='x']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
  </xsl:for-each>
  <xsl:for-each select="field[@id='220']">
    <xsl:for-each select="subfield[@id='x']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
  </xsl:for-each>
  <xsl:for-each select="field[@id='230']">
    <xsl:for-each select="subfield[@id='x']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
  </xsl:for-each>
  <xsl:for-each select="field[@id='235']">
    <xsl:for-each select="subfield[@id='x']">
      <xsl:if test=". = $nterm">
        <xsl:for-each select="../subfield[@id='a']">
          <xsl:value-of select="."/>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
  </xsl:for-each>
-->
  <xsl:for-each select="field[@id='200'] | field[@id='400'] |
	field[@id='210'] | field[@id='410'] |
	field[@id='250'] | field[@id='450']">
    <xsl:apply-templates select="subfield[@id='a']"/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="subfield[@id='a']">
  <xsl:if test=". = $nterm">
    <xsl:for-each select="../../field[@id='210'] | ../../field[@id='410'] |
	../../field[@id='250'] | ../../field[@id='450']">
      <xsl:for-each select="subfield[@id='a']">
        <xsl:value-of select="."/><xsl:text>&#10;</xsl:text>
      </xsl:for-each>
    </xsl:for-each>
    <xsl:for-each select="../../field[@id='200'] | ../../field[@id='400']">
      <xsl:value-of select="subfield[@id='a']"/>
      <xsl:choose>
        <xsl:when test="subfield[@id='g']">
          <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='g']"/>
        </xsl:when>
        <xsl:when test="subfield[@id='b']">
          <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='b']"/>
        </xsl:when>
      </xsl:choose>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="../../field[@id='510'] |
			 ../../field[@id='550']">
      <xsl:if test="substring(subfield[@id='5'], 1, 1) != 'h'">
        <xsl:for-each select="subfield[@id='a']">
          <xsl:value-of select="."/><xsl:text>&#10;</xsl:text>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
    <xsl:for-each select="../../field[@id='500']">
      <xsl:if test="substring(subfield[@id='5'], 1, 1) != 'h'">
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:choose>
          <xsl:when test="subfield[@id='g']">
            <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='g']"/>
          </xsl:when>
          <xsl:when test="subfield[@id='b']">
            <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='b']"/>
          </xsl:when>
        </xsl:choose>
        <xsl:text>&#10;</xsl:text>
      </xsl:if>
    </xsl:for-each>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
