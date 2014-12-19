<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: form.xsl,v $
 * Revision 1.20  2005/04/27 05:46:45  rustam
 * Added PDA support
 *
 * Revision 1.19  2004/11/04 14:56:31  rustam
 * Implemented query filter
 *
 * Revision 1.18  2004/09/23 07:21:08  rustam
 * Added virtual keyboard
 *
 * Revision 1.17  2004/06/22 10:54:35  rustam
 * Implemented logos in form
 *
 * Revision 1.16  2004/06/04 09:10:17  rustam
 * Minor bug corrected
 *
 * Revision 1.15  2004/06/04 08:00:28  rustam
 * Added support for scanninng directories
 *
 * Revision 1.14  2004/05/31 11:25:47  rustam
 * Minor corrections
 *
 * Revision 1.13  2004/04/29 09:59:31  rustam
 * Circulation database supported
 *
 * Revision 1.12  2004/04/06 06:19:32  rustam
 * Minor changes
 *
 * Revision 1.11  2003/11/05 08:44:42  rustam
 * Minor changes
 *
 * Revision 1.10  2003/09/30 11:28:09  rustam
 * Implemented new scan method
 *
 * Revision 1.9  2003/09/02 09:08:44  rustam
 * Implemented record syntax selection simplification
 *
 * Revision 1.8  2003/06/25 10:22:47  rustam
 * Zthes supported
 *
 * Revision 1.7  2003/06/09 09:24:38  rustam
 * Implemented menu bar in form
 *
 * Revision 1.6  2003/05/15 09:32:14  rustam
 * Minor changes
 *
 * Revision 1.5  2003/05/15 07:27:32  rustam
 * Implemented profiles
 *
 * Revision 1.4  2003/04/11 09:47:55  rustam
 * Minor corrections
 *
 * Revision 1.3  2003/04/08 11:36:32  rustam
 * Minor changes
 *
 * Revision 1.2  2003/03/27 10:58:24  rustam
 * Added support for external selector dialog
 *
 * Revision 1.1  2003/01/31 14:11:35  rustam
 * New pre-release
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:exsl="http://exslt.org/common"> 
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN"
	doctype-system="http://www.w3.org/TR/1999/REC-html401-19991224"
/>

<xsl:key name="akey2" match="explain/indexInfo/index/map/attr[@type='2']" use="."/>
<xsl:key name="akey4" match="explain/indexInfo/index/map/attr[@type='4']" use="."/>
<xsl:key name="rskey" match="explain/recordInfo/recordSyntax[@oid!='1.2.840.10003.5.106']" use="@oid"/>

<xsl:template match="target" mode="FORM_MODE">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset={$charset}"/>
      <link href="{$stylesheet.URL}" rel="stylesheet" type="text/css"/>
      <link href="{$stylesheet.FORM}" rel="stylesheet"  type="text/css"/>
      <link href="{$stylesheet.COLOURS}" rel="stylesheet"  type="text/css"/>
      <link href="{$stylesheet.FORMEXT}" rel="stylesheet"  type="text/css"/>      
      <title><xsl:value-of select="explain[1]/configInfo/setting[@type='title'][@lang=$lang]"/></title>
      <xsl:if test="$scan.to.form or $resource.reports or $simplify.recsyn.list or $include.virtual.kbd or
	$include.dialog and count(explain/configInfo/setting[@type='include.dialog']) = 0 or
	explain/configInfo/setting[@type='include.dialog' and .='true'] or
	explain[indexInfo/index/map/attr/@attributeSet = '1.2.840.10003.3.1000.148.1']">
        <script type="text/javascript" src="{$java.script.URL}" charset="{$charset}"></script>
      </xsl:if>
      <script type="text/javascript" src="{$javascript.COOKIE}"></script>
      <script type="text/javascript" src="{$javascript.JSUTILS}"></script>
      <script type="text/javascript" src="{$javascript.JSFORMEXT}"></script>
      <xsl:call-template name="form.js.extention"/>
    </head>
    <xsl:element name="body">
      <xsl:choose>
        <xsl:when test="explain/serverInfo[database = 'circ'] and count(explain/serverInfo/database) = 1">
          <xsl:attribute name="onload">document.forms["ZGATE"].submit();loadProfiles();</xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
          <xsl:attribute name="onload">loadProfiles();</xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>
    
      <xsl:call-template name="form.header"/>

      <xsl:call-template name="form.body">
        <xsl:with-param name="db" select="string(explain/serverInfo/database)"/>
      </xsl:call-template>
      
      <xsl:if test="$include.ext.form and explain/serverInfo[database='IR-Extend-1']
	and count(explain) &gt; 1">
        <xsl:call-template name="form.body">
          <xsl:with-param name="db" select="'IR-Extend-1'"/>
        </xsl:call-template>
      </xsl:if>

      <xsl:call-template name="form.footer"/>
    </xsl:element>
  </html>
