<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: rusmarc.xsl,v $
 * Revision 1.59  2013/08/21 13:14:13  rustam
 * Another scheme for monograph's part support
 *
 * Revision 1.58  2013/02/20 13:12:29  rustam
 * Process enclosed links fore serials and analytics
 *
 * Revision 1.57  2012/05/21 10:49:59  rustam
 * Improved header representation
 *
 * Revision 1.56  2012/03/24 06:37:43  rustam
 * Overdue documents highlighting
 *
 * Revision 1.55  2011/06/14 13:00:27  rustam
 * Do not show links from header and subjects for task packages and records from circulation DB
 *
 * Revision 1.54  2011/05/30 11:03:07  rustam
 * Representation of field 604
 *
 * Revision 1.53  2011/05/16 07:37:16  rustam
 * RUSMARC changes - bib.level 'i'
 *
 * Revision 1.52  2011/04/28 05:30:54  rustam
 * Conditional translation with PVM
 *
 * Revision 1.51  2010/12/17 14:32:25  rustam
 * interface redesign
 *
 * Revision 1.50  2010/09/17 08:40:50  rustam
 * 606$z processing changed
 *
 * Revision 1.49  2010/05/06 16:53:34  rustam
 * Tatar translation
 *
 * Revision 1.48  2009/09/10 10:48:09  rustam
 * Resolved enclosed links conflict
 *
 * Revision 1.47  2009/07/15 10:39:28  rustam
 * Implemented hyperlink on 610$b
 *
 * Revision 1.46  2009/04/14 08:19:45  rustam
 * Improved (?) record representation
 *
 * Revision 1.45  2009/03/12 13:41:24  rustam
 * Added processing of field 206
 *
 * Revision 1.44  2008/09/25 12:53:56  rustam
 * Implemented bibliographic record's header linking
 *
 * Revision 1.43  2008/09/11 13:35:27  rustam
 * Output of field 605
 * Output of field 462 for monographs
 *
 * Revision 1.42  2008/05/27 11:34:43  rustam
 * Linking attributes are parameterized
 *
 * Revision 1.41  2008/01/25 12:31:36  rustam
 * Improved 856 field representation
 *
 * Revision 1.40  2007/10/29 09:26:57  rustam
 * Improved record representation
 *
 * Revision 1.39  2007/10/29 09:04:51  rustam
 * Improved record representation (title)
 *
 * Revision 1.38  2007/05/23 08:50:36  rustam
 * Personal name header representation improved
 *
 * Revision 1.37  2007/04/28 12:45:11  rustam
 * Improved record representation
 *
 * Revision 1.36  2007/04/27 13:15:18  rustam
 * Corrected representation of classification indices
 *
 * Revision 1.35  2007/03/01 13:28:33  rustam
 * Improved record representation
 *
 * Revision 1.34  2006/12/13 07:42:54  rustam
 * Minor improvements
 *
 * Revision 1.33  2006/12/12 14:11:53  rustam
 * Improved embedded fields representation
 *
 * Revision 1.32  2006/12/11 13:56:34  rustam
 * Improved embedded fields representation?
 *
 * Revision 1.31  2006/10/19 12:18:55  rustam
 * Corrected bug with classification indices representation
 *
 * Revision 1.30  2006/06/08 08:40:38  rustam
 * Minor improvements
 *
 * Revision 1.29  2006/04/05 07:30:35  rustam
 * Corrected bug with 700$c
 *
 * Revision 1.28  2006/03/06 13:10:43  rustam
 * Improved subject linking
 *
 * Revision 1.27  2005/09/27 07:09:49  rustam
 * Improved subjects representation
 *
 * Revision 1.26  2005/09/07 11:39:25  rustam
 * Improved record representations (multivolume standards)
 *
 * Revision 1.25  2005/05/05 04:49:03  rustam
 * Minor corrections
 *
 * Revision 1.24  2005/03/22 12:23:40  rustam
 * Corrected pagination for analytics from monograph
 *
 * Revision 1.23  2004/12/10 07:47:51  rustam
 * Minor improvements
 *
 * Revision 1.22  2004/09/27 10:11:26  rustam
 * *** empty log message ***
 *
 * Revision 1.21  2004/09/23 09:52:12  rustam
 * Repeated series delimited now with no .-
 *
 * Revision 1.20  2004/07/01 07:03:02  rustam
 * Conformance to GOST 7.1-2003
 *
 * Revision 1.19  2004/06/04 08:01:28  rustam
 * Minor changes
 *
 * Revision 1.18  2004/05/18 10:12:25  rustam
 * Errors corrected
 *
 * Revision 1.17  2004/04/29 09:59:50  rustam
 * Minor changes
 *
 * Revision 1.16  2004/04/22 06:59:09  rustam
 * 229 field representation added
 *
 * Revision 1.15  2004/04/06 06:19:34  rustam
 * Minor changes
 *
 * Revision 1.14  2004/02/26 08:18:54  rustam
 * Can hide record warnings (bib. level) now
 *
 * Revision 1.13  2003/12/25 12:38:43  rustam
 * Minor changes
 *
 * Revision 1.12  2003/11/24 13:31:34  rustam
 * Enumeration
 *
 * Revision 1.11  2003/10/20 07:39:27  rustam
 * Minor improvements
 *
 * Revision 1.10  2003/10/20 07:31:38  rustam
 * Improved record representation
 *
 * Revision 1.9  2003/09/30 11:25:38  rustam
 * Minor changes
 *
 * Revision 1.8  2003/05/15 07:27:38  rustam
 * Implemented profiles
 *
 * Revision 1.7  2003/04/16 08:21:33  rustam
 * Minor changes
 *
 * Revision 1.6  2003/04/08 13:17:01  rustam
 * Added hyperlinks creation for subjects
 *
 * Revision 1.5  2003/02/25 10:25:18  rustam
 * Minor changes
 *
 * Revision 1.4  2003/01/31 14:11:52  rustam
 * New pre-release
 *
 * Revision 1.3  2002/10/28 09:56:19  rustam
 * Minor changes
 *
 * Revision 1.2  2002/10/18 09:44:11  rustam
 * Standards representation
 *
 * Revision 1.1  2002/08/14 08:39:56  rustam
 * Reworked stylesheets
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:include href="authority.xsl"/>
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>

