<?xml version="1.0" encoding="utf-8"?>
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
          <xsl:if test="field[@id='856']/subfield[@id='x'] = $cover">
            <img src="{field[@id='856' and subfield[@id='x'] = $cover]/subfield[@id='u']}" align="left" hspace="5"/>
          </xsl:if>
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
              <xsl:call-template name="monograph"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="$fmt='F'">
        <xsl:if test="$subject">
          <xsl:call-template name="subjects"/>
        </xsl:if>
        <xsl:if test="$record.source">
          <xsl:call-template name="int"/>
        </xsl:if>
        <xsl:if test="not($type='x' or $type='y' or $type='z') and $class">
          <xsl:call-template name="class"/>
        </xsl:if>
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
      <div class="publication">
      <xsl:for-each select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
        <xsl:if test="position &gt; 1">
          <span class="punct"> ; </span>
        </xsl:if>
        <span class="placeOfPublication"><xsl:value-of select="."/></span>
      </xsl:for-each>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <div class="publication">
      <xsl:if test="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
        <xsl:choose>
          <xsl:when test="$r/../leader/leader07='s'">
            <span class="punct"> (</span><span class="dateOfPublication"><xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/></span><span class="punct">)</span>
          </xsl:when>
          <xsl:otherwise>
            <span class="dateOfPublication"><xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/></span>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
      </div>
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
</xsl:template>

<xsl:template name="spec">
  <xsl:param name="pub" select="'all'"/>
  <xsl:param name="show_author" select="true()"/>
  <xsl:param name="vol_num" select="''"/>
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="field[@id='200']"/>
    <xsl:with-param name="vol_num" select="$vol_num"/>
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
      <div class="armr_header">
      <xsl:apply-templates select="$p/field[@id='700' or @id='710']"/>
<!--
      <xsl:variable name="h1">
        <xsl:apply-templates select="$p/field[@id='700']"/>
      </xsl:variable>
      <xsl:variable name="h2">
        <xsl:apply-templates select="$p/field[@id='710']"/>
      </xsl:variable>
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
-->
<!--
        <xsl:if test="substring($h1, string-length($h1), 1) != '.' and substring($h2, string-length($h2), 1) != '.' and string-length($h1)+string-length($h2) &gt; 0">
          <xsl:text>.</xsl:text>
        </xsl:if>
-->
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
    <xsl:for-each select="field[@id='463']">
      <div class="specification">
        <xsl:call-template name="gen">
          <xsl:with-param name="r" select="."/>
          <xsl:with-param name="pub" select="'year'"/>
        </xsl:call-template>
      </div>
    </xsl:for-each>
  </xsl:if>
</xsl:template>

<xsl:template name="issue">
  <xsl:param name="year" select="true()"/>
  <div class="issue">
  <xsl:if test="subfield[@id='1']/field[@id='210']/subfield[@id='d'] and $year">
    <div class="publication"><span class="dateOfPublication"><xsl:value-of select="subfield[@id='1']/field[@id='210']/subfield[@id='d']"/></span></div>
  </xsl:if>
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="subfield[@id='1']/field[@id='200']"/>
  </xsl:call-template>
  </div>
</xsl:template>

<xsl:template name="htitle">
  <xsl:param name="r" select="/.."/>
  <xsl:for-each select="$r/subfield[@id='1']/field[@id='200']">
    <xsl:call-template name="title">
      <xsl:with-param name="s1" select="."/>
      <xsl:with-param name="show.v" select="false()"/>
    </xsl:call-template>
  </xsl:for-each>
  <div class="publication">
  <xsl:for-each select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
    <xsl:if test="position() &gt; 1">
      <span class="punct"> ; </span>
    </xsl:if>
    <span class="placeOfPublication"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <span class="punct">, </span>
  <span class="dateOfPublication"><xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/></span>
  </div>
  <xsl:if test="$r/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
<!-- !!! -->
    <xsl:value-of select="$r/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
<!-- !!! -->
  </xsl:if>
  <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='225']"/>
</xsl:template>