</xsl:template>

<xsl:template name="form.js.extention">
<script language="javascript">
<xsl:text>
function listItem (title, value) {
  this.title = title;
  if (value) {
    this.value = value;
  }
}
var consItems = new Array(12);
var members = null;
var sProfile = null;
</xsl:text>
var MSG_INPUT_PROFILE_NAME = "<xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_INPUT_SEARCH_PROFILE_REQUEST']"/>";
var MSG_PROFILE_NAME_EXISTS = "<xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_PROFILE_NAME_EXISTS']"/>";
var MSG_NOT_SAVED_PROFILE = "<xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_NOT_SAVED_PROFILE']"/>";
<xsl:for-each select="explain[serverInfo/database != 'IR-Extend-1' and not(indexInfo/index/map/attr[@attributeSet = '1.2.840.10003.3.1000.148.1'])]">
consItems[<xsl:value-of select="position()-1"/>] = new Array(2);
consItems[<xsl:value-of select="position()-1"/>][0] = new listItem ("<xsl:value-of select="normalize-space(databaseInfo/title[@lang=$lang])"/>"); 
members = new Array(<xsl:value-of select="count(membersInfo/server)"/>);
consItems[<xsl:value-of select="position()-1"/>][1] = members;
<xsl:for-each select="membersInfo/server">
members[<xsl:value-of select="position()-1"/>] = new listItem("<xsl:value-of select="label"/>","<xsl:value-of select="zurl"/>");
</xsl:for-each>
</xsl:for-each>
<![CDATA[
]]>
</script>
</xsl:template>

<xsl:template name="form.body">
  <xsl:param name="db"/>
  <form name="ZGATE" method="POST" action="{$cgi.script.URL}">
    <input type="hidden" name="HOST" value="{explain/serverInfo/host}"/>
    <input type="hidden" name="PORT" value="{explain/serverInfo/port}"/>
    <input type="hidden" name="SESSION_ID" value="{$session.id}"/>
    <input type="hidden" name="LANG" value="{$lang}"/>
    <input type="hidden" name="ACTION" value="SEARCH"/>
    <input type="hidden" name="ESNAME" value="{$element.set.name}"/>
    <xsl:if test="explain/configInfo/setting[@type='charset']">
      <input type="hidden" name="CHAR_SET" value="{explain/configInfo/setting[@type='charset']}"/>
    </xsl:if>
  <xsl:choose>
    <xsl:when test="$db='IR-Extend-1'">
      <input type="hidden" name="ATTSET" value="1.2.840.10003.3.3"/>
      <input type="hidden" name="DBNAME" value="{$db}"/>
      <input type="hidden" name="FILTER" value="AND(4[1,5],%)"/>
      <input type="hidden" name="use_1" value="1"/>
      <input type="hidden" name="term_1" value="{$user.id}"/>
      <input type="hidden" name="use_2" value="4"/>
      <input type="hidden" name="boolean_op_1" value="AND"/>
      <input type="hidden" name="boolean_op_2" value="AND"/>
      <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_IO_STATUS']"/>
      <select name="TERM_2" class="edit-field">
        <option selected="" value=""><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_T_STATUS_ANY']"/></option>
        <option value="0"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_T_STATUS_PENDING']"/></option>
        <option value="1"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_T_STATUS_ACTIVE']"/></option>
        <option value="2"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_T_STATUS_COMPLETE']"/></option>
        <option value="3"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_T_STATUS_ABORTED']"/></option>
      </select>
      <br/><br/>
      <select name="USE_3" class="edit-field">
<!--
        <option selected="" value="1"><xsl:value-of select="$ad/attributes/set[@id='1.2.840.10003.3.3']/localization[@lang=$lang]/attr[@type='1' and @value='1']"/></option>