<!--
RUSMARC
-->
<xsl:param name="dash">&#x2014;</xsl:param> <!-- m-dash -->
<xsl:param name="dlm"> .&#x2014; </xsl:param>

<xsl:key name="class" match="record/field[@id='686']/subfield[@id='2']" use="."/>
<xsl:key name="link" match="record/field[@id='421' and indicator[@id='2'] = 1]
	| record/field[@id='422' and indicator[@id='2'] = 1]
	| record/field[@id='423' and indicator[@id='2'] = 1]
	| record/field[@id='430' and indicator[@id='2'] = 1]
	| record/field[@id='431' and indicator[@id='2'] = 1]
	| record/field[@id='432' and indicator[@id='2'] = 1]
	| record/field[@id='433' and indicator[@id='2'] = 1]
	| record/field[@id='434' and indicator[@id='2'] = 1]
	| record/field[@id='435' and indicator[@id='2'] = 1]
	| record/field[@id='436' and indicator[@id='2'] = 1]
	| record/field[@id='437' and indicator[@id='2'] = 1]
	| record/field[@id='440' and indicator[@id='2'] = 1]
	| record/field[@id='441' and indicator[@id='2'] = 1]
	| record/field[@id='442' and indicator[@id='2'] = 1]
	| record/field[@id='443' and indicator[@id='2'] = 1]
	| record/field[@id='444' and indicator[@id='2'] = 1]
	| record/field[@id='445' and indicator[@id='2'] = 1]
	| record/field[@id='446' and indicator[@id='2'] = 1]
	| record/field[@id='448' and indicator[@id='2'] = 1]
	| record/field[@id='451' and indicator[@id='2'] = 1]
	| record/field[@id='452' and indicator[@id='2'] = 1]
	| record/field[@id='453' and indicator[@id='2'] = 1]
	| record/field[@id='454' and indicator[@id='2'] = 1]
	| record/field[@id='455' and indicator[@id='2'] = 1]
	| record/field[@id='456' and indicator[@id='2'] = 1]
	| record/field[@id='470' and indicator[@id='2'] = 1]
	| record/field[@id='481' and indicator[@id='2'] = 1]
	| record/field[@id='482' and indicator[@id='2'] = 1]
	| record/field[@id='488' and indicator[@id='2'] = 1]"
	use="concat(generate-id(..), @id)"/>

