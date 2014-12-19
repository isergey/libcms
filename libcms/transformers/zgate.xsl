<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: zgate.xsl,v $
 * Revision 1.67  2011/04/28 05:30:54  rustam
 * Conditional translation with PVM
 *
 * Revision 1.66  2011/03/25 11:25:56  rustam
 * Implemented record number output via CSS 2.1 count()
 *
 * Revision 1.65  2010/12/30 14:32:32  rustam
 * Minor corrections
 *
 * Revision 1.64  2010/12/18 16:29:58  rustam
 * Persistent query
 *
 * Revision 1.63  2010/12/17 14:32:25  rustam
 * interface redesign
 *
 * Revision 1.62  2010/11/03 10:58:04  rustam
 * A pair of new navigation buttons - to the start and to the end of result set
 * Javascript record postprocessing
 *
 * Revision 1.61  2010/06/11 14:07:52  rustam
 * Further tatar translation
 *
 * Revision 1.60  2009/12/08 14:13:31  rustam
 * Improved search term processing
 *
 * Revision 1.59  2009/07/15 10:40:24  rustam
 * Implementing Periodic Query Schedule
 *
 * Revision 1.58  2009/04/14 08:18:12  rustam
 * Improved diagnostics
 *
 * Revision 1.57  2008/05/27 11:34:43  rustam
 * Linking attributes are parameterized
 *
 * Revision 1.56  2008/01/25 12:30:58  rustam
 * Minor change
 *
 * Revision 1.55  2007/04/28 12:44:09  rustam
 * Implemented passing user ID as a form command argument
 *
 * Revision 1.54  2006/12/11 15:20:14  rustam
 * Improved interlevel linking (from 1-volume monograph to analytics)
 *
 * Revision 1.53  2006/11/10 12:38:08  rustam
 * Implemented links for multivolume monographs
 *
 * Revision 1.52  2006/05/30 12:09:37  rustam
 * Corrected bug with circulation desks
 *
 * Revision 1.51  2006/05/17 10:04:01  rustam
 * Minor improvements
 *
 * Revision 1.50  2006/03/17 08:14:15  rustam
 * Implemented selection of circulation desks during preorder phase
 *
 * Revision 1.49  2006/02/14 10:01:01  rustam
 * Further improvements
 *
 * Revision 1.48  2005/09/27 07:08:34  rustam
 * Added XML records representation
 *
 * Revision 1.47  2005/09/07 11:57:17  rustam
 * Minor corrections
 *
 * Revision 1.46  2005/09/07 11:38:48  rustam
 * Implemented order restrictions
 *
 * Revision 1.45  2005/02/28 10:12:56  rustam
 * Implemented related record search
 *
 * Revision 1.44  2004/10/13 05:49:16  rustam
 * Minor scan improvements corresponding to IIS compatibility
 *
 * Revision 1.43  2004/06/22 10:52:53  rustam
 * globalOccurences is optional!
 *
 * Revision 1.42  2004/05/24 08:14:35  rustam
 * Minor improvements
 *
 * Revision 1.41  2004/05/21 09:21:58  rustam
 * Implemented linking to authority records
 *
 * Revision 1.40  2004/04/06 06:19:36  rustam
 * Minor changes
 *
 * Revision 1.39  2004/02/02 11:22:39  rustam
 * Minor improvement
 *
 * Revision 1.38  2003/11/12 19:33:17  rustam
 * Downloading of selected records
 *
 * Revision 1.37  2003/11/05 08:44:44  rustam
 * Minor changes
 *
 * Revision 1.36  2003/10/13 11:37:22  rustam
 * Minor improvements
 *
 * Revision 1.35  2003/09/30 11:28:33  rustam
 * Implemented new scan method
 *
 * Revision 1.34  2003/09/16 07:27:22  rustam
 * Added parameter item.order
 *
 * Revision 1.33  2003/06/18 08:58:57  rustam
 * Corrected minor bug
 *
 * Revision 1.32  2003/05/27 08:37:58  rustam
 * Implemented UTF-8 records validation
 *
 * Revision 1.31  2003/05/16 06:53:56  rustam
 * Minor changes
 *
 * Revision 1.30  2003/05/15 10:41:12  rustam
 * Minor corrections
 *
 * Revision 1.29  2003/05/15 07:27:45  rustam
 * Implemented profiles
 *
 * Revision 1.28  2003/04/16 07:41:41  rustam
 * Corrected error with scan results
 *
 * Revision 1.27  2003/04/08 11:36:33  rustam
 * Minor changes
 *
 * Revision 1.26  2003/04/02 13:45:19  rustam
 * Corrected bug with error codes
 *
 * Revision 1.25  2003/02/03 13:59:07  web
 * Minor changes
 *
 * Revision 1.24  2003/01/31 14:12:17  rustam
 * New pre-release
 *
 * Revision 1.23  2002/10/09 07:56:40  rustam
 * Corrected bug (incorrect record representation)
 *
 * Revision 1.22  2002/08/14 08:40:00  rustam
 * Reworked stylesheets
 *
 * Revision 1.21  2002/07/17 13:06:22  rustam
 * Imroved follow command processing
 *
 * Revision 1.20  2002/07/15 07:01:51  web
 * Minor changes
 *
 * Revision 1.19  2002/06/18 12:14:55  web
 * Minor changes
 *
 * Revision 1.18  2002/06/18 12:09:08  rustam
 * Minor changes
 *
 * Revision 1.17  2002/05/21 09:32:34  rustam
 * Minor changes
 *
 * Revision 1.16  2002/05/08 09:29:58  rustam
 * Some improvements
 *
 * Revision 1.15  2002/04/15 12:07:02  rustam
 * Added support for organization name representation by code
 *
 * Revision 1.14  2002/03/20 12:47:59  web
 * Minor changes
 *
 * Revision 1.13  2002/03/07 14:48:24  web
 * Minor changes
 *
 * Revision 1.12  2002/02/27 07:32:37  rustam
 * Minor changes
 *
 * Revision 1.11  2002/02/20 13:22:31  rustam
 * Added support for subseries representation
 *
 * Revision 1.10  2002/02/13 12:45:12  rustam
 * Improved MARC diagnostics
 *
 * Revision 1.9  2002/02/04 10:21:07  rustam
 * Added support for bad MARC records presentation
 *
 * Revision 1.8  2001/11/20 14:41:45  web
 * Minor changes
 *
 * Revision 1.7  2001/10/18 09:50:04  web
 * Minor changes
 *
 * Revision 1.6  2001/09/27 09:21:14  web
 * Implemented GRS-1 records presentation via XSLT
 *
 * Revision 1.5  2001/09/20 11:58:25  web
 * Minor changes
 *
 * Revision 1.4  2001/09/19 13:58:18  web
 * Minor changes
 *
 * Revision 1.3  2001/09/10 13:36:38  web
 * Minor changes
 *
 * Revision 1.2  2001/09/07 14:55:09  web
 * Minor bug corrected
 *
 * Revision 1.1  2001/09/03 12:15:13  web
 * Added new XML-based record representation engine
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str"> 
<xsl:import href="xml.xsl"/>
<xsl:include href="grs-1.xsl"/>
<xsl:include href="estp.xsl"/>
<xsl:include href="opac.xsl"/>
<xsl:output
	method="html"
	indent="yes"
	encoding="utf-8"
	standalone="no"
	omit-xml-declaration="yes"