<xsl:template name="title">
  <xsl:param name="s1" select="/.."/>
  <xsl:param name="s2" select="/.."/>
  <xsl:param name="vol_num" select="''"/>
  <xsl:param name="show.v" select="true()"/>
  <div class="title">
  <xsl:if test="string-length($vol_num) &gt; 0">
    <span class="volume"><xsl:value-of select="$vol_num"/></span><span class="punct">: </span>
  </xsl:if>
  <xsl:if test="$s1/../../../leader/leader07 = 'm' and $show.v">
    <xsl:for-each select="$s1/subfield[@id='v']">
      <xsl:if test="position() != 1">
        <span class="punct">, </span>
      </xsl:if>
      <xsl:value-of select="."/>
      <span class="punct">: </span>
    </xsl:for-each>F
  </xsl:if>
  <xsl:for-each select="$s1/subfield[@id='a']">
    <xsl:if test="position() != 1">
       <span class="punct">; </span>
    </xsl:if>
    <span class="titleProper"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="$s2/subfield[@id='1']/field[@id='200']">
    <span class="punct">. </span>
    <xsl:call-template name="title">
      <xsl:with-param name="s1" select="."/>
      <xsl:with-param name="show.v" select="$show.v"/>
    </xsl:call-template>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='b']">
    <span class="punct"> [</span><span class="generalMaterialDesignation"><xsl:value-of select="."/></span><span class="punct">]</span>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='d']">
    <span class="punct"> = </span><span class="parallelTitleProper"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='e']">
    <span class="punct"> : </span><span class="otherInfo"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='h']">
    <span class="punct">. </span><span class="numberOfPart"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="$s1/subfield[@id='i']">
    <span class="punct">. </span><span class="nameOfPart"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:if test="$s1/subfield[@id='f'] or $s1/subfield[@id='g']">
    <span class="punct"> / </span>
    <xsl:for-each select="$s1/subfield[@id='f']">
      <xsl:if test="position() &gt; 1">
        <span class="punct"> ; </span>
      </xsl:if>
      <span class="firstResponsibility"><xsl:value-of select="."/></span>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='g']">
      <span class="punct"> ; </span><span class="subsequentResponsibility"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </xsl:if>
  </div>
  <xsl:if test="$s1/../../../leader/leader07 = 'a' and $show.v">
    <xsl:for-each select="$s1/subfield[@id='v']">
      <div class="locationAnalytic"><xsl:value-of select="."/></div>
    </xsl:for-each>
  </xsl:if>
</xsl:template>

<xsl:template name="monograph">
  <xsl:choose>
    <xsl:when test="field[@id='461']/subfield[@id='1']">
      <xsl:call-template name="header">
        <xsl:with-param name="p" select="field[@id='461']/subfield[@id='1']"/>
      </xsl:call-template>
      <!-- Have link to upper-level record -->
      <div class="bibliographicDescription monograph">
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
      <div class="general">
      <xsl:call-template name="gen">
        <xsl:with-param name="r" select="field[@id='461']"/>
        <xsl:with-param name="s" select="field[@id='462']"/>
      </xsl:call-template>
      </div>
      <div class="specification">
      <xsl:call-template name="spec">
        <xsl:with-param name="pub" select="'all'"/>
        <xsl:with-param name="show_author" select="false()"/>
        <xsl:with-param name="vol_num" select="$volnum"/>
      </xsl:call-template>
      </div>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <!-- Have no link to upper-level record -->
      <xsl:call-template name="header"/>
      <div class="bibliographicDescription monograph">
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
      </div>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="serial">
  <div class="bibliographicDescription serial">
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
      <div class="general">
      <xsl:call-template name="gen">
        <xsl:with-param name="r" select="field[@id='461']"/>
        <xsl:with-param name="s" select="field[@id='462']"/>
      </xsl:call-template>
      </div>
      <div class="specification">
      <xsl:if test="string-length($volnum) &gt; 0 and $havetitle='1'">
        <xsl:value-of select="$volnum"/><span class="punct"> : </span>
      </xsl:if>
      <xsl:call-template name="spec">
        <xsl:with-param name="pub" select="'year'"/>
      </xsl:call-template>
      <xsl:call-template name="sub"/>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <div class="general">
        <xsl:call-template name="spec"/>
      </div>
      <xsl:call-template name="sub"/>
    </xsl:otherwise>
  </xsl:choose>
  </div>
</xsl:template>