-->
        <option value="3"><xsl:value-of select="$ad/attributes/set[@id='1.2.840.10003.3.3']/localization[@lang=$lang]/attr[@type='1' and @value='3']"/></option>
        <option value="7"><xsl:value-of select="$ad/attributes/set[@id='1.2.840.10003.3.3']/localization[@lang=$lang]/attr[@type='1' and @value='7']"/></option>
      </select>
      <input name="term_3" size="{$term.size}" maxlength="{$term.size.max}" class="edit-field"/>
      <br/><br/>
      <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_MAXREC']"/>
      <input name="MAXRECORDS" value="{$num.records}" size="{$num.records.size}" class="edit-field"/>
      <br/>
      <input type="submit" value="{$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SUBMIT']}" class="grey-button"/>
      <input type="reset" value="{$msg.form/messages/localization[@lang=$lang]/msg[@id='I_RESET']}" class="grey-button"/>
    </xsl:when>
    <xsl:when test="$db='circ'">
      <input type="hidden" name="ATTSET" value="1.2.840.10003.3.1"/>
      <input type="hidden" name="DBNAME" value="{$db}"/>
      <input type="hidden" name="use_1" value="100"/>
      <input type="hidden" name="term_1" value="{$user.id}"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:if test="string-length($query.filter) &gt; 0">
        <input type="hidden" name="FILTER" value="{$query.filter}"/>
      </xsl:if>
      <xsl:variable name="have.bib.level" select="count(explain/indexInfo/index/map[attr[@type='1']='1021']) &gt; 0"/>
      <xsl:variable name="have.content.type" select="count(explain/indexInfo/index/map[attr[@type='1']='1034']) &gt; 0"/>
      <xsl:variable name="have.languages" select="count(explain/indexInfo/index/map[attr[@type='1']='54']) &gt; 0"/>

<!-- Begin of materials, languages, databases section-->
      <xsl:choose>
        <xsl:when test="count(explain/serverInfo/database) &gt; 1 or
	$include.languages.list and $have.languages or
	$include.materials.list and ($have.bib.level or $have.content.type)">
          <table>
          <tr>
          <xsl:if test="$include.materials.list and ($have.bib.level or $have.content.type)">
            <th><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_MATERIALS']"/></th>
          </xsl:if>
          <xsl:if test="$include.languages.list and ($have.languages)">
            <th><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_LANGUAGES']"/></th>
          </xsl:if>
          <xsl:if test="count(explain/serverInfo/database)-count(explain/serverInfo[database='IR-Extend-1'])-count(explain[indexInfo/index/map/attr/@attributeSet='1.2.840.10003.3.1000.148.1']) &gt; 1">
            <th><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_DATABASES']"/></th>
          </xsl:if>
          </tr><tr>
          <xsl:if test="$include.materials.list and ($have.bib.level or $have.content.type)">
            <td>
              <select name="MATERIAL_TYPE" multiple="" size="{$list.size + 1}" class="edit-field">
                <option selected="" value=""><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_ALL']"/></option>
                <xsl:for-each select="$md/messages/localization[@lang=$lang]/msg">
                  <option value="{@id}"><xsl:value-of select="."/></option>
                </xsl:for-each>
              </select>
            </td>
          </xsl:if>
          <xsl:if test="$include.languages.list and ($have.languages)">
            <td>
              <select name="CODE_LANG" multiple="" size="{$list.size + 1}" class="edit-field">
                <option selected="" value=""><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_ANY_SM']"/></option>
                <xsl:for-each select="$ld/messages/localization[@lang=$lang]/msg">
                  <option value="{@id}"><xsl:value-of select="."/></option>
                </xsl:for-each>
              </select>
            </td>
          </xsl:if>
          <xsl:choose>
            <xsl:when test="count(explain/serverInfo/database) &gt; 1">
              <td><xsl:call-template name="form.databases"/></td>
            </xsl:when>
            <xsl:otherwise>
              <xsl:call-template name="form.databases"/>
            </xsl:otherwise>
          </xsl:choose>
          </tr>
          </table>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="form.databases"/>
        </xsl:otherwise>
      </xsl:choose>
<!-- End of materials, languages, databases sections -->
      <br/>
      <xsl:call-template name="form.input.fields"/>
      <br/>
 
      <xsl:choose>
        <xsl:when test="$pda.mode">
          <br/>
          <xsl:call-template name="form.buttons"/>
        </xsl:when>
        <xsl:otherwise>
      <table>
      <tr>
      <td class="buttons">