/>

<xsl:template match="results">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html;charset={$charset}"/>
      <link href="{$stylesheet.URL}" rel="stylesheet" type="text/css"/>
      <xsl:if test="$scan.to.form or $hide.diag or $marc.download and $download.selected">
        <script type="text/javascript" src="{$java.script.URL}" charset="{$charset}"></script>
      </xsl:if>
      <title>
        <xsl:choose>
          <xsl:when test="@type='SearchResponse' or @type='ScanResponse'">
            <xsl:value-of select="database"/>
            <xsl:text>[</xsl:text><xsl:value-of select="term"/><xsl:text>]</xsl:text>
          </xsl:when>
          <xsl:when test="@type='PresentResponse'">
            <xsl:value-of select="resultSet"/>
            <xsl:text>[</xsl:text><xsl:value-of select="$start"/><xsl:text>/</xsl:text><xsl:value-of select="resultCount"/><xsl:text>]</xsl:text>
          </xsl:when>
          <xsl:when test="@type='preorder' or @type='order'">
            <xsl:value-of select="resultSet"/>
            <xsl:text>[</xsl:text><xsl:value-of select="$start"/><xsl:text>]</xsl:text>
          </xsl:when>
          <xsl:when test="@type='prepqs' or @type='pqs'">
            <xsl:value-of select="database"/>
            <xsl:text>[</xsl:text><xsl:value-of select="term"/><xsl:text>]</xsl:text>
          </xsl:when>
        </xsl:choose>
      </title>
    </head>
  <xsl:element name="body">
  <xsl:if test="$marc.download and $download.selected">
    <xsl:attribute name="onload">processSelected()</xsl:attribute>
  </xsl:if>
  <xsl:call-template name="res.header"/>

  <xsl:if test="SearchResponse/searchStatus = 'false'">
    <xsl:choose>
      <xsl:when test="resultSetStatus = '1'">
        <div class="fail">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_SEARCHS']"/>
        </div>
      </xsl:when>
      <xsl:otherwise>
        <div class="fail">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_SEARCH']"/>
        </div>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:for-each select="SearchResponse/error">
      <div class="error">
        <xsl:value-of select="."/>
      </div>
    </xsl:for-each>
    <xsl:for-each select="SearchResponse/record">
      <xsl:call-template name="record.selector">
        <xsl:with-param name="hideable" select="true()"/>
      </xsl:call-template>
    </xsl:for-each>
  </xsl:if>

  <xsl:if test="DuplicateDetectionResponse/status = 'false'">
    <div class="fail">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_DEDUP']"/>
    </div>
    <xsl:for-each select="DuplicateDetectionResponse/error">
      <div class="error">
        <xsl:value-of select="."/>
      </div>
    </xsl:for-each>
    <xsl:for-each select="DuplicateDetectionResponse/record">
      <xsl:call-template name="record.selector"/>
    </xsl:for-each>
  </xsl:if>

  <xsl:if test="SortResponse/sortStatus=2">
    <div class="fail">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_SORT']"/>
    </div>
    <xsl:for-each select="SortResponse/error">
      <div class="error">
        <xsl:value-of select="."/>
      </div>
    </xsl:for-each>
    <xsl:for-each select="SortResponse/record">
      <xsl:call-template name="record.selector"/>
    </xsl:for-each>
  </xsl:if>

  <xsl:if test="ESResponse/operationStatus=3">
    <div class="fail">
      <xsl:choose>
        <xsl:when test="ESResponse/@type='order'">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_ORDER']"/>
        </xsl:when>
        <xsl:when test="ESResponse/@type='delete'">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_DELETE']"/>
        </xsl:when>
      </xsl:choose>
    </div>
    <xsl:for-each select="ESResponse/error">
      <div class="error">
        <xsl:value-of select="."/>
      </div>
    </xsl:for-each>
    <xsl:for-each select="ESResponse/record">
      <xsl:call-template name="record.selector"/>
    </xsl:for-each>
  </xsl:if>

  <xsl:choose>
    <xsl:when test="@type='SearchResponse'">
      <div class="succ">
      <xsl:choose>
        <xsl:when test="resultSetStatus = '1'">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SEARCHS']"/>
        </xsl:when>
        <xsl:when test="resultCount">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SEARCH']"/>
        </xsl:when>
      </xsl:choose>
      </div>
    </xsl:when>
    <xsl:when test="@type='ScanResponse'">
      <xsl:choose>
        <xsl:when test="scanStatus != '6'">
          <div class="succ">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SCAN']"/>
          </div>
          <xsl:choose>
            <xsl:when test="scanStatus = '1'">
              <div class="error">
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SCAN_1']"/>
              </div>
            </xsl:when>
            <xsl:when test="scanStatus = '2'">
              <div class="error">
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SCAN_2']"/>
              </div>
            </xsl:when>
            <xsl:when test="scanStatus = '3'">
              <div class="error">
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SCAN_3']"/>
              </div>
            </xsl:when>
            <xsl:when test="scanStatus = '4'">
              <div class="error">
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_SCAN_4']"/>
              </div>
            </xsl:when>
          </xsl:choose>
          <xsl:for-each select="error">
            <div class="error">
              <xsl:value-of select="."/>
            </div>
          </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
          <div class="fail">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_SCAN']"/>
          </div>
        </xsl:otherwise>
      </xsl:choose>
      <hr/>
    </xsl:when>

