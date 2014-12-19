<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: extended.xsl,v $
 * Revision 1.1  2003/05/15 07:27:31  rustam
 * Implemented profiles
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:import href="params_mesh.xsl"/>
<xsl:import href="form.xsl"/>
<xsl:import href="zgate.xsl"/>

<xsl:param name="dedup" select="true()"/>
<xsl:param name="query.expansion" select="false()"/>
<xsl:param name="include.help" select="true()"/>
<xsl:param name="include.dialog" select="false()"/>
<xsl:param name="include.recsyn.list" select="true()"/>
<xsl:param name="simplify.recsyn.list" select="true()"/>
<xsl:param name="include.relation.attrs" select="true()"/>

<xsl:param name="marc.labels" select="true()"/>
<xsl:param name="marc.download" select="false()"/>

<xsl:param name="pa" select="document('attr_extended.xml')"/>

<xsl:param name="modes">
  <mode href="simplem.xsl" label="I_SIMPLE"/>
</xsl:param>

</xsl:stylesheet>
