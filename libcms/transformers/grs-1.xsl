<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: grs-1.xsl,v $
 * Revision 1.14  2006/03/06 13:08:16  rustam
 * Minor improvement
 *
 * Revision 1.13  2003/06/25 10:22:48  rustam
 * Zthes supported
 *
 * Revision 1.12  2003/06/21 09:32:17  rustam
 * Processing of some new tags
 *
 * Revision 1.11  2003/05/15 07:27:34  rustam
 * Implemented profiles
 *
 * Revision 1.10  2003/04/08 13:16:33  rustam
 * Minor changes
 *
 * Revision 1.9  2003/01/31 14:11:39  rustam
 * New pre-release
 *
 * Revision 1.8  2002/08/22 15:15:35  rustam
 * Minor changes
 *
 * Revision 1.6  2002/07/22 10:02:12  web
 * Improved follow directive processing
 *
 * Revision 1.5  2002/02/27 07:33:21  web
 * Minor changes
 *
 * Revision 1.4  2001/12/27 16:06:02  web
 * Compliance with ZThes profile
 *
 * Revision 1.3  2001/10/18 09:49:40  web
 * Minor changes
 *
 * Revision 1.2  2001/09/27 09:50:36  web
 * Minor changes
 *
 * Revision 1.1  2001/09/27 09:21:50  web
 * Implemented GRS-1 records presentation via XSLT
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

<xsl:template name="record.grs-1">
   <xsl:choose>
    <xsl:when test="$fmt='M'">
      <xsl:call-template name="dumpgrs"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:variable name="schema">
        <xsl:choose>
          <xsl:when test="tag[@type='1' and @value='1']">
            <xsl:value-of select="tag[@type='1' and @value='1']"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$schemaId"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test="$schema = '1.2.840.10003.13.2'">
          <xsl:call-template name="GILS"/>
        </xsl:when>
        <xsl:when test="$schema = '1.2.840.10003.13.3'">
          <xsl:call-template name="DCol"/>
        </xsl:when>
        <xsl:when test="$schema = '1.2.840.10003.13.5'">
          <xsl:call-template name="CIMI"/>
        </xsl:when>
        <xsl:when test="$schema = '1.2.840.10003.13.8' or $schemaId = '1.2.840.10003.13.1000.136.1'">
          <xsl:call-template name="Zthes"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="generic"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="dumpgrs">
  <xsl:for-each select="tag">
    <span class="fieldlabel">
    <xsl:text>(</xsl:text><xsl:value-of select="@type"/>
    <xsl:text>/</xsl:text><xsl:value-of select="@value"/><xsl:text>)</xsl:text>
    </span>
    <xsl:choose>
      <xsl:when test="count(tag) &gt; 0">
        <div class="ind">
        <xsl:call-template name="dumpgrs"/>
        </div>
      </xsl:when>
      <xsl:otherwise>
        <span class="data"><xsl:value-of select="."/></span>
        <br/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
</xsl:template>

<xsl:template name="GILS">
  <xsl:for-each select="tag">
    <xsl:apply-templates select="."/>
  </xsl:for-each>

  <xsl:for-each select="tag[@type='4' and @value='97']/tag[@type='4' and @value='22']">
    <xsl:if test="position() = 1">
      <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_UST']"/></span>
      <xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <span class="data"><xsl:value-of select="."/></span>
    <xsl:if test="position() = last()">
      <br/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="tag[@type='4' and @value='32']">
    <xsl:if test="position() = 1">
      <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_LANG']"/></span>
      <xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <span class="data"><xsl:value-of select="."/></span>
    <xsl:if test="position() = last()">
      <br/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="tag[@type='4' and @value='70']">
    <xsl:if test="position() = 1">
      <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_AVAILABILITY']"/></span>
      <xsl:text>: </xsl:text>
    </xsl:if>
    <div class="ind">
      <xsl:for-each select="tag[@type='4' and @value='99']">
        <xsl:if test="position() = 1">
          <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_AVAIL_LINKAGE']"/></span>
          <xsl:text>: </xsl:text>
        </xsl:if>
        <div class="ind">
          <xsl:for-each select="tag[@type='4' and @value='17']">
            <xsl:if test="position() = 1">
              <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_LINKAGE']"/></span>
              <xsl:text>: </xsl:text>
              <xsl:if test="position() != 1">
                <xsl:text>, </xsl:text>
              </xsl:if>
              <span class="data"><xsl:call-template name="linkage"/></span>
              <xsl:if test="position() = last()">
                <br/>
              </xsl:if>
            </xsl:if>
          </xsl:for-each>
        </div>
      </xsl:for-each>
      <xsl:for-each select="tag[@type='4' and @value='90']">
        <xsl:if test="position() = 1">
          <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DISTRIBUTOR']"/></span>
          <xsl:text>: </xsl:text>
        </xsl:if>
        <div class="ind">
          <xsl:for-each select="tag">
            <xsl:apply-templates select="."/>
          </xsl:for-each>
        </div>
      </xsl:for-each>
      
    </div>
  </xsl:for-each>
</xsl:template>