<xsl:template name="record.rusmarc">
  <xsl:choose>
    <xsl:when test="$fmt='M'">
      <xsl:call-template name="dump">
        <xsl:with-param name="r" select="."/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:variable name="bl" select="leader/leader07"/>
      <xsl:variable name="type" select="leader/type"/>
      <xsl:choose>
        <xsl:when test="$type='x' or $type='y' or $type='z'">
          <!-- Authority record -->
          <xsl:call-template name="authority"/>
        </xsl:when>
        <xsl:otherwise>
          <!-- Bibliographic record -->
          <!--<xsl:if test="field[@id='856']/subfield[@id='x'] = $cover">
            <img src="{field[@id='856' and subfield[@id='x'] = $cover]/subfield[@id='u']}" align="left" hspace="5"/>
          </xsl:if>-->
          <xsl:choose>
            <xsl:when test="$bl='a'">
              <xsl:call-template name="analytics"/>
            </xsl:when>
            <xsl:when test="$bl='m'">
              <xsl:call-template name="monograph"/>
            </xsl:when>
            <xsl:when test="$bl='s'">
              <xsl:call-template name="serial"/>
            </xsl:when>
            <xsl:when test="$bl='c'">
              <xsl:call-template name="monograph"/>
            </xsl:when>
            <xsl:when test="$bl='i'">
              <xsl:call-template name="monograph"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:choose>
                <xsl:when test="$hide.record.warnings">
                  <a class="warn" title="{$msg/messages/localization[@language=$lang]/msg[@id='F_IBL']}: '{$bl}'"><xsl:text>*</xsl:text></a>
                </xsl:when>
                <xsl:otherwise>
                  <span class="warn"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_IBL']"/><xsl:text>: '</xsl:text><xsl:value-of select="$bl"/><xsl:text>'</xsl:text></span>
                </xsl:otherwise>
              </xsl:choose>
              <br/>
              <xsl:call-template name="monograph"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="$fmt='F'">
        <xsl:if test="$subject">
          <xsl:call-template name="subjects"/>
        </xsl:if>
        <table width="100%">
        <tr></tr><tr>
        <td align="left" valign="top" class="recsrc">
          <xsl:if test="$record.source">
            <xsl:call-template name="int"/>
          </xsl:if>
        </td>
        <td align="right" valign="top">
        <xsl:if test="not($type='x' or $type='y' or $type='z') and $class">
          <xsl:call-template name="class"/>
        </xsl:if>
        </td>
        </tr>
        </table>
        <xsl:if test="$holdings and count(../../holdingsData) = 0">
          <xsl:apply-templates select="field[@id='850']"/>
          <xsl:apply-templates select="field[@id='899']"/>
        </xsl:if>
      </xsl:if>
      <xsl:apply-templates select="field[@id='999']/subfield[@id='z']"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="gen">
  <xsl:param name="r" select="/.."/>
  <xsl:param name="s" select="/.."/>
  <xsl:param name="pub" select="'all'"/>
  <xsl:param name="na" select="true()"/>
  <xsl:param name="enclosed_link" select="false()"/>
  <xsl:if test="$na">
    <xsl:call-template name="header">
      <xsl:with-param name="p" select="$r/subfield[@id='1']"/>
      <xsl:with-param name="enclosed_link" select="$enclosed_link"/>
    </xsl:call-template>
  </xsl:if>
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="$r/subfield[@id='1']/field[@id='200']"/>
    <xsl:with-param name="s2" select="$s"/>
    <xsl:with-param name="show.v" select="false()"/>
  </xsl:call-template>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='205']"/>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='206']"/>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='229']"/>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='230']"/>
  <xsl:choose>
    <xsl:when test="$pub='all'">
      <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='210']"/>
    </xsl:when>
    <xsl:when test="$pub='place' and $r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
      <xsl:value-of select="$dlm"/>
      <xsl:for-each select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
        <xsl:choose>
          <xsl:when test="position() = 1">
            <xsl:value-of select="."/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text> ; </xsl:text><xsl:value-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
      <xsl:if test="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
        <xsl:choose>
          <xsl:when test="$r/../leader/leader07='s'">
            <xsl:text> (</xsl:text><xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/><xsl:text>)</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$dlm"/><xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='215']"/>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='225']"/>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='010']"/>
  <xsl:if test="$na">
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='011']"/>
    <xsl:apply-templates select="$s/subfield[@id='1']/field[@id='011']"/>
  </xsl:if>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='856']"/>
  <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template name="spec">
  <xsl:param name="pub" select="'all'"/>
  <xsl:param name="show_author" select="true()"/>
  <xsl:call-template name="header">
    <xsl:with-param name="show_author" select="$show_author"/>
  </xsl:call-template>
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="field[@id='200']"/>
  </xsl:call-template>
  <xsl:apply-templates select="field[@id='205']"/>
  <xsl:apply-templates select="field[@id='206']"/>
  <xsl:apply-templates select="field[@id='207']"/>
  <xsl:apply-templates select="field[@id='229']"/>
  <xsl:apply-templates select="field[@id='230']"/>
  <xsl:apply-templates select="field[@id='210']"/>
  <xsl:apply-templates select="field[@id='215']"/>
  <xsl:apply-templates select="field[@id='225']"/>

  <xsl:call-template name="notes"/>

  <xsl:if test="$fmt != 'B' and field[@id='464']">
    <p><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_CONTENTS']"/></p>
    <xsl:for-each select="field[@id='464']">
      <xsl:choose>
        <xsl:when test="subfield[@id='1']/field[@id='001'] and $ht">
          <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="."/>
          </xsl:call-template>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="."/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
      <br/>
    </xsl:for-each>
    <p/>
  </xsl:if>
  <xsl:call-template name="links"/>

  <xsl:apply-templates select="field[@id='010']"/>
  <xsl:apply-templates select="field[@id='011']"/>
  <xsl:apply-templates select="field[@id='856']"/>
  <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template name="header">
  <xsl:param name="enclosed_link" select="false()"/>
  <xsl:param name="show_author" select="true()"/>
  <xsl:param name="p" select="."/>
  <xsl:choose>
    <xsl:when test="$p/field[@id='029']/indicator[@id='1'] = 1">
      <div class="armr_header">
      <xsl:call-template name="std">
        <xsl:with-param name="p" select="$p"/>
      </xsl:call-template>
      </div>
    </xsl:when>
    <xsl:when test="$show_author and $p/field[@id='700' or @id='710']">
      <xsl:variable name="h1">
        <xsl:apply-templates select="$p/field[@id='700']"/>
      </xsl:variable>
      <xsl:variable name="h2">
        <xsl:apply-templates select="$p/field[@id='710']"/>
      </xsl:variable>
      <div class="armr_header">
        <xsl:choose>
          <xsl:when test="$follow.header and not($enclosed_link) and not(//record[@syntax='1.2.840.10003.5.106']) and //database != $circ.db">
            <xsl:if test="string-length($h1) &gt; 0">
              <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={$h1}{$personal.author.attrs}&amp;LANG={$lang}"><xsl:value-of select="$h1"/></a>
            </xsl:if>
            <xsl:if test="string-length($h2) &gt; 0">
              <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={$h2}{$corporate.author.attrs}&amp;LANG={$lang}"><xsl:value-of select="$h2"/></a>
            </xsl:if>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$h1"/>
            <xsl:value-of select="$h2"/>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="substring($h1, string-length($h1), 1) != '.' and substring($h2, string-length($h2), 1) != '.' and string-length($h1)+string-length($h2) &gt; 0">
          <xsl:text>.</xsl:text>
        </xsl:if>
      </div>
    </xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template name="std">
  <xsl:param name="p" select="."/>
  <xsl:for-each select="$p/field[@id='029']">
    <xsl:if test="indicator[@id='1'] = 1">
      <xsl:if test="position() = 2">
        <xsl:text> (</xsl:text>
      </xsl:if>
      <xsl:if test="position() &gt; 2">
        <xsl:text>, </xsl:text>
      </xsl:if>

      <xsl:value-of select="subfield[@id='c']"/>
      <xsl:for-each select="subfield[@id='b']">
        <xsl:choose>
          <xsl:when test="position() = 1">
            <xsl:text> </xsl:text><xsl:value-of select="."/>
            <xsl:if test="../indicator[@id='2'] = 3">
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_ET_AL']"/>
            </xsl:if>
          </xsl:when>
          <xsl:when test="position() &gt;= 2 and ../indicator[@id='2'] = 1">
            <xsl:text>, </xsl:text><xsl:value-of select="."/>
          </xsl:when>
          <xsl:when test="position() = 2 and ../indicator[@id='2'] = 2">
            <xsl:value-of select="$dash"/><xsl:value-of select="."/>
          </xsl:when>
        </xsl:choose>
      </xsl:for-each>
      <xsl:if test="subfield[@id='a'] and contains(substring(../field[@id='105'], 4, 4), 'k')">
        <xsl:text> </xsl:text>
        <xsl:call-template name="country.by.code">
          <xsl:with-param name="cname" select="subfield[@id='a']"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>

      <xsl:if test="position() = last() and position() &gt; 1">
        <xsl:text>)</xsl:text>
      </xsl:if>
    </xsl:if>
  </xsl:for-each>
  <xsl:text>. </xsl:text>
</xsl:template>

<xsl:template name="sub">
  <xsl:if test="field[@id='463']">
    <p><table>
    <xsl:for-each select="field[@id='463']">
      <tr><td>
      <xsl:choose>
        <xsl:when test="subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
          <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="."/>
            <xsl:with-param name="pub" select="'year'"/>
          </xsl:call-template>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="."/>
            <xsl:with-param name="pub" select="'year'"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
      </td></tr>
    </xsl:for-each>
    </table></p>
  </xsl:if>
</xsl:template>

<xsl:template name="issue">
  <xsl:param name="year" select="true()"/>
  <xsl:if test="subfield[@id='1']/field[@id='210']/subfield[@id='d'] and $year">
    <xsl:value-of select="subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
    <xsl:if test="subfield[@id='1']/field[@id='200']">
      <xsl:value-of select="$dlm"/>
    </xsl:if>
  </xsl:if>
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="subfield[@id='1']/field[@id='200']"/>
  </xsl:call-template>