<!-- UNSUPPORTED OPERATION -->
    <xsl:when test="@type='unsupported'">
      <div class="fail">
        <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_UNSUPP']"/>
      </div>
    </xsl:when>
<!-- PREORDER -->

    <xsl:when test="@type='preorder'">
      <div class="succ">
      <xsl:choose>
        <xsl:when test="stage=1">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_PREORDER']"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/illst[@id=current()/illServiceType]"/>
        </xsl:otherwise>
      </xsl:choose>
      </div>
      <form method="POST" action="{$cgi.script.URL}">
        <input name="RSNAME" type="hidden" value="{resultSet}"/>
        <input name="START" type="hidden" value="{$start}"/>
        <input name="LANG" type="hidden" value="{$lang}"/>
        <input name="SESSION_ID" type="hidden" value="{$session.id}"/>
        <input name="STAGE" type="hidden" value="{stage+1}"/>
        <table class="order">
          <tr>
            <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_USERID']"/></td>
            <td class="data"><xsl:value-of select="$user.id"/></td>
          </tr>
          <tr>
            <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_ITM']"/></td>
            <td class="data">
              <xsl:for-each select="record">
                <xsl:call-template name="record.selector"/>
              </xsl:for-each>
            </td>
          </tr>
        </table>
        <xsl:choose>
          <xsl:when test="stage=1">
            <div>
            <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_VOL']"/></span>
            <span class="data"><input name="VOLUME_ISSUE" size="15" MAXLENGTH="40"/></span>
            </div>
            <div>
            <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_REQ_NOTE']"/></span>
            <span class="data"><input name="REQUESTER_NOTE" size="15" MAXLENGTH="40"/></span>
            </div>
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_IS']"/>
            <select name="ILL_SERVICE">
              <option selected="" value="1"><xsl:value-of select="$msg/messages/localization[@language=$lang]/ills[@id='1']"/></option>
              <option value="2"><xsl:value-of select="$msg/messages/localization[@language=$lang]/ills[@id='2']"/></option>
              <option value="3"><xsl:value-of select="$msg/messages/localization[@language=$lang]/ills[@id='3']"/></option>
              <option value="4"><xsl:value-of select="$msg/messages/localization[@language=$lang]/ills[@id='4']"/></option>
            </select>
            <xsl:if test="record/holdingsData/holdingsAndCirc/nucCode">
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_AT']"/>
              <xsl:for-each select="record/holdingsData/holdingsAndCirc[circulationData/circRecord/restrictions != $order.restriction or not(circulationData/circRecord/restrictions)]">
                <xsl:sort select="nucCode"/>
                <xsl:sort select="localLocation"/>
                <xsl:if test="position() = 1 or position() != 1 and
		(nucCode != preceding-sibling::holdingsAndCirc[position()=1]/nucCode
		or localLocation != preceding-sibling::holdingsAndCirc[position()=1]/localLocation)">
                  <br/><input name="IO_LOCATION" type="radio" value="{nucCode}/{localLocation}"/>
                  <xsl:call-template name="org.by.code">
                    <xsl:with-param name="oname" select="nucCode"/>
                  </xsl:call-template>
                  <xsl:text>/</xsl:text>
                  <xsl:call-template name="unit.by.code">
                    <xsl:with-param name="uname" select="localLocation"/>
                  </xsl:call-template>
                  <xsl:if test="$circ.desk/units/localization[@language=$lang]/unit[@id=current()/localLocation]">
                    <xsl:text> - </xsl:text>
                    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_CIRC_DESK']"/>
                    <select name="CIRC_DESK">
                      <xsl:for-each select="$circ.desk/units/localization[@language=$lang]/unit[@id=current()/localLocation]/desk">
                        <option value="{../@id}/{@id}"><xsl:value-of select="."/></option>
                      </xsl:for-each>
                    </select>
                  </xsl:if>
                </xsl:if>
              </xsl:for-each>
            </xsl:if>
            <input name="ACTION" type="hidden" value="PREORDER"/>
            <input name="RECSYNTAX" type="hidden" value="{$record.syntax}"/>
            <div align="center">
              <input type="submit" value="{$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_CONTINUE']}"/>
            </div>
          </xsl:when>
          <xsl:when test="stage=2">
            <xsl:if test="count(volumeIssue) &gt; 0">
              <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_VOL']"/></span>
              <span class="data"><input name="VOLUME_ISSUE" size="15" MAXLENGTH="40" value="{volumeIssue}"/></span>
            </xsl:if>
            <br/>
            <input name="ILL_SERVICE" type="hidden" value="{illServiceType}"/>
            <xsl:if test="count(location) &gt; 0">
              <input name="IO_LOCATION" type="hidden" value="{location}"/>
            </xsl:if>
            <xsl:choose>
              <xsl:when test="illServiceType=1">
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_HOLD']"/>
                <br/>
                <select name="PLACE_ON_HOLD">
                  <option value="1"><xsl:value-of select="$msg/messages/localization[@language=$lang]/hold[@id='1']"/></option>
                  <option value="2"><xsl:value-of select="$msg/messages/localization[@language=$lang]/hold[@id='2']"/></option>
                  <option selected="" value="3"><xsl:value-of select="$msg/messages/localization[@language=$lang]/hold[@id='3']"/></option>
                </select>
                <input name="ACTION" type="hidden" value="ORDER"/>
                <div align="center">
                  <input type="submit" value="{$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_PREORDER']}"/>
                </div>
              </xsl:when>
              <xsl:when test="illServiceType=2">
                <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_PAG']"/></span>
                <span class="data"><input name="PAGINATION" size="15" MAXLENGTH="40" value="{pagination}"/></span>
                <br/>
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_MEDIUM']"/>
                <select name="MEDIUM">
                  <option value="1"><xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id='1']"/></option>
                  <option value="2"><xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id='2']"/></option>
                  <option value="3"><xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id='3']"/></option>
                  <option value="4"><xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id='4']"/></option>
                  <option value="5"><xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id='5']"/></option>
                  <option selected="" value="6"><xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id='6']"/></option>
                </select>
                <input name="ACTION" type="hidden" value="PREORDER"/>
                <div align="center">
                  <input type="submit" value="{$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_CONTINUE']}"/>
                </div>
              </xsl:when>
              <xsl:when test="illServiceType=3 or illServiceType=4">
                <input name="ACTION" type="hidden" value="ORDER"/>
                <div align="center">
                  <input type="submit" value="{$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_INQUIRE']}"/>
                </div>                
              </xsl:when>
            </xsl:choose>
          </xsl:when>
          <xsl:when test="stage=3">
            <xsl:if test="count(volumeIssue) &gt; 0">
              <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_VOL']"/></span>
              <span class="data"><input name="VOLUME_ISSUE" size="15" MAXLENGTH="40" value="{volumeIssue}"/></span>
            </xsl:if>
            <br/>
            <xsl:if test="count(pagination) &gt; 0">
              <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_PAG']"/></span>
              <span class="data"><input name="PAGINATION" size="15" MAXLENGTH="40" value="{pagination}"/></span>
            </xsl:if>
            <br/>
            <span class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_IO_MT']"/></span>
            <span class="data">
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/medium[@id=current()/mediumType]"/>
              <xsl:if test="count(mediumCharacteristics) &gt; 0">
                <xsl:text>, </xsl:text>
                <xsl:value-of select="$msg/messages/localization[@language=$lang]/mchar[@id=current()/mediumCharacteristics]"/>
              </xsl:if>
            </span>
            <input name="ILL_SERVICE" type="hidden" value="{illServiceType}"/>
            <xsl:if test="count(location) &gt; 0">
              <input name="IO_LOCATION" type="hidden" value="{location}"/>
            </xsl:if>
            <input name="MEDIUM_TYPE" type="hidden" value="{mediumType}"/>
            <xsl:if test="count(mediumCharacteristics) &gt; 0">
              <input name="MEDIUM_CHAR" type="hidden" value="{mediumCharacteristics}"/>
            </xsl:if>
            <input name="ACTION" type="hidden" value="ORDER"/>
            <div align="center">
              <input type="submit" value="{$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_PREORDER']}"/>
            </div>
          </xsl:when>
        </xsl:choose>
      </form>
    </xsl:when>

    <xsl:when test="@type='order'">
      <xsl:if test="count(ESResponse[operationStatus=3]) &lt; 1">
        <div class="succ">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_ORDER']"/>
        </div>
      </xsl:if>
    </xsl:when>

    <xsl:when test="@type='delete'">
      <xsl:if test="count(ESResponse[operationStatus=3]) &lt; 1">
        <div class="succ">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_DELETE']"/>
        </div>
      </xsl:if>
    </xsl:when>

    <xsl:when test="@type='prepqs'">
      <div class="succ">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_PREPQS']"/>
      </div>
      <form method="POST" action="{$cgi.script.URL}">
        <input name="ACTION" type="hidden" value="PQS"/>
        <input name="DB" type="hidden" value="{database}"/>
        <input name="TERM" type="hidden" value="{term}"/>
        <input name="LANG" type="hidden" value="{$lang}"/>
        <input name="SESSION_ID" type="hidden" value="{$session.id}"/>
        <table class="order">
          <tr>
            <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DB']"/></td>
            <td class="data"><xsl:value-of select="database"/></td>
          </tr>
          <tr>
            <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_QUERY']"/></td>
            <td class="data"><xsl:value-of select="term"/></td>
          </tr>
          <tr>
            <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_PERIOD']"/></td>
            <td class="data">
              <select name="PERIOD">
                <option value="86400"><xsl:value-of select="$msg/messages/localization[@language=$lang]/period[@id='DAILY']"/></option>
                <option value="604800"><xsl:value-of select="$msg/messages/localization[@language=$lang]/period[@id='WEEKLY']"/></option>
                <option value="2592000"><xsl:value-of select="$msg/messages/localization[@language=$lang]/period[@id='MONTHLY']"/></option>
              </select>
            </td>
          </tr>
          <tr>
            <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DEST']"/></td>
            <td class="data"><input name="DESTINATION" size="15" MAXLENGTH="40" value=""/></td>
          </tr>
        </table>
        <div align="center">
          <input type="submit" value="{$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_PREPQS']}"/>
        </div>
      </form>
    </xsl:when>

  </xsl:choose>

  <xsl:if test="resultCount = 0">
    <span class="warn">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_NOT_FOUND']"/>
    </span>
  </xsl:if>

  <xsl:if test="PresentResponse/presentStatus='0'">
    <div class="fail">
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='F_OP_PRESENT']"/>
    </div>
  </xsl:if>

  <xsl:if test="resultCount &gt; 0 and @type != 'order'">
    <xsl:choose>
      <xsl:when test="count(record) = 0">
        <span class="warn">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='W_NO_REC']"/>
        </span>
        <xsl:for-each select="PresentResponse/error">
          <div class="error">
            <xsl:value-of select="."/>
          </div>
        </xsl:for-each>
     </xsl:when>
      <xsl:otherwise>
        <span class="succ">
          <xsl:choose>
            <xsl:when test="$lang='tat'">
              <xsl:value-of select="resultCount"/>
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_FOUND1']"/>
              <span class="start" style="counter-increment: r {$start - 1};"><xsl:value-of select="$start"/></span>
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_FOUND2']"/>
              <xsl:value-of select="$start + count(record) - 1"/>
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_FOUND3']"/>
           </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_FOUND1']"/>
              <span class="start" style="counter-increment: r {$start - 1};"><xsl:value-of select="$start"/></span>
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_FOUND2']"/>
              <xsl:value-of select="$start + count(record) - 1"/>
              <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_OP_FOUND3']"/>
              <xsl:value-of select="resultCount"/>
            </xsl:otherwise>
          </xsl:choose>
        </span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:if>

