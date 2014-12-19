<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: authority.xsl,v $
 * Revision 1.12  2008/05/27 11:34:43  rustam
 * Linking attributes are parameterized
 *
 * Revision 1.11  2005/12/20 11:31:43  rustam
 * Minor improvement
 *
 * Revision 1.10  2004/05/31 10:40:05  rustam
 * URL recognition
 *
 * Revision 1.9  2004/05/21 09:21:18  rustam
 * Improved record representation
 *
 * Revision 1.8  2004/02/25 13:39:05  rustam
 * Minor corrections
 *
 * Revision 1.7  2004/02/25 13:24:40  rustam
 * Minor improvements
 *
 * Revision 1.6  2003/05/15 07:18:45  rustam
 * Minor changes
 *
 * Revision 1.5  2003/04/08 13:16:31  rustam
 * Minor changes
 *
 * Revision 1.4  2002/02/20 14:39:23  web
 * Minor changes
 *
 * Revision 1.3  2002/02/18 08:42:27  web
 * Minor changes
 *
 * Revision 1.2  2001/09/27 09:18:07  web
 * Minor changes
 *
 * Revision 1.1  2001/09/19 14:00:30  web
 * Authority records support
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
<xsl:param name="da" select="' '"/>
<xsl:template name="auth_ref">
  <xsl:param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE']"/>
   
  <xsl:choose>
    <xsl:when test="subfield[@id='5']">
      <xsl:variable name="c" select="subfield[@id='5']"/>
      <xsl:if test="substring($c, 2, 1) != '0'">
        <xsl:choose>
          <xsl:when test="substring($c, 1, 1) = 'a'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_EARLIER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'b'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_LATER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'c'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ASSOC']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'd'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ACRONYM']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'e'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_PSEUDONYM']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'f'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_REAL']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'g'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_BROADER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'h'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_NARROWER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 's'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_OTHER']"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$lbl"/>
          </xsl:otherwise>
       </xsl:choose>
      </xsl:if>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$lbl"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="auth_ref_also">
  <xsl:param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO']"/>
   
  <xsl:choose>
    <xsl:when test="subfield[@id='5']">
      <xsl:variable name="c" select="subfield[@id='5']"/>
      <xsl:if test="substring($c, 2, 1) != '0'">
        <xsl:choose>
          <xsl:when test="substring($c, 1, 1) = 'a'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_EARLIER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'b'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_LATER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'c'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_ASSOC']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'd'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_ACRONYM']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'e'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_PSEUDONYM']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'f'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_REAL']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'g'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_BROADER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 'h'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_NARROWER']"/>
          </xsl:when>
          <xsl:when test="substring($c, 1, 1) = 's'">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO_SYN']"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$lbl"/>
          </xsl:otherwise>
       </xsl:choose>
      </xsl:if>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$lbl"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="auth_name">
  <xsl:choose>
    <xsl:when test="indicator[@id='2'] = '0'">
      <xsl:value-of select="subfield[@id='a']"/>
      <xsl:if test="subfield[@id='d']">
        <xsl:text> </xsl:text><xsl:value-of select="subfield[@id='d']"/>
      </xsl:if>
      <xsl:for-each select="subfield[@id='c']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:if test="subfield[@id='f']">
        <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='f']"/><xsl:text>)</xsl:text>
      </xsl:if>
    </xsl:when>
    <xsl:when test="indicator[@id='2'] = '1'">
      <xsl:value-of select="subfield[@id='a']"/>
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
      <xsl:for-each select="subfield[@id='c']">
        <xsl:text>, </xsl:text><xsl:value-of select="."/>
      </xsl:for-each>
      <xsl:if test="subfield[@id='f']">
        <xsl:text> (</xsl:text><xsl:value-of select="subfield[@id='f']"/><xsl:text>)</xsl:text>
      </xsl:if>
    </xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template name="auth_subj">
  <xsl:value-of select="subfield[@id='a']"/>
  <xsl:for-each select="subfield[@id='x']">
    <xsl:value-of select="$da"/><xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='y']">
    <xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='z']">
    <xsl:value-of select="."/>
  </xsl:for-each>
  <xsl:for-each select="subfield[@id='9']">
    <xsl:value-of select="."/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="sources">
  <xsl:if test="field[@id='810']/subfield[@id='a']">
    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_SOURCES']"/>
    <ol>
    <xsl:for-each select="field[@id='810']/subfield[@id='a']">
      <li>
        <xsl:choose>
          <xsl:when test="contains(., '&lt;URL:')">
            <xsl:variable name="u" select="substring-before(substring-after(., '&lt;URL:'), '&gt;')"/>
            <xsl:value-of select="substring-before(., '&lt;URL:')"/>
            <xsl:text>&lt;URL:</xsl:text><a href="{$u}"><xsl:value-of select="$u"/></a><xsl:text>&gt;</xsl:text>
            <xsl:value-of select="substring-after(substring-after(., '&lt;URL:'), '&gt;')"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </li>
    </xsl:for-each>
    </ol>
  </xsl:if>
