<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="marc"> 
	<xsl:include href="param.xsl"/>
	<xsl:include href="marc.xsl"/>
	<xsl:output
		method="html"
		indent="yes"
		encoding="utf-8"
		standalone="no"
		omit-xml-declaration="yes"
	/>



	<xsl:template match="record">
		<xsl:call-template name="record.selector"/>
	</xsl:template>


	<xsl:template name="record.selector">
	  <xsl:param name="hideable" select="false()"/>
	  <xsl:param name="class" select="'record'"/>
	  <xsl:element name="div">
	  <xsl:choose>
	    <xsl:when test="@syntax='1.2.840.10003.5.1' or @syntax='Unimarc'">
	      <xsl:attribute name="class"><xsl:value-of select="$class"/></xsl:attribute>
	      <xsl:if test="$class='record'">
		<xsl:attribute name="id"><xsl:value-of select="field[@id='001']"/></xsl:attribute>
	      </xsl:if>
	      <xsl:call-template name="record.rusmarc"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.10' or @syntax='USmarc'">
	      <xsl:attribute name="class"><xsl:value-of select="$class"/></xsl:attribute>
	      <xsl:if test="$class='record'">
		<xsl:attribute name="id"><xsl:value-of select="field[@id='001']"/></xsl:attribute>
	      </xsl:if>
	      <xsl:call-template name="record.usmarc"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.28' or @syntax='RUSmarc'">
	      <xsl:attribute name="class"><xsl:value-of select="$class"/></xsl:attribute>
	      <xsl:if test="$class='record'">
		<xsl:attribute name="id"><xsl:value-of select="field[@id='001']"/></xsl:attribute>
	      </xsl:if>
	      <xsl:call-template name="record.rusmarc"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.101' or @syntax='SUTRS'">
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:call-template name="record.sutrs"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.102' or @syntax='OPAC'">
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:attribute name="id"><xsl:value-of select="bibliographicRecord/record/field[@id='001']"/></xsl:attribute>
	      <xsl:call-template name="record.opac"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.105' or @syntax='GRS-1'">
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:call-template name="record.grs-1"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.106' or @syntax='Extended' or eSTaskPackage"> <!-- esTaskPackage - temporary workaround -->
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:call-template name="record.estp"/>
	    </xsl:when>
	    <xsl:when test="@syntax='1.2.840.10003.5.109.10' or @syntax='XML'">
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:call-template name="record.xml"/>
	    </xsl:when>
	    <xsl:when test="@syntax='incorrect'">
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:call-template name="record.incorrect"/>
	    </xsl:when>
	    <xsl:when test="@syntax='NOT_UTF8'">
	      <xsl:attribute name="class">record</xsl:attribute>
	      <xsl:call-template name="record.not.utf8"/>
	    </xsl:when>
	    <xsl:when test="@syntax='diagnostic'">
	      <xsl:call-template name="record.diagnostic">
		<xsl:with-param name="hideable" select="$hideable"/>
	      </xsl:call-template>
	    </xsl:when>
	    <xsl:otherwise>
	      <span class="warn">
		<xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='W_REC_UNKNOWN']"/>
		<xsl:text>: </xsl:text>
		<xsl:value-of select="@syntax"/>
	      </span>
	    </xsl:otherwise>
	  </xsl:choose>
	  </xsl:element>
	</xsl:template>							
</xsl:stylesheet>