</xsl:template>

<xsl:template name="htitle">
  <xsl:param name="r" select="/.."/>
  <xsl:for-each select="$r/subfield[@id='1']/field[@id='200']">
    <xsl:call-template name="title">
      <xsl:with-param name="s1" select="."/>
      <xsl:with-param name="show.v" select="false()"/>
    </xsl:call-template>
  </xsl:for-each>
  <xsl:value-of select="$dlm"/>
  <xsl:for-each select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
    <xsl:choose>
      <xsl:when test="position() = 1">
        <xsl:value-of select="."/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text> ; </xsl:text><xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
  <xsl:text>, </xsl:text>
  <xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
  <xsl:if test="$r/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
    <xsl:value-of select="$dlm"/>
    <xsl:value-of select="$r/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
  </xsl:if>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='225']"/>
</xsl:template>

<!-- Derived from template for field 200 -->
<xsl:template name="title">
  <xsl:param name="s1" select="/.."/>
  <xsl:param name="s2" select="/.."/>
  <xsl:param name="show.v" select="true()"/>
  <xsl:if test="$s1/../../../leader/leader07 = 'm' and $show.v">
    <xsl:for-each select="$s1/subfield[@id='v']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
      <xsl:text>: </xsl:text>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="$s1/subfield[@id='a']">
    <xsl:if test="position() != 1">
       <xsl:text>; </xsl:text>
    </xsl:if>
    <xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="$s2/subfield[@id='1']/field[@id='200']">
    <xsl:text>. </xsl:text>
    <xsl:call-template name="title">
      <xsl:with-param name="s1" select="."/>
      <xsl:with-param name="show.v" select="$show.v"/>
    </xsl:call-template>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='b']">
    <xsl:text> [</xsl:text><xsl:value-of select="."/><xsl:text>]</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='d']">
    <xsl:text> = </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='e']">
    <xsl:text> : </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='h']">
    <xsl:text>. </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='i']">
    <xsl:text>. </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="$s1/subfield[@id='f'] or $s1/subfield[@id='g']">
    <xsl:text> / </xsl:text>
    <xsl:for-each select="$s1/subfield[@id='f']">
      <xsl:choose>
        <xsl:when test="position() = 1">
          <xsl:value-of select="."/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text> ; </xsl:text><xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='g']">
      <xsl:text> ; </xsl:text><xsl:value-of select="."/>
    </xsl:for-each>
  </xsl:if>
  <xsl:if test="$s1/../../../leader/leader07 = 'a' and $show.v">
    <xsl:for-each select="$s1/subfield[@id='v']">
      <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
    </xsl:for-each>
  </xsl:if>
</xsl:template>

<xsl:template name="monograph">
  <xsl:choose>
    <xsl:when test="field[@id='461']/subfield[@id='1']">
      <!-- Have link to upper-level record -->
<!--
      <xsl:variable name="volnum" select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
-->
      <xsl:variable name="volnum">
        <xsl:choose>
          <xsl:when test="field[@id='462']/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
            <xsl:value-of select="field[@id='462']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:variable name="havetitle" select="field[@id='200']/indicator[@id='1']"/>
      <xsl:choose>
        <xsl:when test="field[@id='461']/subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
          <a href="{$cgi.script.URL}?follow+{$session.id}+{field[@id='461']/subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
          <xsl:call-template name="gen">
            <xsl:with-param name="enclosed_link" select="true()"/>
            <xsl:with-param name="r" select="field[@id='461']"/>
            <xsl:with-param name="s" select="field[@id='462']"/>
          </xsl:call-template>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="field[@id='461']"/>
            <xsl:with-param name="s" select="field[@id='462']"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
      <p>
      <xsl:if test="string-length($volnum) &gt; 0 and $havetitle='1'">
        <xsl:value-of select="$volnum"/><xsl:text>: </xsl:text>
      </xsl:if>
      <xsl:call-template name="spec">
        <xsl:with-param name="pub" select="'all'"/>
        <xsl:with-param name="show_author" select="false()"/>
      </xsl:call-template>
      </p>
    </xsl:when>
    <xsl:otherwise>
      <!-- Have no link to upper-level record -->
      <xsl:call-template name="spec"/>
      <xsl:for-each select="field[@id='463']">
        <p>
        <xsl:choose>
          <xsl:when test="subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
            <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
            <xsl:call-template name="gen">
              <xsl:with-param name="r" select="."/>
              <xsl:with-param name="pub" select="'year'"/>
            </xsl:call-template>
            </a>
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="gen">
              <xsl:with-param name="r" select="."/>
              <xsl:with-param name="pub" select="'year'"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
        </p>
      </xsl:for-each>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="serial">
  <xsl:choose>
    <xsl:when test="field[@id='461']/subfield[@id='1']">
      <xsl:variable name="volnum">
        <xsl:choose>
          <xsl:when test="field[@id='462']/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
            <xsl:value-of select="field[@id='462']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:variable name="havetitle" select="field[@id='200']/indicator[@id='1']"/>
      <xsl:choose>
        <xsl:when test="field[@id='461']/subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
          <a href="{$cgi.script.URL}?follow+{$session.id}+{field[@id='461']/subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
          <xsl:call-template name="gen">
            <xsl:with-param name="enclosed_link" select="true()"/>
            <xsl:with-param name="r" select="field[@id='461']"/>
            <xsl:with-param name="s" select="field[@id='462']"/>
          </xsl:call-template>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="field[@id='461']"/>
            <xsl:with-param name="s" select="field[@id='462']"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
      <p>
      <xsl:if test="string-length($volnum) &gt; 0 and $havetitle='1'">
        <xsl:value-of select="$volnum"/><xsl:text> : </xsl:text>
      </xsl:if>
      <xsl:call-template name="spec">
        <xsl:with-param name="pub" select="'year'"/>
      </xsl:call-template>
      <xsl:call-template name="sub"/>
      </p>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="spec"/>
      <xsl:call-template name="sub"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="analytics">
  <xsl:call-template name="header"/>
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="field[@id='200']"/>
  </xsl:call-template>
  <xsl:apply-templates select="field[@id='205']"/>
  <xsl:apply-templates select="field[@id='229']"/>
  <xsl:apply-templates select="field[@id='230']"/>
  <xsl:text> // </xsl:text>
  <xsl:choose>
    <xsl:when test="field[@id='461']/subfield[@id='1']">
      <xsl:variable name="pub">
        <xsl:choose>
          <xsl:when test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">place</xsl:when>
          <xsl:otherwise>all</xsl:otherwise>
        </xsl:choose>
      </xsl:variable>

      <xsl:choose>
        <xsl:when test="field[@id='461']/subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
          <a href="{$cgi.script.URL}?follow+{$session.id}+{field[@id='461']/subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
          <xsl:call-template name="gen">
            <xsl:with-param name="enclosed_link" select="true()"/>
            <xsl:with-param name="r" select="field[@id='461']"/>
            <xsl:with-param name="s" select="field[@id='462']"/>
            <xsl:with-param name="pub" select="$pub"/>
            <xsl:with-param name="na" select="false()"/>
          </xsl:call-template>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="gen">
            <xsl:with-param name="r" select="field[@id='461']"/>
            <xsl:with-param name="s" select="field[@id='462']"/>
            <xsl:with-param name="pub" select="$pub"/>
            <xsl:with-param name="na" select="false()"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:for-each select="field[@id='463']">
        <xsl:choose>
          <xsl:when test="position() != 1">
            <xsl:text> ; </xsl:text>
          </xsl:when>
          <xsl:when test="../field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='a'] and subfield[@id='1']/field[@id='210']/subfield[@id='d']">
            <xsl:text>, </xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$dlm"/>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
          <xsl:when test="subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
            <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
            <xsl:call-template name="issue"/>
            </a>
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="issue"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
      <xsl:choose>
        <xsl:when test="field[@id='463']/subfield[@id='1']/field[@id='001'] and $fmt != 'B' and $ht">
          <a href="{$cgi.script.URL}?follow+{$session.id}+{field[@id='463']/subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
          <xsl:call-template name="htitle">
            <xsl:with-param name="r" select="field[@id='463']"/>
            <xsl:with-param name="na" select="false()"/>
          </xsl:call-template>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="htitle">
            <xsl:with-param name="r" select="field[@id='463']"/>
            <xsl:with-param name="na" select="false()"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:apply-templates select="field[@id='215']"/>
  <xsl:apply-templates select="field[@id='225']"/>
  <xsl:apply-templates select="field[@id='461']/subfield[@id='1']/field[@id='011']"/>
  <xsl:apply-templates select="field[@id='463']/subfield[@id='1']/field[@id='011']"/>
  <xsl:call-template name="notes"/>
  <xsl:call-template name="links"/>
  <xsl:apply-templates select="field[@id='856']"/>
  <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template name="collection">
  <span class="warn"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='W_UNIMPL']"/></span>