</xsl:template>

<xsl:template name="authority">
  <h3>
  <xsl:for-each select="field[@id='200']">
    <xsl:call-template name="auth_name"/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='210']">
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='b']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='c']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='d']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:value-of select="subfield[@id='e']"/>
    <xsl:value-of select="subfield[@id='f']"/>
    <xsl:value-of select="subfield[@id='g']"/>
    <xsl:for-each select="subfield[@id='h']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='9']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='215']">
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='9']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='220']">
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:value-of select="subfield[@id='f']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='9']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='230']">
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='b']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='h']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='i']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:value-of select="subfield[@id='k']"/>
    <xsl:value-of select="subfield[@id='l']"/>
    <xsl:value-of select="subfield[@id='m']"/>
    <xsl:for-each select="subfield[@id='n']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:value-of select="subfield[@id='q']"/>
    <xsl:for-each select="subfield[@id='r']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='s']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:value-of select="subfield[@id='u']"/>
    <xsl:value-of select="subfield[@id='w']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='9']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='235']">
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='b']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:value-of select="subfield[@id='e']"/>
    <xsl:value-of select="subfield[@id='k']"/>
    <xsl:value-of select="subfield[@id='m']"/>
    <xsl:for-each select="subfield[@id='r']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='s']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:value-of select="subfield[@id='u']"/>
    <xsl:value-of select="subfield[@id='w']"/>
    <xsl:for-each select="subfield[@id='x']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='y']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='z']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='9']">
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='250']">
    <xsl:call-template name="auth_subj"/>
  </xsl:for-each>
  </h3>
  <xsl:for-each select="field[@id='400']">
    <p class="ind">
    <xsl:call-template name="auth_ref">
      <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE']"/>
    </xsl:call-template>
    <br/>
    <xsl:choose>
      <xsl:when test="subfield[@id='3']">
        <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='3']}{$follow.attrs}+{$lang}">
        <xsl:call-template name="auth_name"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="auth_name"/>
      </xsl:otherwise>
    </xsl:choose>
    </p>
  </xsl:for-each>
  <xsl:for-each select="field[@id='450']">
    <p class="ind">
    <xsl:call-template name="auth_ref">
      <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE']"/>
    </xsl:call-template>
    <br/>
    <xsl:choose>
      <xsl:when test="subfield[@id='3']">
        <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='3']}{$follow.attrs}+{$lang}">
        <xsl:call-template name="auth_subj"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="auth_subj"/>
      </xsl:otherwise>
    </xsl:choose>
    </p>
  </xsl:for-each>
  <xsl:for-each select="field[@id='500']">
    <p class="ind">
    <xsl:call-template name="auth_ref_also">
      <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO']"/>
    </xsl:call-template>
    <br/>
    <xsl:choose>
      <xsl:when test="subfield[@id='3']">
        <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='3']}{$follow.attrs}+{$lang}">
        <xsl:call-template name="auth_name"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="auth_name"/>
      </xsl:otherwise>
    </xsl:choose>
    </p>
  </xsl:for-each>
  <xsl:for-each select="field[@id='550']">
    <p class="ind">
    <xsl:call-template name="auth_ref_also">
      <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEE_ALSO']"/>
    </xsl:call-template>
    <br/>
    <xsl:choose>
      <xsl:when test="subfield[@id='3']">
        <a href="{$cgi.script.URL}?follow+{$session.id}+{subfield[@id='3']}{$follow.attrs}+{$lang}">
        <xsl:call-template name="auth_subj"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="auth_subj"/>
      </xsl:otherwise>
    </xsl:choose>
    </p>
  </xsl:for-each>
  <xsl:for-each select="field[@id='675']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="subfield[@id='b']"/>
    <xsl:text> </xsl:text>
    <xsl:for-each select="subfield[@id='c']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='300']">
    <p class="note.auth"><xsl:value-of select="subfield[@id='a']"/></p>
  </xsl:for-each>
  <xsl:call-template name="sources"/>
  <xsl:for-each select="field[@id='676']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_DDC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="subfield[@id='b']"/>
    <xsl:text> </xsl:text>
    <xsl:for-each select="subfield[@id='c']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='680']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LCC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="subfield[@id='b']"/>
    <xsl:text> </xsl:text>
    <xsl:for-each select="subfield[@id='c']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='686']">
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
    <xsl:text> </xsl:text>
    <xsl:value-of select="subfield[@id='b']"/>
    <xsl:text> </xsl:text>
    <xsl:for-each select="subfield[@id='c']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
  <xsl:for-each select="field[@id='689']">
    <xsl:if test="position() = 1">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LBC']"/><xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="subfield[@id='b']"/>
    <xsl:text> </xsl:text>
    <xsl:for-each select="subfield[@id='c']">
      <xsl:if test="position() != 1">
        <xsl:text>, </xsl:text>
      </xsl:if>
      <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
