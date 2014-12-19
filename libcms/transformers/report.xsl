<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: report.xsl,v $
 * Revision 1.1  2003/09/30 11:27:17  rustam
 * Implemented resource control
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>
<xsl:template match="res">
<script type="text/javascript">
<xsl:for-each select="report/estimates/estimate">
  <xsl:text>p = document.getElementById('EST_</xsl:text><xsl:value-of select="@type"/><xsl:text>');</xsl:text>
  <xsl:text>p.value='</xsl:text><xsl:value-of select="@value"/>
  <xsl:if test="@type = '12'">
    <xsl:text>%</xsl:text>
  </xsl:if>
  <xsl:text>';</xsl:text>
</xsl:for-each>
</script>
</xsl:template>

<!--
<xsl:template match="res">
var s;
<xsl:for-each select="report/estimates/estimate">
s = '';
  <xsl:if test="@type='12'">
s += 'a:' + <xsl:value-of select="@value"/> + '%';
  </xsl:if>
  <xsl:if test="@type='1'">
s += ' b:' + <xsl:value-of select="@value"/>;
  </xsl:if>
window.status = s;
</xsl:for-each>
</xsl:template>
-->

</xsl:stylesheet>