</xsl:template>

<xsl:template name="subjects">
  <xsl:variable name="fs" select="$follow.subject and not(//record[@syntax='1.2.840.10003.5.106']) and //database != $circ.db"/>
  <xsl:variable name="p600" select="count(field[@id='600'])"/>
  <xsl:variable name="p601" select="count(field[@id='601'])"/>
  <xsl:variable name="p602" select="count(field[@id='602'])"/>
  <xsl:variable name="p604" select="count(field[@id='604'])"/>
  <xsl:variable name="p605" select="count(field[@id='605'])"/>
  <xsl:variable name="p606" select="count(field[@id='606'])"/>
  <xsl:variable name="p607" select="count(field[@id='607'])"/>
  <xsl:variable name="p610" select="count(field[@id='610'])"/>
  <div class="subjects">
  <xsl:if test="$p600 + $p601 + $p602 + $p604 + $p605 + $p606 + $p607 + $p610 &gt; 0">
    <xsl:value-of select="$dash"/><xsl:text> </xsl:text><xsl:value-of select="$dash"/>
  </xsl:if>
  <xsl:for-each select="field[@id='600']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="position()"/>
    <xsl:text>. </xsl:text>
    <xsl:variable name="na">
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:choose>
      <xsl:when test="subfield[@id='g']">
        <xsl:text>, </xsl:text>
        <xsl:value-of select="subfield[@id='g']"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:if test="subfield[@id='b']">
          <xsl:text>, </xsl:text>
          <xsl:value-of select="subfield[@id='b']"/>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
    </xsl:variable>
    <xsl:choose>
      <xsl:when test="$fs">
        <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={$na}[1,21]&amp;LANG={$lang}">
          <xsl:value-of select="$na"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$na"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="subfield[@id='d']">
      <xsl:text> </xsl:text>
      <xsl:value-of select="subfield[@id='d']"/>
    </xsl:if>
    <xsl:if test="subfield[@id='c']">
      <xsl:text> (</xsl:text>
      <xsl:for-each select="subfield[@id='c']">
        <xsl:if test="position() != 1">
          <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:text>) </xsl:text>
    </xsl:if>
    <xsl:if test="subfield[@id='f']">
      <xsl:text>, </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={subfield[@id='f']}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="subfield[@id='f']"/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="subfield[@id='f']"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text>, </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='601']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + position()"/>
    <xsl:text>. </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={subfield[@id='a']}[1,21]&amp;LANG={$lang}">
            <xsl:value-of select="subfield[@id='a']"/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="subfield[@id='a']"/>
        </xsl:otherwise>
      </xsl:choose>
    <xsl:for-each select="subfield[@id='b']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,21]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:if test="subfield[@id='e'] or subfield[@id='f']">
      <xsl:text> (</xsl:text>
      <xsl:value-of select="subfield[@id='e']"/>
      <xsl:if test="subfield[@id='f']">
        <xsl:text> ; </xsl:text>
        <xsl:value-of select="subfield[@id='f']"/>
      </xsl:if>
      <xsl:text>)</xsl:text>
    </xsl:if>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text>, </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='602']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + $p601 + position()"/>
    <xsl:text>. </xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:if test="subfield[@id='f']">
      <xsl:text>, </xsl:text>
      <xsl:value-of select="subfield[@id='f']"/>
    </xsl:if>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text>, </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='604']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + $p601 + $p602 + position()"/>
    <xsl:text>. </xsl:text>
    <xsl:choose>
    <xsl:when test="subfield[@id='1']/field[starts-with(@id, '70')]">
      <xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='a']"/>
      <xsl:choose>
        <xsl:when test="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='g']">
          <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='g']"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:if test="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='b']">
            <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='b']"/>
          </xsl:if>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='c' or @id='f']">
        <xsl:text> (</xsl:text>
        <xsl:for-each select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='c' or @id='f']">
          <xsl:value-of select="."/>
          <xsl:if test="position() != last()"><xsl:text> ; </xsl:text></xsl:if>
        </xsl:for-each>
        <xsl:text>)</xsl:text>
      </xsl:if>
      <xsl:text>. </xsl:text>
    </xsl:when>
    <xsl:when test="subfield[@id='1']/field[starts-with(@id, '71')]">
      <xsl:value-of select="subfield[@id='1']/field[starts-with(@id, '71')]/subfield[@id='a']"/>
      <xsl:for-each select="subfield[@id='1']/field[starts-with(@id, '71')]/subfield[@id='b']">
        <xsl:text>. </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:text>. </xsl:text>
    </xsl:when>
    <xsl:when test="subfield[@id='1']/field[starts-with(@id, '72')]">
      <xsl:value-of select="subfield[@id='1']/field[starts-with(@id, '72')]/subfield[@id='a']"/>
      <xsl:if test="subfield[@id='1']/field[starts-with(@id,'72')]/subfield[@id='f']">
        <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'72')]/subfield[@id='f']"/><xsl:text>)</xsl:text>
      </xsl:if>
      <xsl:text>. </xsl:text>
    </xsl:when>
    </xsl:choose>
    <xsl:if test="subfield[@id='1']/field[starts-with(@id, '50')]">
      <xsl:for-each select="subfield[@id='1']/field[starts-with(@id, '50')]/subfield">
        <xsl:choose>
          <xsl:when test="@id='a'">
            <xsl:value-of select="."/>
          </xsl:when>
          <xsl:when test="@id='j' or @id='x' or @id='y' or @id='z'">
            <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
            <xsl:choose>
              <xsl:when test="$fs">
                <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
                  <xsl:value-of select="."/>
                </a>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="."/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:when test="@id='l' or @id='r' or @id='u'">
            <xsl:text>. </xsl:text>
            <xsl:choose>
              <xsl:when test="$fs">
                <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
                  <xsl:value-of select="."/>
                </a>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="."/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:when test="@id='w'">
            <xsl:text>. (</xsl:text>
            <xsl:choose>
              <xsl:when test="$fs">
                <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
                  <xsl:value-of select="."/>
                </a>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="."/>
              </xsl:otherwise>
            </xsl:choose>
            <xsl:text>)</xsl:text>
          </xsl:when>
        </xsl:choose>
      </xsl:for-each>
    </xsl:if>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='605']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + $p601 + $p602 + $p604 + position()"/>
    <xsl:text>. </xsl:text>
    <xsl:choose>
      <xsl:when test="$fs">
        <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={subfield[@id='a']}[1,21]&amp;LANG={$lang}">
          <xsl:value-of select="subfield[@id='a']"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="subfield[@id='a']"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:for-each select="subfield[@id='h']">
      <xsl:text>. </xsl:text><xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='i']">
      <xsl:text>. </xsl:text><xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="subfield[@id='l']">
      <xsl:text>(</xsl:text><xsl:value-of select="subfield[@id='l']"/><xsl:text>)</xsl:text>
    </xsl:if>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='j']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='606']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + $p601 + $p602 + $p604 + $p605 + position()"/>
    <xsl:text>. </xsl:text>
    <xsl:choose>
      <xsl:when test="$fs">
        <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={subfield[@id='a']}[1,21]&amp;LANG={$lang}">
          <xsl:value-of select="subfield[@id='a']"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="subfield[@id='a']"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text>, </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='j']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='607']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + $p601 + $p602 + $p604 + $p605 + $p606 + position()"/>
    <xsl:text>. </xsl:text>
    <xsl:choose>
      <xsl:when test="$fs">
        <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={subfield[@id='a']}[1,21]&amp;LANG={$lang}">
          <xsl:value-of select="subfield[@id='a']"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="subfield[@id='a']"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:for-each select="subfield[@id='j']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,47]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  <xsl:for-each select="field[@id='610']">
    <xsl:text> </xsl:text>
    <xsl:value-of select="$p600 + $p601 + $p602 + $p604 + $p605 + $p606 + $p607 + position()"/>
    <xsl:text>. </xsl:text>
    <xsl:for-each select="subfield[@id='a']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:choose>
        <xsl:when test="$fs">
          <a href="{$cgi.script.URL}?ACTION=follow&amp;SESSION_ID={$session.id}&amp;TERM={.}[1,21]&amp;LANG={$lang}">
            <xsl:value-of select="."/>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="class">
  <xsl:for-each select="field[@id='675']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='676']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_DDC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='680']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LCC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:value-of select="subfield[@id='b']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='rubbk']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LBC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='rugasnti']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_GASNTI']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='grnti']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_GRNTI']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='rueskl']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_ESKL']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='oksvnk']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OKSVNK']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <br/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="int">
  <xsl:apply-templates select="field[@id='801']"/>