<!-- Records received during ANY operation exluding PREORDER -->
  <xsl:if test="@type != 'preorder'">
    <xsl:for-each select="record">
      <xsl:call-template name="record.selector"/>

      <xsl:if test="@syntax != 'diagnostic'">
        <xsl:call-template name="record.menu"/>
      </xsl:if>
    </xsl:for-each>
    <xsl:if test="string-length($check.records) &gt; 0">
      <script type="text/javascript"><xsl:value-of select="$check.records"/></script>
    </xsl:if>
  </xsl:if>

<!-- Entries received during SCAN operation -->  
  <xsl:if test="termInfo">
    <xsl:variable name="attr" select="concat('[', substring-after(term, '['))"/>
    <xsl:variable name="attr.val" select="substring-before(substring-after(substring-after(term, '['), ','), ',')"/>
<!--
    <xsl:if test="record">
      <hr/>
    </xsl:if>
-->
    <table class="scan">
      <tr>
        <xsl:if test="termInfo/globalOccurences">
          <th><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_MSG_ENTRIES']"/></th>
        </xsl:if>
        <th><xsl:value-of select="$ad/attributes/set[@id=$attribute.set]/localization[@lang=$lang]/attr[@type='1' and @value=$attr.val]"/></th>
      </tr>
      <xsl:for-each select="termInfo">
        <tr>
          <xsl:if test="globalOccurences">
            <td class="occur"><xsl:value-of select="globalOccurences"/></td>
          </xsl:if>
          <td class="terminfo">
            <xsl:element name="a">
              <xsl:choose>
                <xsl:when test="$scan.to.form">
                  <xsl:attribute name="href">javascript:setForm('<xsl:value-of select="term"/>')</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:attribute name="href"><xsl:value-of select="$cgi.script.URL"/>?ACTION=SEARCH&amp;SESSION_ID=<xsl:value-of select="$session.id"/>&amp;DBNAME=<xsl:value-of select="../database"/>&amp;ESNAME=<xsl:value-of select="$fmt"/>&amp;RECSYNTAX=<xsl:value-of select="$record.syntax"/>&amp;MAXRECORDS=<xsl:value-of select="$max.records"/>&amp;ATTSET=<xsl:value-of select="$attribute.set"/>&amp;LANG=<xsl:value-of select="$lang"/>&amp;TERM_1=<xsl:value-of select="str:encode-uri(term, true())"/><xsl:value-of select="$attr"/></xsl:attribute>
                </xsl:otherwise>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="count(displayTerm) &gt; 0">
                  <xsl:value-of select="displayTerm"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="term"/>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:if>

  <xsl:call-template name="res.footer"/>
  </xsl:element>
  </html>