<xsl:template name="analytics">
  <xsl:call-template name="header"/>
  <div class="bibliographicDescription analytic">
  <div class="pieceAnalytic">
  <xsl:call-template name="title">
    <xsl:with-param name="s1" select="field[@id='200']"/>
  </xsl:call-template>
  <xsl:apply-templates select="field[@id='205']"/>
  <xsl:apply-templates select="field[@id='229']"/>
  <xsl:apply-templates select="field[@id='230']"/>
  </div>
  <div class="identifyingDocument">
  <xsl:choose>
    <xsl:when test="field[@id='461']/subfield[@id='1']">
      <xsl:variable name="pub">
        <xsl:choose>
          <xsl:when test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">place</xsl:when>
          <xsl:otherwise>all</xsl:otherwise>
        </xsl:choose>
      </xsl:variable>

      <xsl:call-template name="gen">
        <xsl:with-param name="r" select="field[@id='461']"/>
        <xsl:with-param name="s" select="field[@id='462']"/>
        <xsl:with-param name="pub" select="$pub"/>
        <xsl:with-param name="na" select="false()"/>
      </xsl:call-template>
      <xsl:for-each select="field[@id='463']">
        <xsl:choose>
          <xsl:when test="position() != 1">
            <span class="punct"> ; </span>
          </xsl:when>
          <xsl:when test="../field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='a'] and subfield[@id='1']/field[@id='210']/subfield[@id='d']">
 <!--           <span class="punct">, </span>-->
          </xsl:when>
        </xsl:choose>
        <xsl:call-template name="issue"/>
       </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="htitle">
        <xsl:with-param name="r" select="field[@id='463']"/>
        <xsl:with-param name="na" select="false()"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
  </div>
  <xsl:apply-templates select="field[@id='215']"/>
  <xsl:apply-templates select="field[@id='225']"/>
  <xsl:apply-templates select="field[@id='461']/subfield[@id='1']/field[@id='011']"/>
  <xsl:apply-templates select="field[@id='463']/subfield[@id='1']/field[@id='011']"/>
  <xsl:call-template name="notes"/>
  <xsl:call-template name="links"/>
  <xsl:apply-templates select="field[@id='856']"/>
  </div>
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
  <xsl:for-each select="field[@id='600']">
    <div class="personalNameSubject">
    <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:choose>
      <xsl:when test="subfield[@id='g']">
        <span class="punct">, </span>
        <span class="expansionOfInitials"><xsl:value-of select="subfield[@id='g']"/></span>
      </xsl:when>
      <xsl:otherwise>
        <xsl:if test="subfield[@id='b']">
          <span class="punct">, </span>
          <span class="partOfName"><xsl:value-of select="subfield[@id='b']"/></span>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="subfield[@id='d']">
      <span class="punct"> </span>
      <span class="romanNumerals"><xsl:value-of select="subfield[@id='d']"/></span>
    </xsl:if>
    <xsl:if test="subfield[@id='c']">
      <span class="punct"> (</span>
      <xsl:for-each select="subfield[@id='c']">
        <xsl:if test="position() != 1">
          <span class="punct">, </span>
        </xsl:if>
        <span class="additionsToName"><xsl:value-of select="."/></span>
      </xsl:for-each>
      <span class="punct">) </span>
    </xsl:if>
    <xsl:if test="subfield[@id='f']">
      <span class="punct">, </span>
      <span class="dates"><xsl:value-of select="subfield[@id='f']"/></span>
    </xsl:if>
    <xsl:call-template name="xyz"/>
    </div>
  </xsl:for-each>
  <xsl:for-each select="field[@id='601']">
    <div class="corporateNameSubject">
    <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:for-each select="subfield[@id='b']">
      <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
      <span class="subdivision"><xsl:value-of select="."/></span>
    </xsl:for-each>
    <xsl:if test="subfield[@id='e'] or subfield[@id='f']">
      <span class="punct"> (</span>
      <span class="locationOfMeeting"><xsl:value-of select="subfield[@id='e']"/></span>
      <xsl:if test="subfield[@id='f']">
        <span class="punct"> ; </span>
        <span class="dateOfMeeting"><xsl:value-of select="subfield[@id='f']"/></span>
      </xsl:if>
      <span class="punct">)</span>
    </xsl:if>
    <xsl:call-template name="xyz"/>
    </div>
  </xsl:for-each>
  <xsl:for-each select="field[@id='602']">
    <div class="familyNameSubject">
    <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:if test="subfield[@id='f']">
      <span class="punct">, </span>
      <span class="dates"><xsl:value-of select="subfield[@id='f']"/></span>
    </xsl:if>
    <xsl:call-template name="xyz"/>
    </div>
  </xsl:for-each>
  <xsl:for-each select="field[@id='604']">
    <div class="nameTitleSubject">
    <xsl:choose>
    <xsl:when test="subfield[@id='1']/field[starts-with(@id, '70')]">
      <div class="personalName">
      <span class="entry"><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='a']"/></span>
      <xsl:choose>
        <xsl:when test="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='g']">
         <span class="punct">, </span><span class="expansionOfInitials"><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='g']"/></span>
        </xsl:when>
        <xsl:otherwise>
          <xsl:if test="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='b']">
            <span class="punct">, </span><span class="partOfName"><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='b']"/></span>
          </xsl:if>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='c' or @id='f']">
        <span class="punct"> (</span>
        <xsl:for-each select="subfield[@id='1']/field[starts-with(@id,'70')]/subfield[@id='c' or @id='f']">
          <span class="partOfName"><xsl:value-of select="."/></span>
          <xsl:if test="position() != last()"><span class="punct"> ; </span></xsl:if>
        </xsl:for-each>
        <span class="punct">)</span>
      </xsl:if>
      </div>
    </xsl:when>
    <xsl:when test="subfield[@id='1']/field[starts-with(@id, '71')]">
      <div class="corporateName">
      <span class="entry"><xsl:value-of select="subfield[@id='1']/field[starts-with(@id, '71')]/subfield[@id='a']"/></span>
      <xsl:for-each select="subfield[@id='1']/field[starts-with(@id, '71')]/subfield[@id='b']">
        <span class="punct">. </span><span class="subdivision"><xsl:value-of select="."/></span>
      </xsl:for-each>
      </div>
    </xsl:when>
    <xsl:when test="subfield[@id='1']/field[starts-with(@id, '72')]">
      <div class="familyName">
      <span class="entry"><xsl:value-of select="subfield[@id='1']/field[starts-with(@id, '72')]/subfield[@id='a']"/></span>
      <xsl:if test="subfield[@id='1']/field[starts-with(@id,'72')]/subfield[@id='f']">
        <span class="punct"> (</span><span class="dates"><xsl:value-of select="subfield[@id='1']/field[starts-with(@id,'72')]/subfield[@id='f']"/></span><span class="punct">)</span>
      </xsl:if>
      </div>
    </xsl:when>
    </xsl:choose>
    <xsl:if test="subfield[@id='1']/field[starts-with(@id, '50')]">
      <div class="uniformTitleOrHeading">
      <xsl:for-each select="subfield[@id='1']/field[starts-with(@id, '50')]/subfield">
        <xsl:choose>
          <xsl:when test="@id='a'">
            <span class="uniformTitleOrHeading"><xsl:value-of select="."/></span>
          </xsl:when>
          <xsl:when test="@id='j'">
            <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
            <span class="formSubdivisionOrYear"><xsl:value-of select="."/></span>
          </xsl:when>
          <xsl:when test="@id='l'">
            <span class="punct">. </span>
            <span class="formSubheadingOrRomanNumeration"><xsl:value-of select="."/></span>
          </xsl:when>
          <xsl:when test="@id='r'">
            <span class="punct">. </span>
            <span class="mediumOfPerformance"><xsl:value-of select="."/></span>
          </xsl:when>
          <xsl:when test="@id='u'">
            <span class="punct">. </span>
            <span class="key"><xsl:value-of select="."/></span>
          </xsl:when>
          <xsl:when test="@id='w'">
            <span class="punct">. (</span>
            <span class="arrangedStatement"><xsl:value-of select="."/></span>
            <span class="punct">)</span>
          </xsl:when>
        </xsl:choose>
      </xsl:for-each>
      <xsl:call-template name="xyz"/>
      </div>     
    </xsl:if>
    </div>     
   </xsl:for-each>
   <xsl:for-each select="field[@id='605']">
    <div class="titleSubject">
    <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:for-each select="subfield[@id='h']">
      <span class="punct">. </span><span class="numberOfSectionOrPart"><xsl:value-of select="."/></span>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='i']">
      <span class="punct">. </span><span class="nameOfSectionOrPart"><xsl:value-of select="."/></span>
    </xsl:for-each>
    <xsl:if test="subfield[@id='l']">
      <span class="punct">(</span><span class="formSubheading"><xsl:value-of select="subfield[@id='l']"/></span><span class="punct">)</span>
    </xsl:if>
    <xsl:call-template name="xyz"/>
    <xsl:for-each select="subfield[@id='j']">
      <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
      <span class="formSubdivision"><xsl:value-of select="."/></span>
    </xsl:for-each>
    </div>     
  </xsl:for-each>
  <xsl:for-each select="field[@id='606']">
    <div class="topicalSubject">
    <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:call-template name="xyz"/>
    <xsl:for-each select="subfield[@id='j']">
      <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
      <span class="formSubdivision"><xsl:value-of select="."/></span>
    </xsl:for-each>
    </div>     
  </xsl:for-each>
  <xsl:for-each select="field[@id='607']">
    <div class="geographicalSubject">
    <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:for-each select="subfield[@id='j']">
      <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
      <span class="formSubdivision"><xsl:value-of select="."/></span>
    </xsl:for-each>
    <xsl:call-template name="xyz"/>
    </div>     
  </xsl:for-each>
  <xsl:for-each select="field[@id='610']">
    <div class="uncontrolledSubject">
    <xsl:for-each select="subfield[@id='a']">
      <xsl:if test="position() != 1">
        <span class="punct">, </span>
      </xsl:if>
      <span class="subjectTerm"><xsl:value-of select="."/></span>
    </xsl:for-each>
    </div>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="xyz">
  <xsl:for-each select="subfield[@id='x']">
    <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
    <span class="topicalSubdivision"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='y']">
    <span class="punct"><xsl:text> </xsl:text><xsl:value-of select="$dash"/><xsl:text> </xsl:text></span>
    <span class="geographicalSubdivision"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='z']">
    <span class="punct">, </span>
    <span class="chronolgicalSubdivision"><xsl:value-of select="."/></span>
  </xsl:for-each>