</xsl:template>

<xsl:template name="notes">
  <xsl:for-each select="field[@id='300']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='301']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='302']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='305']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='309']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='311']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='313']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='316'] | field[@id='317']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
    <xsl:text> </xsl:text>
    <xsl:call-template name="org.by.code">
      <xsl:with-param name="oname" select="subfield[@id='5']"/>
    </xsl:call-template>
    <xsl:if test="count(subfield[@id='9'])">
      <xsl:text> : </xsl:text><xsl:value-of select="subfield[@id='9']"/>
    </xsl:if>
  </xsl:for-each>
  <xsl:for-each select="field[@id='320']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='321']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='322']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='323']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='324']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='325']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='326']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='327']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="$abstract">
    <xsl:for-each select="field[@id='330']/subfield[@id='a']">
      <xsl:if test="position()=1">
        <xsl:text>.</xsl:text>
      </xsl:if>
      <p class="note">
      <xsl:value-of select="."/>
      <xsl:text>.</xsl:text>
      </p>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="field[@id='333']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='336']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='337']/subfield[@id='a']">
    <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="link">
  <xsl:param name="lbl"/>
  <xsl:value-of select="$lbl"/><xsl:text> </xsl:text>
  <xsl:choose>
    <xsl:when test="subfield[@id='1']/field[@id='001'] and $ht">
      <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='1']/field[@id='001']}{$follow.attrs}+{$lang}">
