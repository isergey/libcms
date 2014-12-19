<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: record.xsl,v $
 * Revision 1.1  2004/05/21 09:51:53  rustam
 * *** empty log message ***
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
<xsl:include href="param.xsl"/>
<xsl:include href="zgate.xsl"/>

<xsl:template match="record">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html;charset={$charset}"/>
      <link href="{$stylesheet.URL}" rel="stylesheet" type="text/css"/>
    </head>
    <body>
    <xsl:call-template name="record.selector"/>
    </body>
  </html>
</xsl:template>

</xsl:stylesheet>