</xsl:template>

<xsl:template name="class">
  <div class="classification">
  <xsl:for-each select="field[@id='675']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="uDCNumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='676']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_DDC']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="dDCNumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='680']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LCC']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="lCClassNumber"><xsl:value-of select="subfield[@id='a']"/></span>
    <span class="lCBookNumber"><xsl:value-of select="subfield[@id='b']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='rubbk']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LBC']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="lBCNumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='rugasnti']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_GASNTI']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="gASNTINumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='grnti']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_GRNTI']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="gRNTINumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='rueskl']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_ESKL']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="eSKLNumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686' and subfield[@id='2']='oksvnk']">
    <xsl:if test="position() = 1">
      <span class="punct"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OKSVNK']"/><xsl:text> </xsl:text></span>
    </xsl:if>
    <span class="oKSVNKNumber"><xsl:value-of select="subfield[@id='a']"/></span>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="int">
  <div class="originatingSource">
  <xsl:apply-templates select="field[@id='801']"/>
  </div>
</xsl:template>

<xsl:template name="notes">
  <div class="notes">
  <xsl:for-each select="field[@id='300' or @id='301' or @id='302' or @id='305' or @id='309' or @id='311' or @id='313']/subfield[@id='a']">
    <span class="note"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='316'] | field[@id='317']">
    <span class="note"><xsl:value-of select="subfield[@id='a']"/>
    <span class="punct"> </span>
    <xsl:call-template name="org.by.code">
     <xsl:with-param name="oname" select="subfield[@id='5']"/>
    </xsl:call-template>
    <xsl:if test="count(subfield[@id='9'])">
      <span class="punct"> : </span><xsl:value-of select="subfield[@id='9']"/>
    </xsl:if>
    </span>
  </xsl:for-each>
  <xsl:for-each select="field[@id='320' or @id='321' or @id='322' or @id='323' or @id='324' or @id='325' or @id='326' or @id='327']/subfield[@id='a']">
    <span class="note"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:if test="$abstract">
    <xsl:for-each select="field[@id='330']/subfield[@id='a']">
      <span class="note abstract"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="field[@id='333' or @id='336' or @id='337']/subfield[@id='a']">
    <span class="note"><xsl:value-of select="."/></span>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="link">
  <xsl:param name="lbl"/>
  <div class="link">
    <span class="punct"><xsl:value-of select="$lbl"/><xsl:text> </xsl:text></span>
    <xsl:call-template name="gen">
      <xsl:with-param name="r" select="."/>
      <xsl:with-param name="na" select="false()"/>
    </xsl:call-template>
  </div>
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
    <div class="links">
    <xsl:for-each select="$links">
      <xsl:sort select="@id"/>
        <xsl:choose>
        <xsl:when test="generate-id() = generate-id(key('link', concat(generate-id(..), @id)))">
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
  <xsl:element name="div">
  <xsl:choose>
    <xsl:when test="indicator[@id='2']=0">
      <xsl:attribute name="class">originalCataloguingAgency</xsl:attribute>
    </xsl:when>
    <xsl:when test="indicator[@id='2']=1">
      <xsl:attribute name="class">transcribingAgency</xsl:attribute>
    </xsl:when>
    <xsl:when test="indicator[@id='2']=2">
       <xsl:attribute name="class">modifyingAgency</xsl:attribute>
   </xsl:when>
    <xsl:when test="indicator[@id='2']=3">
      <xsl:attribute name="class">issuingAgency</xsl:attribute>
    </xsl:when>
  </xsl:choose>
  <span class="agency">
  <xsl:call-template name="org.by.code">
    <xsl:with-param name="oname" select="subfield[@id='b']"/>
  </xsl:call-template>
  </span>
  <xsl:variable name="date" select="subfield[@id='c']"/>
  <span class="dateOfTransaction">
  <xsl:value-of select="substring($date, 7, 2)"/><xsl:text>.</xsl:text>
  <xsl:value-of select="substring($date, 5, 2)"/><xsl:text>.</xsl:text>
  <xsl:value-of select="substring($date, 1, 4)"/>
  </span>
  </xsl:element>
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
  <div class="standardNumber">
  <xsl:choose>
    <xsl:when test="subfield[@id='x'] = $cover">
    </xsl:when>
    <xsl:otherwise>
      <xsl:if test="subfield[@id='u']">
        <xsl:choose>
          <xsl:when test="subfield[@id='z']">
            <a href="{subfield[@id='u']}"><span class="comment"><xsl:value-of select="subfield[@id='z']"/></span></a>
          </xsl:when>
          <xsl:when test="not(../leader/type='l') and not(../field[@id='106']/subfield[@id='a']='s')">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_URL']"/><a href="{subfield[@id='u']}"><xsl:value-of select="subfield[@id='u']"/></a>
          </xsl:when>
          <xsl:otherwise>
            <span class="punct">&lt;URL:</span><a href="{subfield[@id='u']}"><span class="uRL"><xsl:value-of select="subfield[@id='u']"/></span></a><span class="punct">&gt;</span>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  </div>
