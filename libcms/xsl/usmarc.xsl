<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: usmarc.xsl,v $
 * Revision 1.7  2003/10/20 07:31:40  rustam
 * Improved record representation
 *
 * Revision 1.6  2003/09/30 11:25:39  rustam
 * Minor changes
 *
 * Revision 1.5  2003/04/02 12:22:57  rustam
 * Minor corrections
 *
 * Revision 1.4  2003/01/31 14:11:57  rustam
 * New pre-release
 *
 * Revision 1.3  2002/09/13 07:25:13  rustam
 * Added location representation
 *
 * Revision 1.2  2002/08/27 07:14:32  rustam
 * Changed 856 field representation
 *
 * Revision 1.1  2002/08/14 08:39:58  rustam
 * Reworked stylesheets
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

<xsl:param name="dlm">.&#x2014;</xsl:param>
<!--
USMARC
-->
<xsl:template name="record.usmarc">
  <xsl:choose>
    <xsl:when test="$fmt='M'">
      <xsl:call-template name="dump">
        <xsl:with-param name="r" select="."/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:variable name="bl" select="leader/leader07"/>
      <xsl:choose>
        <xsl:when test="$bl='a' or $bl='b' or $bl='d'">
          <xsl:call-template name="usmain"/>
        </xsl:when>
        <xsl:when test="$bl='m'">
          <xsl:call-template name="usmain"/>
        </xsl:when>
        <xsl:when test="$bl='s'">
          <xsl:call-template name="usmain"/>
        </xsl:when>
        <xsl:when test="$bl='c'">
          <xsl:call-template name="usmain"/>
        </xsl:when>
        <xsl:otherwise>
          <span class="warn"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_IBL']"/><xsl:text>: </xsl:text><xsl:value-of select="$bl"/></span><br/>
          <xsl:call-template name="usmain"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="$fmt='F'">
        <xsl:if test="$subject">
          <xsl:call-template name="M21subjects"/>
        </xsl:if>
        <table width="100%">
        <tr></tr><tr>
        <td align="left" valign="top" class="recsrc">
          <xsl:if test="$record.source">
            <xsl:call-template name="M21int"/>
          </xsl:if>
        </td>
        <td align="right" valign="top">
          <xsl:if test="$class">
            <xsl:call-template name="M21class"/>
          </xsl:if>
        </td>
        </tr>
        </table>
        <xsl:if test="$holdings and count(../../holdingsData) = 0">
          <xsl:apply-templates select="field[@id='852']"/>
        </xsl:if>
        <xsl:for-each select="field[@id='900']">
          <p><xsl:value-of select="subfield[@id='a']"/></p>
        </xsl:for-each>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="M21subjects">
  <p/>
  <xsl:if test="count(field[@id='600']) + count(field[@id='610']) + count(field[@id='650']) + count(field[@id='651']) + count(field[@id='653']) &gt; 0">
    <xsl:text>- -</xsl:text>
  </xsl:if>
  <xsl:for-each select="field[@id='600']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="position()"/>
    <xsl:text>. </xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='610']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="position() + count(../field[@id='600'])"/>
    <xsl:text>. </xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='650']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="position() + count(../field[@id='600']) + count(../field[@id='610'])"/>
    <xsl:text>. </xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='651']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="position() + count(../field[@id='600']) + count(../field[@id='610']) + count(../field[@id='650'])"/>
    <xsl:text>. </xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text> - </xsl:text>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='653']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="position() + count(../field[@id='600']) + count(../field[@id='610']) + count(../field[@id='650']) + count(../field[@id='651'])"/>
    <xsl:text>. </xsl:text>
    <xsl:for-each select="subfield[@id='a']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
</xsl:template>

<xsl:template name="M21class">
  <xsl:for-each select="field[@id='080']">
    <xsl:if test="position() = 1">
       <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='082']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_DDC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='050']">
    <xsl:if test="position() = 1">
        <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LCC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:value-of select="subfield[@id='b']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='084']">
    <xsl:if test="position() = 1">
      <xsl:variable name="csystem" select="subfield[@id='2']"/>
      <xsl:choose>
        <xsl:when test="$csystem='rubbk'">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LBC']"/><xsl:text> </xsl:text>
        </xsl:when>
        <xsl:when test="$csystem='rugasnti'">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_GASNTI']"/><xsl:text> </xsl:text>
        </xsl:when>
        <xsl:when test="$csystem='rueskl'">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_ESKL']"/><xsl:text> </xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$csystem"/><xsl:text> </xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="M21int">
  <xsl:if test="count(field[@id='040']) &gt; 0">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="field[@id='040']/subfield[@id='a']"/>
  </xsl:call-template>
  <xsl:text> </xsl:text>
  </xsl:if>
  <xsl:if test="count(field[@id='005']) &gt; 0">
    <xsl:variable name="date" select="field[@id='005']"/>
    <xsl:value-of select="substring($date, 7, 2)"/><xsl:text>.</xsl:text>
    <xsl:value-of select="substring($date, 5, 2)"/><xsl:text>.</xsl:text>
    <xsl:value-of select="substring($date, 1, 4)"/>
  </xsl:if>
</xsl:template>