</xsl:template>

<xsl:template name="record.incorrect">
  <span class="warn">
    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='W_MRC_BAD']"/>
    <xsl:text>: </xsl:text>
    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id=current()/@code]"/>
  </span>
</xsl:template>

<xsl:template name="record.not.utf8">
  <span class="warn">
    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='W_NOT_UTF8']"/>
  </span>
</xsl:template>

<xsl:template name="record.diagnostic">
  <xsl:param name="hideable" select="false()"/>
  <xsl:element name="div">
    <xsl:attribute name="class">diag</xsl:attribute>
    <xsl:if test="$hideable and $hide.diag and count(../record[@syntax='diagnostic']) &gt; $diag.threshold">
      <xsl:attribute name="style">display: none;</xsl:attribute>
    </xsl:if>
    <xsl:variable name="n1" select="string(diagSetId)"/>
    <xsl:variable name="n2" select="condition"/>
    <xsl:value-of select="$dia/diagnostic/set[@id=$n1]/localization[@lang=$lang]/code[@value=$n2]"/>
    <xsl:text>: </xsl:text>
    <xsl:value-of select="addInfo"/>
  </xsl:element>
</xsl:template>

<xsl:template name="record.sutrs">
  <pre>
    <xsl:value-of select="."/>
  </pre>
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


<xsl:template name="res.header">
  <xsl:call-template name="menu.bar"/>
  <hr/>
</xsl:template>