</xsl:template>

<xsl:template match="field[@id='010']">
  <div class="standardNumber">
    <xsl:if test="subfield[@id='a']">
      <span class="punct">ISBN </span><span class="number"><xsl:value-of select="subfield[@id='a']"/></span>
    </xsl:if>
    <xsl:for-each select="subfield[@id='b']">
      <span class="punct"> (</span><span class="qualification"><xsl:value-of select="."/></span><span class="punct">) </span>
    </xsl:for-each>
    <xsl:if test="subfield[@id='d']">
      <span class="punct"> : </span><span class="price"><xsl:value-of select="."/></span>
    </xsl:if>
  </div>
</xsl:template>

<xsl:template match="field[@id='011']">
  <div class="standardNumber">
    <xsl:if test="subfield[@id='a']">
      <span class="punct">ISSN </span><span class="number"><xsl:value-of select="subfield[@id='a']"/></span>
    </xsl:if>
    <xsl:for-each select="subfield[@id='d']">
      <span class="punct"> : </span><span class="price"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </div>
</xsl:template>

<xsl:template match="field[@id='700']">
  <div class="personalName">
  <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
  <xsl:if test="subfield[@id='d']">
    <span class="punct"> </span><span class="romanNumerals"><xsl:value-of select="subfield[@id='d']"/></span>
  </xsl:if>
  <xsl:choose>
    <xsl:when test="subfield[@id='g']">
       <span class="punct">, </span><span class="expansionOfInitials"><xsl:value-of select="subfield[@id='g']"/></span>
    </xsl:when>
    <xsl:otherwise>
      <xsl:if test="subfield[@id='b']">
         <span class="punct">, </span><span class="partOfName"><xsl:value-of select="subfield[@id='b']"/></span>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:if test="subfield[@id='c' or @id='f']">
     <span class="punct"> (</span>
    <xsl:for-each select="subfield[@id='c' or @id='f']">
      <span class="additionOrDate"><xsl:value-of select="."/></span>
      <xsl:if test="position() != last()"><span class="punct"> ; </span></xsl:if>
    </xsl:for-each>
     <span class="punct">) </span>
  </xsl:if>
  </div>