<!-- Record syntaxes list -->

        <xsl:choose>
          <xsl:when test="count(explain[1]/recordInfo/recordSyntax) = 1">
            <input name="RECSYNTAX" type="hidden" value="{explain[1]/recordInfo/recordSyntax/@oid}"/>
          </xsl:when>
          <xsl:when test="$include.recsyn.list and count(explain/configInfo/setting[@type='include.recsyn.list']) = 0 or
	explain/configInfo/setting[@type='include.recsyn.list' and .='true']">
            <xsl:if test="$simplify.recsyn.list and explain[1]/recordInfo/recordSyntax[@oid='1.2.840.10003.5.102']">
              <input type="checkbox" name="SHOW_HOLDINGS" onclick="showHoldings(this.form)"/>
              <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SHOW_HOLDINGS']"/>
              <br/>
            </xsl:if>
            <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_RECSYN']"/>
            <xsl:element name="select">
              <xsl:attribute name="name">RECSYNTAX</xsl:attribute>
              <xsl:attribute name="class">edit-field</xsl:attribute>
              <xsl:if test="$simplify.recsyn.list and explain[1]/recordInfo/recordSyntax[@oid='1.2.840.10003.5.102']">
                <xsl:attribute name="onChange">recordSyntax(this.form)</xsl:attribute>
              </xsl:if>
              <xsl:for-each select="explain[1]/recordInfo/recordSyntax[generate-id()=generate-id(key('rskey', @oid))]">
                <option value="{@oid}"><xsl:value-of select="@name"/></option>
              </xsl:for-each>
            </xsl:element>
            <br/>
          </xsl:when>
          <xsl:when test="explain[1]/recordInfo/recordSyntax[@oid='1.2.840.10003.5.102']">
            <input type="checkbox" name="SHOW_HOLDINGS" checked=""/>
            <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SHOW_HOLDINGS']"/>
            <br/>
          </xsl:when>
          <xsl:when test="explain[1]/configInfo/setting[@type='include.record.syntax']">
            <xsl:variable name="n" select="explain[1]/configInfo/setting[@type='include.record.syntax']"/>
            <xsl:for-each select="explain[1]/recordInfo/recordSyntax[generate-id()=generate-id(key('rskey', @oid)) and position() &lt;=$n]">
              <input name="RECSYNTAX" type="hidden" value="{@oid}"/>
            </xsl:for-each>
          </xsl:when>
        </xsl:choose>

<!-- Duplicate detection -->

        <xsl:if test="count(explain/configInfo/supports[@type='option' and .='duplicateDetection']) &gt; 0 and $dedup">
          <input type="checkbox" name="DEDUP"/>
          <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_DEDUP']"/>
          <br/>
        </xsl:if>

<!-- Records portion size -->

        <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_MAXREC']"/>
        <input name="MAXRECORDS" value="{$num.records}" size="{$num.records.size}" maxlength="{$num.records.size}" class="edit-field"/>
        <br/>
      </td>
      <td class="buttons">

<!-- Sort -->

        <xsl:if test="count(explain[serverInfo/database != 'IR-Extend-1']/indexInfo/index[@sort='true']) &gt; 0 and $sort">
          <xsl:variable name="x" select="current()"/>

          <input type="checkbox" name="SORT"/>
          <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SORT']"/>
          <select name="SORT_KEY" class="edit-field">
            <xsl:for-each select="$pa/attributes/attr">
              <xsl:if test="count($x/explain[serverInfo/database != 'IR-Extend-1']/indexInfo/index[@sort='true']/map[attr[@type='1']=current()/@value]) &gt; 0">
                <option value="{@value}"><xsl:value-of select="$ad/attributes/set[@id=$attribute.set]/localization[@lang=$lang]/attr[@type='1' and @value=current()/@value]"/></option>
              </xsl:if>
            </xsl:for-each>
          </select>
          <br/>
        </xsl:if>

<!-- Query expansion -->

        <xsl:if test="$query.expansion and count(explain/configInfo/setting[@type='query.expansion']) = 0 or
	count(explain/configInfo/setting[@type='query.expansion' and .='true']) &gt; 0">
          <input type="checkbox" name="EXPAND"/>
          <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_EXPAND']"/>
          <br/>
          <select name="EXPAND_SOURCE" class="edit-field">
            <xsl:for-each select="$ed/target/explain">
              <option value="z39.50s://{serverInfo/host}:{serverInfo/port}/{serverInfo/database}?cs={configInfo/setting[@type='charset']}&#38;type={configInfo/setting[@type='scheme']}">
                <xsl:value-of select="databaseInfo/title[@lang=$lang]"/>
              </option>
            </xsl:for-each>
          </select>
          <br/>
        </xsl:if>

        <br/>
        <xsl:if test="not($pda.mode)">
          <xsl:call-template name="form.buttons"/>
        </xsl:if>
      </td>
      </tr>
      </table>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
  
  <xsl:call-template name="form.search.profiles"/>
  
  </form>
</xsl:template>