<xsl:template name="res.footer">
  <hr/>
  <xsl:call-template name="menu.bar"/>
</xsl:template>

<xsl:template name="menu.bar">
  <div class="menubar">
<!-- Home -->
    <xsl:text>[ </xsl:text>
    <xsl:element name="a">
      <xsl:attribute name="href">
        <xsl:value-of select="$cgi.script.URL"/><xsl:text>?form+</xsl:text>
        <xsl:value-of select="$session.id"/><xsl:text>+</xsl:text>
        <xsl:value-of select="$target"/><xsl:text>+</xsl:text>
        <xsl:value-of select="$profile"/><xsl:text>+</xsl:text>
        <xsl:value-of select="$lang"/>
        <xsl:if test="$user.id">
          <xsl:text>+</xsl:text>
          <xsl:value-of select="$user.id"/>
        </xsl:if>
      </xsl:attribute>
      <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_FORM']"/>
    </xsl:element>
    <xsl:text> ]</xsl:text>

<!-- PQ, PQS -->
<!--
    <xsl:if test="(@type='SearchResponse' or @type='PresentResponse') and $user.id and not (database='IR-Extend-1' or database=$circ.db)">
      <xsl:text> [ </xsl:text>
        <a href="{$cgi.script.URL}?ACTION=pq&amp;SESSION_ID={$session.id}&amp;DB={database}&amp;TERM={term}&amp;LANG={$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_PQ']"/></a>
      <xsl:text> ] </xsl:text>
      <xsl:text> [ </xsl:text>
        <a href="{$cgi.script.URL}?ACTION=prepqs&amp;SESSION_ID={$session.id}&amp;DB={database}&amp;TERM={term}&amp;TARGET={$target}&amp;LANG={$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_FORM_PQS']"/></a>
      <xsl:text> ] </xsl:text>
    </xsl:if>
-->
<!-- Backwards -->
    <xsl:choose>
      <xsl:when test="@type='SearchResponse' or @type='PresentResponse'">
        <xsl:if test="$start &gt; 1">

          <xsl:variable name="bkw.start">
            <xsl:choose>
              <xsl:when test="($fmt = 'F' or $fmt = 'M') and $start &gt; 1">
                <xsl:value-of select="$start - 1"/>
              </xsl:when>
              <xsl:when test="$start - $max.records &gt; 1">
                <xsl:value-of select="$start - $max.records"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="1"/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>

          <xsl:variable name="fwd.end">
            <xsl:choose>
              <xsl:when test="$bkw.start + $max.records &gt; resultCount">
                <xsl:value-of select="resultCount"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="$max.records"/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>

          <xsl:text> [ </xsl:text>
          <xsl:choose>
            <xsl:when test="$fmt = 'B'">
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+1+{$max.records}+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>|&lt;</xsl:text></a>
            </xsl:when>
            <xsl:otherwise>
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+1+1+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>|&lt;</xsl:text></a>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:text> ]</xsl:text>
          <xsl:text> [ </xsl:text>
          <xsl:choose>
            <xsl:when test="$fmt = 'B'">
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+{$bkw.start}+{$fwd.end}+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>&lt;&lt;</xsl:text></a>
            </xsl:when>
            <xsl:otherwise>
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+{$bkw.start}+1+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>&lt;&lt;</xsl:text></a>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:text> ]</xsl:text>
        </xsl:if>
      </xsl:when>
      <xsl:when test="@type='ScanResponse'">
        <xsl:variable name="attr" select="concat('[', substring-after(term, '['))"/>
        <xsl:if test="scanStatus != 6 and (scanStatus != 5 or preferredPositionInResponse != $max.records)">
          <xsl:text> [ </xsl:text>
            <xsl:choose>
              <xsl:when test="termInfo">
                <a href="{$cgi.script.URL}?ACTION=SCAN&amp;SESSION_ID={$session.id}&amp;DBNAME={database}&amp;THE_TERM={str:encode-uri(termInfo[1]/term, true())}{$attr}&amp;STEP_SIZE={$step.size}&amp;MAXRECORDS={$max.records}&amp;PREF_POS={$max.records}&amp;ATTSET={$attribute.set}&amp;RECSYNTAX={$record.syntax}&amp;LANG={$lang}"><xsl:text>&lt;&lt;</xsl:text></a>
              </xsl:when>
              <xsl:otherwise>
                <a href="{$cgi.script.URL}?ACTION=SCAN&amp;SESSION_ID={$session.id}&amp;DBNAME={database}&amp;THE_TERM={str:encode-uri(term, true())}&amp;STEP_SIZE={$step.size}&amp;MAXRECORDS={$max.records}&amp;PREF_POS={$max.records}&amp;ATTSET={$attribute.set}&amp;RECSYNTAX={$record.syntax}&amp;LANG={$lang}"><xsl:text>&lt;&lt;</xsl:text></a>
              </xsl:otherwise>
            </xsl:choose>
          <xsl:text> ]</xsl:text>
        </xsl:if>
      </xsl:when>
    </xsl:choose>

