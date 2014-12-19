<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>
<xsl:param name="extra.template" select="true()"/>
<xsl:param name="extra.header" select="'Достоверность'"/>
<xsl:param name="extra.js" select="'/js/slider.js'"/>

<xsl:template name="extra">
<td>
<br/>
<br/>
<br/>
<hr class="slider" id="ruler"/>
<div class="slider" id="slider" onMouseDown="dragStart(event); return false;"/>
<span class="slider" id="min">min</span>
<span class="slider" id="max">max</span>
</td>
</xsl:template>

</xsl:stylesheet>
