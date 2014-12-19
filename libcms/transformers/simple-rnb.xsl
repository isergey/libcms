<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: simple.xsl,v $
 * Revision 1.1  2003/05/15 07:27:39  rustam
 * Implemented profiles
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:import href="param_rnb.xsl"/>
<xsl:import href="form.xsl"/>
<xsl:import href="zgate.xsl"/>

<xsl:param name="include.dialog" select="false()"/>
<xsl:param name="include.help" select="true()"/>
<xsl:param name="include.structure.attrs" select="false()"/>
<xsl:param name="sort" select="false()"/>

<xsl:param name="pa" select="document('attr_simple.xml')"/>

<xsl:param name="modes">
  <mode href="extended-rnb.xsl" label="I_EXTENDED"/>
</xsl:param>

</xsl:stylesheet>