</xsl:template>

<xsl:template match="field[@id='710']">
  <div class="corporateName">
  <span class="entry"><xsl:value-of select="subfield[@id='a']"/></span>
    <xsl:for-each select="subfield[@id='b']">
      <span class="punct">. </span><span class="subdivision"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </div>
</xsl:template>

<xsl:template match="field[@id='205']">
  <div class="edition">
  <span class="editionStatement"><xsl:value-of select="subfield[@id='a']"/></span>
  <xsl:for-each select="subfield[@id='d']">
     <span class="punct"> = </span><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:if test="subfield[@id='f'] or subfield[@id='g']">
    <span class="punct"> / </span>
    <xsl:for-each select="subfield[@id='f']">
      <xsl:if test="position() &gt; 1">
        <span class="punct"> ; </span>
      </xsl:if>
      <span class="firstResponsibility"><xsl:value-of select="."/></span>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='g']">
       <span class="punct"> ; </span><span class="subsequentResponsibility"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="subfield[@id='b']">
    <span class="punct">, </span><span class="additionalInfo"><xsl:value-of select="."/></span>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template match="field[@id='206']">
  <div class="materialSpecific">
  <xsl:choose>
    <xsl:when test="subfield[@id='a']">
      <span class="mathematicalData"><xsl:value-of select="subfield[@id='a']"/></span>
    </xsl:when>
    <xsl:otherwise>
      <xsl:for-each select="subfield[@id='b']">
        <xsl:if test="position() != 1">
          <span class="punct">, </span>
        </xsl:if>
        <span class="scale"><xsl:value-of select="."/></span>
      </xsl:for-each>
      <xsl:if test="subfield[@id='c']">
        <span class="punct"> ; </span><span class="projection"><xsl:value-of select="subfield[@id='c']"/></span>
      </xsl:if>
      <xsl:if test="subfield[@id='d']">
        <span class="punct"> (</span><span class="coordinates"><xsl:value-of select="subfield[@id='d']"/></span><span class="punct">) </span>
      </xsl:if>
      <xsl:if test="subfield[@id='e']">
        <span class="punct"> (</span>
          <span class="declination"><xsl:value-of select="subfield[@id='e']"/></span>
          <xsl:if test="subfield[@id='f']">
            <span class="punct"> ; </span><span class="equinox"><xsl:value-of select="subfield[@id='f']"/></span>
          </xsl:if>
        <span class="punct">) </span>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  </div>