<xsl:template name="form.input.fields">
  <xsl:call-template name="form.term">
    <xsl:with-param name="number" select="'1'"/>
  </xsl:call-template>
  <xsl:call-template name="form.operator">
    <xsl:with-param name="number" select="'1'"/>
  </xsl:call-template>
  <xsl:call-template name="form.term">
    <xsl:with-param name="number" select="'2'"/>
  </xsl:call-template>
  <xsl:if test="not($pda.mode)">
    <xsl:call-template name="form.operator">
      <xsl:with-param name="number" select="'2'"/>
    </xsl:call-template>
    <xsl:call-template name="form.term">
      <xsl:with-param name="number" select="'3'"/>
    </xsl:call-template>
  </xsl:if>
</xsl:template>

<xsl:template name="form.term">
  <xsl:param name="number" select="'1'"/>

  <xsl:call-template name="form.ap.list">
    <xsl:with-param name="number" select="$number"/>
  </xsl:call-template>
  <xsl:if test="$include.relation.attrs">
    <xsl:call-template name="form.relation.list">
      <xsl:with-param name="number" select="$number"/>
    </xsl:call-template>
  </xsl:if>
  <xsl:text> </xsl:text>
  <xsl:element name="input">
    <xsl:attribute name="name">TERM_<xsl:value-of select="$number"/></xsl:attribute>
    <xsl:attribute name="size"><xsl:value-of select="$term.size"/></xsl:attribute>
    <xsl:attribute name="maxlength"><xsl:value-of select="$term.size.max"/></xsl:attribute>
    <xsl:if test="$scan.to.form or $include.virtual.kbd or $include.dialog and count(explain/configInfo/setting[@type='include.dialog']) = 0 or
	count(explain/configInfo/setting[@type='include.dialog' and .='true']) &gt; 0">
      <xsl:attribute name="onclick">setTerm('TERM_<xsl:value-of select="$number"/>')</xsl:attribute>
      <xsl:attribute name="class">edit-field</xsl:attribute>
    </xsl:if>
  </xsl:element>
  <xsl:if test="$include.structure.attrs">
    <xsl:call-template name="form.structure.list">
      <xsl:with-param name="number" select="$number"/>
    </xsl:call-template>
  </xsl:if>
</xsl:template>

<xsl:template name="form.ap.list">
  <xsl:param name="number" select="'1'"/>
  <xsl:variable name="x" select="current()"/>

  <xsl:if test="count(explain/indexInfo/index/map/attr[@type='1']) &gt; 0">
    <select name="USE_{$number}" class="edit-field">
      <xsl:for-each select="$pa/attributes/attr">
        <xsl:variable name="a">
          <xsl:choose>
            <xsl:when test="count(@attributeSet) &gt; 0">
              <xsl:value-of select="@attributeSet"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="$attribute.set"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:variable>
        <xsl:if test="count($x/explain[serverInfo/database != 'IR-Extend-1']/indexInfo/index/map[attr[@type='1']=current()/@value and (attr[@attributeSet=$a] or count(attr/@attributeSet)=0 and $a=$attribute.set)]) &gt; 0">
          <xsl:element name="option">
            <xsl:if test="@pos=$number">
              <xsl:attribute name="selected"/>
            </xsl:if>
            <xsl:attribute name="value">
               <xsl:if test="count(@attributeSet) &gt; 0">
                 <xsl:value-of select="@attributeSet"/><xsl:text>:</xsl:text>
               </xsl:if>
               <xsl:value-of select="@value"/>
            </xsl:attribute>
            <xsl:value-of select="$ad/attributes/set[@id=$a]/localization[@lang=$lang]/attr[@type='1' and @value=current()/@value]"/>
          </xsl:element>
        </xsl:if>
      </xsl:for-each>
    </select>
  </xsl:if>
</xsl:template>

<xsl:template name="form.relation.list">
  <xsl:param name="number" select="'1'"/>

  <xsl:if test="count(explain/indexInfo/index/map/attr[@type='2']) &gt; 0">
    <select name="REL_{$number}" class="edit-field">
      <xsl:for-each select="explain/indexInfo/index/map/attr[@type='2'][generate-id()=generate-id(key('akey2', .))]">
        <option value="{.}"><xsl:value-of select="$ad/attributes/set[@id=$attribute.set]/localization[@lang=$lang]/attr[@type='2' and @value=current()]"/></option>
      </xsl:for-each>
      <option selected="" value="0"></option>
    </select>
  </xsl:if>
</xsl:template>