<!--
        <xsl:call-template name="htitle">
-->
        <xsl:call-template name="gen">
          <xsl:with-param name="r" select="."/>
          <xsl:with-param name="na" select="false()"/>
        </xsl:call-template>
      </a>
    </xsl:when>
    <xsl:otherwise>
<!--
      <xsl:call-template name="htitle">
-->
      <xsl:call-template name="gen">
        <xsl:with-param name="r" select="."/>
        <xsl:with-param name="na" select="false()"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="links">
  <xsl:variable name="links" select="field[@id='421' and indicator[@id='2'] = 1]
	| field[@id='422' and indicator[@id='2'] = 1]
	| field[@id='423' and indicator[@id='2'] = 1]
	| field[@id='430' and indicator[@id='2'] = 1]
	| field[@id='431' and indicator[@id='2'] = 1]
	| field[@id='432' and indicator[@id='2'] = 1]
	| field[@id='433' and indicator[@id='2'] = 1]
	| field[@id='434' and indicator[@id='2'] = 1]
	| field[@id='435' and indicator[@id='2'] = 1]
	| field[@id='436' and indicator[@id='2'] = 1]
	| field[@id='437' and indicator[@id='2'] = 1]
	| field[@id='440' and indicator[@id='2'] = 1]
	| field[@id='441' and indicator[@id='2'] = 1]
	| field[@id='442' and indicator[@id='2'] = 1]
	| field[@id='443' and indicator[@id='2'] = 1]
	| field[@id='444' and indicator[@id='2'] = 1]
	| field[@id='445' and indicator[@id='2'] = 1]
	| field[@id='446' and indicator[@id='2'] = 1]
	| field[@id='448' and indicator[@id='2'] = 1]
	| field[@id='451' and indicator[@id='2'] = 1]
	| field[@id='452' and indicator[@id='2'] = 1]
	| field[@id='453' and indicator[@id='2'] = 1]
	| field[@id='454' and indicator[@id='2'] = 1]
	| field[@id='455' and indicator[@id='2'] = 1]
	| field[@id='456' and indicator[@id='2'] = 1]
	| field[@id='470' and indicator[@id='2'] = 1]
	| field[@id='481' and indicator[@id='2'] = 1]
	| field[@id='482' and indicator[@id='2'] = 1]
	| field[@id='488' and indicator[@id='2'] = 1]"/>
  <xsl:if test="$links">
    <xsl:text>.</xsl:text><div class="links">
  <xsl:for-each select="$links">
    <xsl:sort select="@id"/>
      <xsl:choose>
      <xsl:when test="generate-id() = generate-id(key('link', concat(generate-id(..), @id)))">
        <xsl:text>.</xsl:text><p/>
        <xsl:call-template name="link">
          <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id=current()/@id]"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="link">
          <xsl:with-param name="lbl" select="','"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
    </div>
  </xsl:if>
</xsl:template>

<xsl:template match="field[@id='801']">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="subfield[@id='b']"/>
  </xsl:call-template>
  <xsl:text> </xsl:text>
  <xsl:variable name="date" select="subfield[@id='c']"/>
  <xsl:value-of select="substring($date, 7, 2)"/><xsl:text>.</xsl:text>
  <xsl:value-of select="substring($date, 5, 2)"/><xsl:text>.</xsl:text>
  <xsl:value-of select="substring($date, 1, 4)"/><br/>
</xsl:template>

<xsl:template match="field[@id='850']">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="subfield[@id='a']"/>
  </xsl:call-template>
  <br/>
</xsl:template>

<xsl:template match="field[@id='899']">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="subfield[@id='a']"/>
  </xsl:call-template>
  <xsl:for-each select="subfield[@id='b']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='c']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="subfield[@id='h']">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='h']"/>
  </xsl:if>
  <xsl:for-each select="subfield[@id='i']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="subfield[@id='j']">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='j']"/>
  </xsl:if>
  <xsl:if test="subfield[@id='p']">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='p']"/>
  </xsl:if>
  <xsl:if test="subfield[@id='t']">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='t']"/>
  </xsl:if>
  <xsl:for-each select="subfield[@id='z']">
    <xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <br/>
</xsl:template>