<xsl:template name="usmain">
  <b>
  <xsl:if test="count(field[@id='100']) &gt; 0">
    <xsl:value-of select="field[@id='100']/subfield[@id='a']"/>
  </xsl:if>
  <xsl:if test="count(field[@id='110']) &gt; 0">
    <xsl:value-of select="field[@id='110']/subfield[@id='a']"/>
      <xsl:for-each select="field[@id='110']/subfield[@id='b']">
        <xsl:text>. </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
  </xsl:if>
  <xsl:text> </xsl:text>
  </b>
  
  <xsl:apply-templates select="field[@id='245']"/>
  <xsl:if test="count(field[@id='773']) &gt; 0">
    <xsl:text> // </xsl:text><xsl:value-of select="field[@id='773']/subfield[@id='t']"/>
    <xsl:if test="count(field[@id='773']/subfield[@id='d']) &gt; 0">
      <xsl:value-of select="$dlm"/>
      <xsl:value-of select="field[@id='773']/subfield[@id='d']"/>
    </xsl:if>
    <xsl:if test="count(field[@id='773']/subfield[@id='g']) &gt; 0">
      <xsl:value-of select="$dlm"/>
      <xsl:value-of select="field[@id='773']/subfield[@id='g']"/>
    </xsl:if>
    <xsl:if test="count(field[@id='773']/subfield[@id='x']) &gt; 0">
      <xsl:value-of select="$dlm"/><xsl:text>ISSN </xsl:text>
      <xsl:value-of select="field[@id='773']/subfield[@id='x']"/>
    </xsl:if>
  </xsl:if>

  <xsl:apply-templates select="field[@id='250']"/>

  <xsl:apply-templates select="field[@id='260']"/>

  <xsl:apply-templates select="field[@id='300']"/>
  
  <xsl:apply-templates select="field[@id='440']"/>

  <xsl:apply-templates select="field[@id='490']"/>

  <xsl:for-each select="field[@id='500']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='501']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='502']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='504']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='505']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='506']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:if test="count(field[@id='507']/subfield[@id='a']) &gt; 0">
    <xsl:value-of select="$dlm"/><xsl:value-of select="field[@id='507']/subfield[@id='a']"/>
  </xsl:if>
  <xsl:if test="count(field[@id='508']/subfield[@id='a']) &gt; 0">
    <xsl:value-of select="$dlm"/><xsl:value-of select="field[@id='508']/subfield[@id='a']"/>
  </xsl:if>
  <xsl:for-each select="field[@id='510']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='511']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='513']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:if test="count(field[@id='514']/subfield[@id='a']) &gt; 0">
    <xsl:value-of select="$dlm"/><xsl:value-of select="field[@id='514']/subfield[@id='a']"/>
  </xsl:if>
  <xsl:for-each select="field[@id='515']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='516']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='518']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:if test="$abstract">
    <xsl:for-each select="field[@id='520']">
      <xsl:text>.</xsl:text>
      <p class="note">
      <xsl:value-of select="subfield[@id='a']"/>
      </p>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="field[@id='521']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='522']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='524']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='525']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='526']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='530']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='533']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='534']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='535']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  </xsl:for-each>
  
  <xsl:if test="count(field[@id='020']) &gt; 0">
    <xsl:if test="count(field[@id='020']/subfield[@id='a']) &gt; 0">
      <xsl:value-of select="$dlm"/><xsl:text>ISBN </xsl:text><xsl:value-of select="field[@id='020']/subfield[@id='a']"/>
    </xsl:if>
    <xsl:if test="count(field[@id='020']/subfield[@id='c']) &gt; 0">
      <xsl:value-of select="field[@id='020']/subfield[@id='c']"/>
    </xsl:if>
  </xsl:if>

  <xsl:call-template name="M21.856"/>
  <xsl:text>.</xsl:text>
  
</xsl:template>

<xsl:template match="field[@id='245']">
  <xsl:value-of select="subfield[@id='a']"/>
  <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='b']"/>
  <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='c']"/>
</xsl:template>

<xsl:template match="field[@id='250']">
  <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='b']"/>
</xsl:template>

<xsl:template match="field[@id='260']">
  <xsl:value-of select="$dlm"/>
  <xsl:for-each select="subfield[@id='a']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='b']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='c']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='300']">
  <xsl:value-of select="$dlm"/>
  <xsl:for-each select="subfield[@id='a']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='b']"/>
  <xsl:for-each select="subfield[@id='c']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='440']">
  <xsl:value-of select="$dlm"/><xsl:text>(</xsl:text><xsl:value-of select="subfield[@id='a']"/>
  <xsl:for-each select="subfield[@id='n']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='p']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:value-of select="subfield[@id='v']"/>
  <xsl:if test="count(subfield[@id='x']) &gt; 0">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='x']"/>
  </xsl:if>
  <xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="field[@id='490']">
  <xsl:value-of select="$dlm"/><xsl:text>(</xsl:text><xsl:value-of select="subfield[@id='a']"/>
  <xsl:for-each select="subfield[@id='n']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='p']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:value-of select="subfield[@id='v']"/>
  <xsl:if test="count(subfield[@id='x']) &gt; 0">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='x']"/>
  </xsl:if>
  <xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="field[@id='852']">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="subfield[@id='a']"/>
  </xsl:call-template>
  <xsl:for-each select="subfield[@id='b']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='c']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="count(subfield[@id='h']) &gt; 0">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='h']"/>
  </xsl:if>
  <xsl:for-each select="subfield[@id='i']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="count(subfield[@id='j']) &gt; 0">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='j']"/>
  </xsl:if>
  <xsl:if test="count(subfield[@id='p']) &gt; 0">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='p']"/>
  </xsl:if>
  <xsl:if test="count(subfield[@id='t']) &gt; 0">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='t']"/>
  </xsl:if>
  <xsl:for-each select="subfield[@id='z']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <br/>
</xsl:template>

<xsl:template name="M21.856">
  <xsl:for-each select="field[@id='856']">
    <xsl:for-each select="subfield[@id='u']">
      <xsl:text> </xsl:text><xsl:value-of select="$dlm"/><xsl:text> &lt;URL:</xsl:text><a href="{.}"><xsl:value-of select="."/></a><xsl:text>&gt;</xsl:text>
    </xsl:for-each>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