<xsl:template name="form.structure.list">
  <xsl:param name="number" select="'1'"/>

  <xsl:if test="count(explain/indexInfo/index/map/attr[@type='4']) &gt; 0">
    <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_AS']"/>
    <select name="STRUCT_{$number}" class="edit-field">
      <xsl:for-each select="explain/indexInfo/index/map/attr[@type='4'][generate-id()=generate-id(key('akey4', .))]">
        <option value="{.}"><xsl:value-of select="$ad/attributes/set[@id=$attribute.set]/localization[@lang=$lang]/attr[@type='4' and @value=current()]"/></option>
      </xsl:for-each>
    </select>
  </xsl:if>
</xsl:template>

<xsl:template name="form.operator">
  <xsl:param name="number" select="'1'"/>
  <br/>
  <select name="BOOLEAN_OP{$number}" class="edit-field">
    <option selected="" value="AND"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_AND']"/></option>
    <option value="OR"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_OR']"/></option>
    <option value="ANDNOT"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_ANDNOT']"/></option>
  </select>
  <br/>
</xsl:template>

<xsl:template name="form.databases">
  <xsl:variable name="cnt" select="count(explain/serverInfo/database)-count(explain/serverInfo[database='IR-Extend-1'])-count(explain[indexInfo/index/map/attr/@attributeSet='1.2.840.10003.3.1000.148.1'])"/>
  <xsl:choose>
    <xsl:when test="$cnt &gt; 1">
      <xsl:variable name="ls">
        <xsl:choose>
          <xsl:when test="$cnt &gt; $list.size">
            <xsl:value-of select="$list.size"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$cnt"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <table border="0" cellpadding="0" cellspacing="0" width="100%" class="area-white">
        <tr>
          <td colspan="3" class="area-blue-sky" height="1"><img src="/images/clear.gif"/></td>
        </tr>
        <tr>
          <td width="1" class="area-blue-sky"><img src="/images/clear.gif"/></td>
          <td class="area-white" width="100%" align="left">
            <div class="visible" id="consarea">            
              <select name="DBNAME" id="DBNAME" multiple="" size="{$ls}" class="edit-field">
                <xsl:for-each select="explain[serverInfo/database != 'IR-Extend-1' and not(indexInfo/index/map/attr[@attributeSet = '1.2.840.10003.3.1000.148.1'])]">
                  <option selected="" value="{serverInfo/database}">
                    <xsl:value-of select="databaseInfo/title[@lang=$lang]"/>
                  </option>
                </xsl:for-each>
              </select>
            </div>
            <div id ="membarea" class="hidden">
              <select name="MEMBDBNAME" id="MEMBDBNAME" multiple="" size="{$ls}" class="edit-field" onchange="setTemporaryProfile()">
              </select>
            </div>         
          </td>
          <td width="1" class="area-blue-sky"><img src="/images/clear.gif"/></td>
        </tr>
        <tr>
          <td align="left" colspan="3" height="20">
            <table border="0"  cellpadding="0" cellspacing="0" height="20">
              <tr>
                <td rowspan="2" height="20" width="2" id="tableft" class="tab-left-selected"><img src="/images/clear.gif"/></td>
                <td height="19" id="tab1" class="area-white"><span class="tab-label" onclick="showConsortiums()">
                  <xsl:attribute name="title"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='TITLE_CONSORTIUMS']"/></xsl:attribute>
                <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_CONSORTIUMS']"/></span></td>
                <td rowspan="2" height="20" width="22" id="tabmiddle" class="tab-middle-selected"><img src="/images/clear.gif"/></td>
                <td height="19" id="tab2" class="area-grey"><span class="tab-label" onclick="showMembers()">
                <xsl:attribute name="title"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='TITLE_MEMBERS']"/></xsl:attribute>
                <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_MEMBERS']"/></span></td>
                <td rowspan="2" height="20" width="23" id="tabright" class="tab-right"><img src="/images/clear.gif"/></td>
              </tr>
              <tr>
                <td height="1" id="tab1bottom" class="area-blue-sky"><img src="/images/clear.gif"/></td>
                <td height="1" id="tab2bottom" class="area-grey-dark"><img src="/images/clear.gif"/></td>            
              </tr>
            </table>
          </td>
        </tr>        
      </table>
    </xsl:when>
    <xsl:otherwise>
      <input type="hidden" name="DBNAME" value="{explain[1]/serverInfo/database}"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="form.buttons">
  <xsl:choose>
    <xsl:when test="explain/indexInfo/index[@scan='true']">