<xsl:template match="field[@id='856']">
  <xsl:choose>
    <xsl:when test="subfield[@id='x'] = $cover">
    </xsl:when>
    <xsl:otherwise>
      <xsl:if test="subfield[@id='u']">
        <xsl:value-of select="$dlm"/>
        <xsl:choose>
          <xsl:when test="subfield[@id='z']">
            <a href="{subfield[@id='u']}"><xsl:value-of select="subfield[@id='z']"/></a>
          </xsl:when>
          <xsl:when test="not(../leader/type='l') and not(../field[@id='106']/subfield[@id='a']='s')">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_URL']"/><a href="{subfield[@id='u']}"><xsl:value-of select="subfield[@id='u']"/></a>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>&lt;URL:</xsl:text><a href="{subfield[@id='u']}"><xsl:value-of select="subfield[@id='u']"/></a><xsl:text>&gt;</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='010']">
  <xsl:choose>
    <xsl:when test="subfield[@id='a']">
      <xsl:value-of select="$dlm"/><xsl:text>ISBN </xsl:text><xsl:value-of select="subfield[@id='a']"/>
      <xsl:if test="subfield[@id='b']">
        <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='b']"/><xsl:text>) </xsl:text>
      </xsl:if>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:text> : </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:for-each select="subfield[@id='9']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:choose>
          <xsl:when test="position() != 1">
            <xsl:text> : </xsl:text><xsl:value-of select="."/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
      <xsl:for-each select="subfield[@id='9']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='011']">
  <xsl:choose>
    <xsl:when test="subfield[@id='a']">
      <xsl:value-of select="$dlm"/><xsl:text>ISSN </xsl:text><xsl:value-of select="subfield[@id='a']"/>
      <xsl:if test="subfield[@id='b']">
        <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='b']"/><xsl:text>) </xsl:text>
      </xsl:if>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:text> : </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:for-each select="subfield[@id='9']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:choose>
          <xsl:when test="position() != 1">
            <xsl:text> : </xsl:text><xsl:value-of select="."/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$dlm"/><xsl:value-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
      <xsl:for-each select="subfield[@id='9']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='700']">
  <xsl:value-of select="subfield[@id='a']"/>
  <xsl:if test="subfield[@id='d']">
    <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='d']"/>
  </xsl:if>
  <xsl:choose>
    <xsl:when test="subfield[@id='g']">
      <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='g']"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:if test="subfield[@id='b']">
        <xsl:text>, </xsl:text><xsl:value-of select="subfield[@id='b']"/>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:if test="subfield[@id='c' or @id='f']">
    <xsl:text> (</xsl:text>
    <xsl:for-each select="subfield[@id='c' or @id='f']">
      <xsl:value-of select="."/>
      <xsl:if test="position() != last()"><xsl:text> ; </xsl:text></xsl:if>
    </xsl:for-each>
    <xsl:text>) </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="field[@id='710']">
  <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='b']">
      <xsl:text>. </xsl:text><xsl:value-of select="."/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='205']">
  <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
  <xsl:for-each select="subfield[@id='b']">
    <xsl:text>, </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='d']">
    <xsl:text> = </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="subfield[@id='f'] or subfield[@id='g']">
    <xsl:text> / </xsl:text>
    <xsl:for-each select="subfield[@id='f']">
      <xsl:choose>
        <xsl:when test="position() = 1">
          <xsl:value-of select="."/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text> ; </xsl:text><xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='g']">
      <xsl:text> ; </xsl:text><xsl:value-of select="."/>
    </xsl:for-each>
  </xsl:if>
</xsl:template>

<xsl:template match="field[@id='206']">
  <xsl:value-of select="$dlm"/>
  <xsl:choose>
    <xsl:when test="subfield[@id='a']">
      <xsl:value-of select="subfield[@id='a']"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:for-each select="subfield[@id='b']">
        <xsl:if test="position() != 1">
          <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:if test="subfield[@id='c']">
        <xsl:text> ; </xsl:text><xsl:value-of select="subfield[@id='c']"/>
      </xsl:if>
      <xsl:if test="subfield[@id='d']">
        <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='d']"/><xsl:text>) </xsl:text>
      </xsl:if>
      <xsl:if test="subfield[@id='e']">
        <xsl:text> (</xsl:text>
          <xsl:value-of select="subfield[@id='e']"/>
          <xsl:if test="subfield[@id='f']">
            <xsl:text> ; </xsl:text><xsl:value-of select="subfield[@id='f']"/>
          </xsl:if>
        <xsl:text>) </xsl:text>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='207']">
  <xsl:value-of select="$dlm"/>
  <xsl:for-each select="subfield[@id='a']">
    <xsl:if test="position() != 1">
       <xsl:text> ; </xsl:text>
    </xsl:if>
    <xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='210']">
  <xsl:value-of select="$dlm"/>
  <xsl:choose>
    <xsl:when test="subfield[@id='r'] and count(subfield)=1">
      <xsl:value-of select="subfield[@id='r']"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:for-each select="subfield[@id='a']">
        <xsl:if test="position() != 1">
          <xsl:text> ; </xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:for-each select="subfield[@id='c']">
        <xsl:text> : </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:text>, </xsl:text>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:if test="position() != 1">
          <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:if test="subfield[@id='e'] | subfield[@id='f'] | subfield[@id='g'] | subfield[@id='h']">
        <xsl:text> (</xsl:text>
        <xsl:for-each select="subfield[@id='e']">
          <xsl:if test="position() != 1">
            <xsl:text>, </xsl:text>
          </xsl:if>
          <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='f']">
          <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='g']">
          <xsl:text> : </xsl:text><xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='h']">
          <xsl:text>, </xsl:text><xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>) </xsl:text>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='215']">
  <xsl:value-of select="$dlm"/>
  <xsl:for-each select="subfield[@id='a']">
    <xsl:choose>
      <xsl:when test="position() = 1">
        <xsl:value-of select="."/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
  <xsl:if test="subfield[@id='c']">
    <xsl:text> : </xsl:text><xsl:value-of select="subfield[@id='c']"/>
  </xsl:if>
  <xsl:for-each select="subfield[@id='d']">
    <xsl:text> ; </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='e']">
    <xsl:text> + </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='225']">
  <xsl:choose>
    <xsl:when test="position() = 1">
      <xsl:value-of select="$dlm"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:text> </xsl:text>
    </xsl:otherwise>
 </xsl:choose>
  <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='a']"/>
  <xsl:for-each select="subfield[@id='d']">
    <xsl:text> = </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='h']">
    <xsl:text>. </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='i']">
    <xsl:choose>
      <xsl:when test="position() = 1">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>. </xsl:text><xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='e']">
    <xsl:text> : </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="subfield[@id='f']">
    <xsl:text> / </xsl:text>
    <xsl:for-each select="subfield[@id='f']">
      <xsl:choose>
        <xsl:when test="position() = 1">
          <xsl:value-of select="."/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text> ; </xsl:text><xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="subfield[@id='v']">
    <xsl:text> ; </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='x']">
    <xsl:text>, </xsl:text><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:text>) </xsl:text>
</xsl:template>

<xsl:template match="field[@id='229']">
  <xsl:value-of select="$dlm"/>
  <xsl:for-each select="subfield[@id='a']">
    <xsl:if test="position() != 1">
      <xsl:text> ; </xsl:text>
    </xsl:if>
    <xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='230']">
  <xsl:value-of select="$dlm"/><xsl:value-of select="subfield[@id='a']"/>
</xsl:template>

<xsl:template match="field[@id='999']/subfield[@id='z']">
  <xsl:choose>
    <xsl:when test='contains(., "размер штрафа за задержку")'>
      <p class="fine"><xsl:value-of select="."/></p>
    </xsl:when>
    <xsl:otherwise>
      <p class="terms"><xsl:value-of select="."/></p>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