</xsl:template>

<xsl:template match="field[@id='207']">
  <div class="materialSpecific">
  <xsl:for-each select="subfield[@id='a']">
    <xsl:if test="position() != 1">
       <span class="punct"> ; </span>
    </xsl:if>
    <span class="numbering"><xsl:value-of select="."/></span>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template match="field[@id='210']">
  <div class="publication">
  <xsl:choose>
    <xsl:when test="subfield[@id='r'] and count(subfield)=1">
      <span class="dataInSourceForm"><xsl:value-of select="subfield[@id='r']"/></span>
    </xsl:when>
    <xsl:otherwise>
      <xsl:for-each select="subfield[@id='a']">
        <xsl:if test="position() != 1">
          <span class="punct"> ; </span>
        </xsl:if>
        <span class="placeOfPublication"><xsl:value-of select="."/></span>
      </xsl:for-each>
      <xsl:for-each select="subfield[@id='c']">
        <span class="punct"> : </span><span class="nameOfPublisher"><xsl:value-of select="."/></span>
      </xsl:for-each>
      <span class="punct">, </span>
      <xsl:for-each select="subfield[@id='d']">
        <xsl:if test="position() != 1">
          <span class="punct">, </span>
        </xsl:if>
        <span class="dateOfPublication"><xsl:value-of select="."/></span>
      </xsl:for-each>
      <xsl:if test="subfield[@id='e'] | subfield[@id='f'] | subfield[@id='g'] | subfield[@id='h']">
        <span class="punct"> (</span>
        <xsl:for-each select="subfield[@id='e']">
          <xsl:if test="position() != 1">
            <span class="punct">, </span>
          </xsl:if>
          <span class="placeOfManufacture"><xsl:value-of select="."/></span>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='f']">
          <span class="addressOfManufacturer"><xsl:value-of select="."/></span>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='g']">
          <span class="punct"> : </span><span class="nameOfManufacturer"><xsl:value-of select="."/></span>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='h']">
          <span class="punct">, </span><span class="dateOfManufacture"><xsl:value-of select="."/></span>
        </xsl:for-each>
        <span class="punct">) </span>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
  </div>