<!--
      <input name="SEARCH" type="image" alt="{$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SEARCH']}" src="{$msg.form/messages/localization[@lang=$lang]/msg[@id='URL_SEARCH_PIC']}" border="0"/>
      <input name="SCAN" type="image" alt="{$msg.form/messages/localization[@lang=$lang]/msg[@id='I_BROWSE']}" src="{$msg.form/messages/localization[@lang=$lang]/msg[@id='URL_BROWSE_PIC']}" border="0"/>
-->
      <xsl:element name="input">
        <xsl:attribute name="name">SEARCH</xsl:attribute>
        <xsl:attribute name="type">submit</xsl:attribute>
        <xsl:attribute name="value"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SEARCH']"/></xsl:attribute>
        <xsl:if test="$resource.reports and count(explain/configInfo/supports[@type='option' and .='resourceCtrl']) &gt; 0">
          <xsl:attribute name="onclick">showProgress('<xsl:value-of select="$cgi.script.URL"/>?report+<xsl:value-of select="$session.id"/>+<xsl:value-of select="$report"/>+<xsl:value-of select="$lang"/>')</xsl:attribute>
        </xsl:if>
        <xsl:attribute name="class">grey-button</xsl:attribute>
      </xsl:element>
      <xsl:choose>
        <xsl:when test="$scan.to.form">
         <xsl:element name="input">
           <xsl:attribute name="type">button</xsl:attribute>
           <xsl:attribute name="value"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_BROWSE']"/></xsl:attribute>
           <xsl:attribute name="onclick">scan('<xsl:value-of select="$cgi.script.URL"/>')</xsl:attribute>
          <xsl:attribute name="class">grey-button</xsl:attribute>           
         </xsl:element>
        </xsl:when>
        <xsl:otherwise>
      <input name="SCAN" type="submit" value="{$msg.form/messages/localization[@lang=$lang]/msg[@id='I_BROWSE']}" class="grey-button"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:element name="input">
        <xsl:attribute name="type">submit</xsl:attribute>
        <xsl:attribute name="value"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_SUBMIT']"/></xsl:attribute>
        <xsl:if test="$resource.reports and count(explain/configInfo/supports[@type='option' and .='resourceCtrl']) &gt; 0">
          <xsl:attribute name="onclick">showProgress('<xsl:value-of select="$cgi.script.URL"/>?report+<xsl:value-of select="$session.id"/>+<xsl:value-of select="$report"/>+<xsl:value-of select="$lang"/>')</xsl:attribute>
        </xsl:if>
        <xsl:attribute name="class">grey-button</xsl:attribute>        
      </xsl:element>
      <input type="reset" value="{$msg.form/messages/localization[@lang=$lang]/msg[@id='I_RESET']}" class="grey-button"/>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:variable name="dir" select="explain[indexInfo/index/map/attr/@attributeSet = '1.2.840.10003.3.1000.148.1']"/>
  <xsl:if test="$dir">
    <xsl:element name="input">
      <xsl:attribute name="type">button</xsl:attribute>
      <xsl:attribute name="value"><xsl:value-of select="$dir/databaseInfo/title[@lang=$lang]"/></xsl:attribute>
      <xsl:attribute name="onclick">scan('<xsl:value-of select="$cgi.script.URL"/>', '<xsl:value-of select="$dir/serverInfo/database"/>', '<xsl:value-of select="$dir/indexInfo/index/map/attr[@type = '1']"/>', '<xsl:value-of select="$dir/indexInfo/index/map/attr[@type = '1']/@attributeSet"/>')</xsl:attribute>
      <xsl:attribute name="class">grey-button</xsl:attribute>      
    </xsl:element>
  </xsl:if>
</xsl:template>