<!-- Forwards -->
    <xsl:choose>
      <xsl:when test="@type='SearchResponse' or @type='PresentResponse'">
        <xsl:if test="$start + count(record) - 1 &lt; resultCount">

          <xsl:variable name="fwd.end">
            <xsl:choose>
              <xsl:when test="$start + count(record) - 1 + $max.records &gt; resultCount">
                <xsl:value-of select="resultCount - $start - count(record) + 1"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="$max.records"/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>

          <xsl:text> [ </xsl:text>
          <xsl:choose>
            <xsl:when test="$fmt = 'B'">
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+{$start + count(record)}+{$fwd.end}+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>&gt;&gt;</xsl:text></a>
            </xsl:when>
            <xsl:otherwise>
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+{$start + count(record)}+1+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>&gt;&gt;</xsl:text></a>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:text> ]</xsl:text>
          <xsl:text> [ </xsl:text>
          <xsl:choose>
            <xsl:when test="$fmt = 'B'">
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+{resultCount - $max.records + 1}+{$max.records}+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>&gt;|</xsl:text></a>
            </xsl:when>
            <xsl:otherwise>
              <a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+{resultCount}+1+{$fmt}+{$record.syntax}+{$lang}"><xsl:text>&gt;|</xsl:text></a>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:text> ]</xsl:text>
        </xsl:if>
      </xsl:when>
      <xsl:when test="@type='ScanResponse'">
        <xsl:variable name="attr" select="concat('[', substring-after(term, '['))"/>
        <xsl:if test="scanStatus != 6 and (scanStatus != 5 or preferredPositionInResponse != 1)">
          <xsl:text> [ </xsl:text>
            <xsl:choose>
              <xsl:when test="count(termInfo) &gt; 0">
                <a href="{$cgi.script.URL}?ACTION=SCAN&amp;SESSION_ID={$session.id}&amp;DBNAME={database}&amp;THE_TERM={str:encode-uri(termInfo[count(current()/termInfo)]/term, true())}{$attr}&amp;STEP_SIZE={$step.size}&amp;MAXRECORDS={$max.records}&amp;PREF_POS=1&amp;ATTSET={$attribute.set}&amp;RECSYNTAX={$record.syntax}&amp;LANG={$lang}"><xsl:text>&gt;&gt;</xsl:text></a>
              </xsl:when>
              <xsl:otherwise>
                <a href="{$cgi.script.URL}?ACTION=SCAN&amp;SESSION_ID={$session.id}&amp;DBNAME={database}&amp;THE_TERM={str:encode-uri(term, true())}&amp;STEP_SIZE={$step.size}&amp;MAXRECORDS={$max.records}&amp;PREF_POS={$max.records}&amp;ATTSET={$attribute.set}&amp;RECSYNTAX={$record.syntax}&amp;LANG={$lang}"><xsl:text>&lt;&lt;</xsl:text></a>
              </xsl:otherwise>
            </xsl:choose>
          <xsl:text> ]</xsl:text>
        </xsl:if>
      </xsl:when>
    </xsl:choose>

<!-- Download all -->
    <xsl:if test="@type='SearchResponse' or @type='PresentResponse'">
      <xsl:if test="$marc.download and $download.all and resultCount &gt; 0">
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+1+{resultCount}+R+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_DOWNLOAD_ALL']"/></a><xsl:text> ]</xsl:text>
      </xsl:if>
    </xsl:if>

<!-- Download selected -->
    <xsl:if test="@type='SearchResponse' or @type='PresentResponse'">
      <xsl:if test="$marc.download and $download.selected and resultCount &gt; 0">
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{resultSet}+0+0+R+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_DOWNLOAD_SEL']"/></a><xsl:text> ]</xsl:text>
      </xsl:if>
    </xsl:if>

<!-- Show diagnostic -->
    <xsl:if test="@type='SearchResponse' or @type='PresentResponse'">
      <xsl:if test="$hide.diag and count(SearchResponse/record[@syntax='diagnostic']) &gt; $diag.threshold">
        <span class="show_diag"><xsl:text>[ </xsl:text><a href="javascript:showDiagnostics()"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_SHOW_DIAG']"/></a><xsl:text> ]</xsl:text></span>
      </xsl:if>
    </xsl:if>

  </div>
</xsl:template>

<xsl:template name="record.menu">
  <xsl:if test="$fmt = 'B'">
    <div class="recordmenu">
      <xsl:if test="$marc.download and $download.selected">
        <xsl:text>[ </xsl:text>
        <xsl:element name="input">
          <xsl:attribute name="type">checkbox</xsl:attribute>
          <xsl:attribute name="name">sel</xsl:attribute>
          <xsl:attribute name="id"><xsl:value-of select="$start + position() - 1"/></xsl:attribute>
          <xsl:attribute name="onchange">selectRecord(this)</xsl:attribute>
        </xsl:element>
        <xsl:text> ]</xsl:text>
      </xsl:if>
      <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{../resultSet}+{$start + position() - 1}+1+F+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_FULL']"/></a><xsl:text> ]</xsl:text>
    </div>
  </xsl:if>
  <xsl:if test="$fmt = 'F'">
    <div class="recordmenu">
      <xsl:if test="@syntax='1.2.840.10003.5.1' or @syntax='Unimarc' or
			@syntax='1.2.840.10003.5.10' or @syntax='USmarc' or
			@syntax='1.2.840.10003.5.28' or @syntax='RUSmarc'">

<!-- MARC TAGS -->
        <xsl:if test="$marc.labels">
          <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{../resultSet}+{$start + position() - 1}+1+M+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_TAG']"/></a><xsl:text> ] </xsl:text>
        </xsl:if>

<!-- DOWNLOAD -->
        <xsl:if test="$marc.download">
          <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{../resultSet}+{$start + position() - 1}+1+R+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_DOWNLOAD']"/></a><xsl:text> ] </xsl:text>
        </xsl:if>
      </xsl:if>

<!-- ORDER -->
      <xsl:if test="$item.order and string-length($user.id) &gt; 0 and @syntax !='1.2.840.10003.5.106' and @syntax !='Extended' and @syntax !='1.2.840.10003.5.109.10'">
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?preorder+{$session.id}+1+{../resultSet}+{$start + position() - 1}+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_PREORDER']"/></a><xsl:text> ] </xsl:text>
      </xsl:if>

<!-- LINK TO AUTHORITY RECORD -->
      <xsl:variable name="rid">
        <xsl:choose>
          <xsl:when test="@syntax='1.2.840.10003.5.102' or @syntax='OPAC'">
            <xsl:value-of select="bibliographicRecord/record/field[@id='700']/subfield[@id='3']"/>
          </xsl:when>
          <xsl:when test="@syntax='1.2.840.10003.5.1' or @syntax='Unimarc' or
		@syntax='1.2.840.10003.5.28' or @syntax='RUSmarc'">
            <xsl:value-of select="field[@id='700']/subfield[@id='3']"/>
          </xsl:when>
        </xsl:choose>
      </xsl:variable>

      <xsl:if test="string-length($rid) &gt; 0 and $author.link">
        <xsl:variable name="link">
         <xsl:for-each select="$ia/map/mapping">
             <xsl:if test="starts-with($rid, id)">
              <xsl:value-of select="zurl"/>
            </xsl:if>
          </xsl:for-each>
        </xsl:variable>
        <xsl:if test="string-length($link) &gt; 0">
          <xsl:text>[ </xsl:text><a href="{$ZURL.resolver}?{substring-before($link, '?')}?{$rid};{substring-after($link, '?')};lang={$lang}" target="_blank"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_AA']"/></a><xsl:text> ] </xsl:text>
        </xsl:if>
      </xsl:if>

<!-- RELATED RECORDS -->
      <xsl:if test="$link.to.related and (@syntax='1.2.840.10003.5.1' or @syntax='Unimarc' or
			@syntax='1.2.840.10003.5.28' or @syntax='RUSmarc' or
			(@syntax='1.2.840.10003.5.102' or @syntax='OPAC') and
			bibliographicRecord/record[@syntax='1.2.840.10003.5.28' or @syntax='RUSmarc' or
			@syntax='1.2.840.10003.5.1' or @syntax='Unimarc'])">
        <xsl:choose>
          <xsl:when test="//leader/leader08='1'">
            <xsl:choose>
              <xsl:when test="//leader/leader07='s'">
                <!-- Generic serial -->
                <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?ACTION=FOLLOW&amp;SESSION_ID={$session.id}&amp;LANG={$lang}&amp;TERM=AND(AND(2[1,1045],s[1,1021]),{str:encode-uri(//field[@id='001'], true())}{$link.attrs}))"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_NV']"/></a><xsl:text> ] </xsl:text>
              </xsl:when>
              <xsl:when test="//leader/leader07='m'">
                <!-- Generic monograph -->
                <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?ACTION=FOLLOW&amp;SESSION_ID={$session.id}&amp;LANG={$lang}&amp;TERM=AND(AND(2[1,1045],m[1,1021]),{str:encode-uri(//field[@id='001'], true())}{$link.attrs}))"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_NV']"/></a><xsl:text> ] </xsl:text>
              </xsl:when>
            </xsl:choose>
            <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?ACTION=FOLLOW&amp;SESSION_ID={$session.id}&amp;LANG={$lang}&amp;TERM=AND(OR(a[1,1021],b[1,1021]),{str:encode-uri(//field[@id='001'], true())}{$link.attrs})"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_ART']"/></a><xsl:text> ] </xsl:text>
          </xsl:when>
          <xsl:when test="//leader/leader08='2' and (//leader/leader07='s' or //leader/leader07='m')">
            <!-- Specific serial or monograph -->
            <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?ACTION=FOLLOW&amp;SESSION_ID={$session.id}&amp;LANG={$lang}&amp;TERM=AND(OR(a[1,1021],b[1,1021]),{str:encode-uri(//field[@id='001'], true())}{$link.attrs})"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_ART']"/></a><xsl:text> ] </xsl:text>
          </xsl:when>
        </xsl:choose>
      </xsl:if>
<!-- TASK PACKAGE -->
      <xsl:if test="(@syntax='1.2.840.10003.5.106' or @syntax='1.2.840.10003.5.109.10') and eSTaskPackage/packageType='1.2.840.10003.9.1'">
<!-- Implement TP deletion first at server
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?ACTION=DELETE&amp;SESSION_ID={$session.id}&amp;LANG={$lang}&amp;TP_TYPE=1.2.840.10003.9.{eSTaskPackage/packageType}&amp;TP_NAME={str:encode-uri(eSTaskPackage/packageName, true())}&amp;USER_ID={$user.id}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_DELETE']"/></a><xsl:text> ] </xsl:text>
-->
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?ACTION=SEARCH&amp;SESSION_ID={$session.id}&amp;LANG={$lang}&amp;DBNAME={str:encode-uri(eSTaskPackage/taskSpecificParameters/taskPackage/originPart/databaseNames/database, true())}&amp;TERM_1={str:encode-uri(eSTaskPackage/taskSpecificParameters/taskPackage/targetPart/query, true())}&amp;ESNAME=B&amp;MAXRECORDS={$max.records}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_INVOKE']"/></a><xsl:text> ] </xsl:text>
      </xsl:if>
    </div>
  </xsl:if>
  <xsl:if test="$fmt='M'">
    <xsl:if test="@syntax='1.2.840.10003.5.1' or @syntax='Unimarc' or
			@syntax='1.2.840.10003.5.10' or @syntax='USmarc' or
			@syntax='1.2.840.10003.5.28' or @syntax='RUSmarc'">
      <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{../resultSet}+{$start + position() - 1}+1+F+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_NOR']"/></a><xsl:text> ]</xsl:text>
      <xsl:text> </xsl:text>
      <xsl:if test="$marc.download">
        <xsl:text>[ </xsl:text><a href="{$cgi.script.URL}?present+{$session.id}+{../resultSet}+{$start + position() - 1}+1+R+{$record.syntax}+{$lang}"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_REC_DOWNLOAD']"/></a><xsl:text> ]</xsl:text>
      </xsl:if>
    </xsl:if>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