</xsl:template>

<xsl:template match="field[@id='215']">
  <div class="physicalDescription">
  <xsl:for-each select="subfield[@id='a']">
    <xsl:choose>
      <xsl:when test="position() = 1">
        <xsl:value-of select="."/>
      </xsl:when>
      <xsl:otherwise>
        <span class="punct">, </span><span class="materialDesignationAndExtent"><xsl:value-of select="."/></span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
  <xsl:if test="subfield[@id='c']">
    <span class="punct"> : </span><span class="oherInfo"><xsl:value-of select="subfield[@id='c']"/></span>
  </xsl:if>
  <xsl:for-each select="subfield[@id='d']">
    <span class="punct"> ; </span><span class="dimensions"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='e']">
    <span class="punct"> + </span><span class="accompanyingMaterial"><xsl:value-of select="."/></span>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template match="field[@id='225']">
  <div class="series">
  <span class="punct"> (</span><span class="seriesTitle"><xsl:value-of select="subfield[@id='a']"/></span>
  <xsl:for-each select="subfield[@id='d']">
    <span class="punct"> = </span><span class="parallelSeriesTitle"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='h']">
    <span class="punct">. </span><span class="numberOfPart"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='i']">
    <xsl:choose>
      <xsl:when test="position() = 1">
        <span class="punct">, </span>
      </xsl:when>
      <xsl:otherwise>
        <span class="punct">. </span>
      </xsl:otherwise>
    </xsl:choose>
    <span class="nameOfPart"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='e']">
    <span class="punct"> : </span><span class="otherInfo"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:if test="subfield[@id='f']">
    <span class="punct"> / </span>
    <xsl:for-each select="subfield[@id='f']">
      <xsl:if test="position() != 1">
        <span class="punct"> ; </span>
      </xsl:if>
      <span class="responsibility"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </xsl:if>
  <xsl:for-each select="subfield[@id='v']">
    <span class="punct"> ; </span><span class="volume"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='x']">
    <span class="punct">, </span><span class="iSSN"><xsl:value-of select="."/></span>
  </xsl:for-each>
  <span class="punct">) </span>
  </div>
</xsl:template>

<xsl:template match="field[@id='229']">
  <div class="materialSpecific">
  <xsl:for-each select="subfield[@id='a']">
    <xsl:if test="position() != 1">
      <span class="punct"> ; </span>
    </xsl:if>
    <span class="designationAndExtent"><xsl:value-of select="."/></span>
  </xsl:for-each>
  </div>
</xsl:template>

<xsl:template match="field[@id='230']">
  <div class="materialSpecific">
    <span class="designationAndExtent"><xsl:value-of select="subfield[@id='a']"/></span>
  </div>
</xsl:template>

</xsl:stylesheet>