<xsl:template name="DCol">
  <xsl:variable name="p" select="tag[@type='4' and @value='4']/tag[@type='4' and @value='14']/tag[@type='4' and @value='29']"/>
  <xsl:call-template name="generic"/>
  <xsl:choose>
    <xsl:when test="$p/tag[@type='1' and @value='1'] = '1.2.840.10003.13.5'">
      <xsl:call-template name="CIMI">
        <xsl:with-param name="oi" select="$p"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="generic"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="CIMI">
  <xsl:param name="oi"/>
  <div class="cimi">
    <xsl:for-each select="$oi/tag[@type='5' and @value='49']">
      <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_CREATOR']"/></span>
      <xsl:text>: </xsl:text>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:for-each>
    <xsl:for-each select="$oi/tag[@type='5' and @value='32']">
      <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_TITLE']"/></span>
      <xsl:text>: </xsl:text>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:for-each>
    <xsl:for-each select="$oi/tag[@type='5' and @value='28']">
      <img title="{../tag[@type='5' and @value='32']}" alt="{../tag[@type='5' and @value='32']}" src="{normalize-space(tag[@type='5' and @value='29']/tag[@type='5' and @value='30'])}"/>
    </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="Zthes">
  <xsl:for-each select="tag[@type='2' and @value='30'][tag[@type='4' and @value='3']='BT']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_BT']"/><xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <a href="{$cgi.script.URL}?follow+{$session.id}+{tag[@type='1' and @value='14']}[1,1.2.840.10003.3.11:4]+{$lang}">
    <xsl:value-of select="tag[@type='2' and @value='1']"/>
    </a>
  </xsl:for-each>

  <h3><xsl:value-of select="tag[@type='2' and @value='1']"/></h3>

  <xsl:for-each select="tag[@type='2' and @value='30'][tag[@type='4' and @value='3']='UF']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_UF']"/><xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <a href="{$cgi.script.URL}?follow+{$session.id}+{tag[@type='1' and @value='14']}[1,1.2.840.10003.3.11:4]+{$lang}">
    <xsl:value-of select="tag[@type='2' and @value='1']"/>
    </a>
    <xsl:if test="position() = last()">
      <p/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="tag[@type='2' and @value='30'][tag[@type='4' and @value='3']='USE']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_USE']"/><xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <a href="{$cgi.script.URL}?follow+{$session.id}+{tag[@type='1' and @value='14']}[1,1.2.840.10003.3.11:4]+{$lang}">
    <xsl:value-of select="tag[@type='2' and @value='1']"/>
    </a>
    <xsl:if test="position() = last()">
      <br/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="tag[@type='2' and @value='30'][tag[@type='4' and @value='3']='LE']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_LE']"/><xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <a href="{$cgi.script.URL}?follow+{$session.id}+{tag[@type='1' and @value='14']}[1,1.2.840.10003.3.11:4]+{$lang}">
    <xsl:value-of select="tag[@type='2' and @value='1']"/>
    </a>
    <xsl:if test="position() = last()">
      <br/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="tag[@type='2' and @value='30'][tag[@type='4' and @value='3']='RT']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_RT']"/><xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <a href="{$cgi.script.URL}?follow+{$session.id}+{tag[@type='1' and @value='14']}[1,1.2.840.10003.3.11:4]+{$lang}">
    <xsl:value-of select="tag[@type='2' and @value='1']"/>
    </a>
    <xsl:if test="position() = last()">
      <p/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="tag[@type='2' and @value='30'][tag[@type='4' and @value='3']='NT']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_NT']"/><xsl:text>: </xsl:text>
    </xsl:if>
    <xsl:if test="position() != 1">
      <xsl:text>, </xsl:text>
    </xsl:if>
    <a href="{$cgi.script.URL}?follow+{$session.id}+{tag[@type='1' and @value='14']}[1,1.2.840.10003.3.11:4]+{$lang}">
    <xsl:value-of select="tag[@type='2' and @value='1']"/>
    </a>
    <xsl:if test="position() = last()">
      <br/>
    </xsl:if>
  </xsl:for-each>
</xsl:template>

<xsl:template name="generic">
  <xsl:for-each select="tag">
    <xsl:apply-templates select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="linkage">
  <xsl:choose> 
    <xsl:when test="starts-with(., 'http://')">
      <a href="{.}"><xsl:value-of select="."/></a>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="."/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='1' and @value='1']">
</xsl:template>

<xsl:template match="tag[@type='4']">
</xsl:template>

<xsl:template match="tag[@type='1' and @value='11']">
  <br/>
  <div class="msg"><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="tag[@type='1' and @value='14']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_LCN']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='1' and @value='16']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DATE_LAST_MOD']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='1' and @value='21']">
</xsl:template>

<xsl:template match="tag[@type='1' and @value='23']">
</xsl:template>

<xsl:template match="tag[@type='2' and @value='1']">
    <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_TITLE']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='2']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_AUTHOR']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='3']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_PLACE_PUB']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='4']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DATE_PUB']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='7']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_NAME']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='8']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DATE_TIME']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='17']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DESCRIPTION']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='19']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DOCUMENT_CONTENT']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='20']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_LANG']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='21']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_SUBJECT']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='23']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_CITY']"/></span>
  <xsl:text>: </xsl:text>
  <span class="data"><xsl:value-of select="."/></span>
  <br/>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='28']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IDENTIFIER']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='29']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_RIGHTS']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='31']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_PUBLISHER']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='33']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_SOURCE']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='2' and @value='34']">
  <span class="fieldlabel"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_COVERAGE']"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="tag[@type='3']">
  <span class="fieldlabel"><xsl:value-of select="@value"/></span>
  <xsl:text>: </xsl:text>
  <xsl:choose>
    <xsl:when test="count(tag) &gt; 0">
      <div class="ind">
      <xsl:apply-templates select="tag"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <span class="data"><xsl:value-of select="."/></span>
      <br/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