<xsl:template name="form.header">
  <xsl:choose>
    <xsl:when test="$pda.mode">
      <xsl:for-each select="explain[1]/configInfo/setting[@type='title'][@lang=$lang]">
        <h4><xsl:value-of select="."/></h4>
      </xsl:for-each>
      <xsl:if test="count(explain) - count(explain/serverInfo[database='IR-Extend-1']) - count(explain[indexInfo/index/map/attr/@attributeSet='1.2.840.10003.3.1000.148.1'])= 1">
        <h5><xsl:value-of select="explain[1]/databaseInfo/title[@lang=$lang]"/></h5>
      </xsl:if>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="form.bar"/>
      <hr/>
      <xsl:choose>
        <xsl:when test="string-length($logo.left.URL)+string-length($logo.right.URL) &gt; 0">
          <table align="center">
            <tr>
              <xsl:if test="string-length($logo.left.URL) &gt; 0">
                <td><img src="{$logo.left.URL}"/></td>
              </xsl:if>
              <td>
                <xsl:for-each select="explain[1]/configInfo/setting[@type='title'][@lang=$lang]">
                  <h2><xsl:value-of select="."/></h2>
                </xsl:for-each>
              </td>
              <xsl:if test="string-length($logo.right.URL) &gt; 0">
                <td><img src="{$logo.right.URL}"/></td>
              </xsl:if>
            </tr>
          </table>
        </xsl:when>
        <xsl:otherwise>
          <xsl:for-each select="explain[1]/configInfo/setting[@type='title'][@lang=$lang]">
            <h2><xsl:value-of select="."/></h2>
          </xsl:for-each>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="count(explain) - count(explain/serverInfo[database='IR-Extend-1']) - count(explain[indexInfo/index/map/attr/@attributeSet='1.2.840.10003.3.1000.148.1'])= 1">
        <h3><xsl:value-of select="explain[1]/databaseInfo/title[@lang=$lang]"/></h3>
      </xsl:if>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="form.footer">
  <hr/>
  <xsl:call-template name="form.bar"/>
</xsl:template>

<xsl:template name="form.bar">
  <div class="menubar">
    <xsl:if test="$include.profiles">
      <xsl:for-each select="exsl:node-set($modes)/mode">
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?form+{$session.id}+{$target}+{current()/@href}+{$lang}"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id=current()/@label]"/></a><xsl:text> ] </xsl:text>
      </xsl:for-each>
    </xsl:if>
    <xsl:if test="$include.virtual.kbd">
      <xsl:text>[ </xsl:text><a href="#" onclick="showKeyboard()"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_KBD']"/></a><xsl:text> ]</xsl:text>
    </xsl:if>
    <xsl:if test="$include.dialog and count(explain/configInfo/setting[@type='include.dialog']) = 0 or
	explain/configInfo/setting[@type='include.dialog' and .='true']">
    <xsl:text>[ </xsl:text><a href="#" onclick="openDialog()"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_CLASS']"/></a><xsl:text> ]</xsl:text>
    </xsl:if>
    <xsl:if test="$include.help">
      <xsl:text>[ </xsl:text><a href="{$help.URL}"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='I_HELP']"/></a><xsl:text> ]</xsl:text>
    </xsl:if>
  </div>
</xsl:template>

<xsl:template name="form.search.profiles">
<!-- The list of stored searching profiles -->
  <br/>
  <table border="0" cellpadding="0" cellspacing="1" class="area-grey">
    <tr>
      <td>
        <table border="0" cellpadding="0" cellspacing="1" width="100%" class="area-white">
          <tr>
            <td>
              <div class="visible">
                <table border="0" cellpadding="0" cellspacing="0">
                  <tr>
                    <td>
                      <div class="option-label">
                        <xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_SEARCH_PROFILES']"/>
                      </div>
                    </td>
                    <td>
                      <select size="1" id="profilelist" disabled="" selectedIndex="0" class="edit-field" onchange="applyProfile()">
                        <option value="-1" selected=""><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_PROFILE_NOT_SET']"/></option>
                      </select>
                    </td>
                    <td>
                      <div class="option-text">
                        <span id="savebtn" class="hidden"><a href="javascript:saveProfile()" class="blue-anchor"><xsl:attribute name="title"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_SAVE_SEARCH_OPTIONS_INTO_PROFILE']"/></xsl:attribute><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_SAVE']"/></a></span><span id="nosavebtn" class="visible"><span class="disabled-anchor"><xsl:attribute name="title"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_SAVE_SEARCH_OPTIONS_INTO_PROFILE']"/></xsl:attribute><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_SAVE']"/></span></span>
                      </div>
                    </td>
                    <td>
                      <div class="option-text">
                        <span id="deletebtn" class="hidden"><a href="javascript:deleteProfile()" class="blue-anchor"><xsl:attribute name="title"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_DELETE_SEARCH_PROFILE']"/></xsl:attribute><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_DELETE']"/></a></span><span id="nodeletebtn" class="visible"><span class="disabled-anchor"><xsl:attribute name="title"><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='MSG_DELETE_SEARCH_PROFILE']"/></xsl:attribute><xsl:value-of select="$msg.form/messages/localization[@lang=$lang]/msg[@id='LAB_DELETE']"/></span></span>
                      </div>
                    </td>
                  </tr>
                </table>
              </div>
            </td>
          </tr>
        </table> 
      </td>
    </tr>
  </table>
  <br/>
<!-- End of the list of stored searching profiles -->
</xsl:template>

</xsl:stylesheet>

