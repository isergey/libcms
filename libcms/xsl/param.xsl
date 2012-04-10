<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: param.xsl,v $
 * Revision 1.30  2011/06/14 12:58:43  rustam
 * Minor changes
 *
 * Revision 1.29  2011/04/28 05:30:54  rustam
 * Conditional translation with PVM
 *
 * Revision 1.28  2010/12/17 14:32:25  rustam
 * interface redesign
 *
 * Revision 1.27  2010/11/03 10:58:44  rustam
 * Javascript record postprocessing
 * Linking from organisation ID
 *
 * Revision 1.26  2010/05/06 16:53:34  rustam
 * Tatar translation
 *
 * Revision 1.25  2008/09/25 12:53:56  rustam
 * Implemented bibliographic record's header linking
 *
 * Revision 1.24  2008/05/27 11:34:43  rustam
 * Linking attributes are parameterized
 *
 * Revision 1.23  2006/03/17 08:11:48  rustam
 * Implemented selection of circulation desks during preorder phase
 *
 * Revision 1.22  2006/03/06 13:09:42  rustam
 * Added some new parameters - onload and extra.*
 *
 * Revision 1.21  2005/09/07 11:38:47  rustam
 * Implemented order restrictions
 *
 * Revision 1.20  2005/08/25 07:52:21  rustam
 * Minor changes
 *
 * Revision 1.19  2005/06/23 17:27:07  rustam
 * Implemented processing of terms
 *
 * Revision 1.18  2005/04/27 05:45:50  rustam
 * Added PDA support
 *
 * Revision 1.17  2005/02/28 10:11:21  rustam
 * Added new parameter
 *
 * Revision 1.16  2004/11/04 14:56:32  rustam
 * Implemented query filter
 *
 * Revision 1.15  2004/09/23 07:22:45  rustam
 * Added virtual keyboard
 *
 * Revision 1.14  2004/06/22 10:54:36  rustam
 * Implemented logos in form
 *
 * Revision 1.13  2004/05/21 09:21:56  rustam
 * Implemented linking to authority records
 *
 * Revision 1.12  2004/05/18 10:12:22  rustam
 * Errors corrected
 *
 * Revision 1.11  2004/02/26 08:18:53  rustam
 * Can hide record warnings (bib. level) now
 *
 * Revision 1.10  2003/11/12 19:41:13  rustam
 * Downloading of selected records
 *
 * Revision 1.9  2003/10/20 08:26:56  rustam
 * Minor changes
 *
 * Revision 1.8  2003/10/20 07:33:56  rustam
 * Minor changes
 *
 * Revision 1.7  2003/09/30 11:27:15  rustam
 * Implemented resource control
 *
 * Revision 1.6  2003/09/16 07:27:20  rustam
 * Added parameter item.order
 *
 * Revision 1.5  2003/09/02 09:08:45  rustam
 * Implemented record syntax selection simplification
 *
 * Revision 1.4  2003/05/15 10:40:55  rustam
 * Minor changes
 *
 * Revision 1.3  2003/05/15 07:27:37  rustam
 * Implemented profiles
 *
 * Revision 1.2  2003/03/27 10:58:26  rustam
 * Added support for external selector dialog
 *
 * Revision 1.1  2003/01/31 14:11:50  rustam
 * New pre-release
 *
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 

<!-- Common parameters -->
<xsl:param name="lang" select="'rus'"/>
<xsl:param name="charset" select="'UTF-8'"/>
<xsl:param name="session.id" select="''"/>
<xsl:param name="target" select="''"/>
<xsl:param name="cgi.script.URL" select="'zgate'"/>
<xsl:param name="stylesheet.URL" select="'/ss/zgate.css'"/>
<xsl:param name="ZURL.resolver" select="'zurlhtml'"/>
<xsl:param name="attribute.set" select="'1.2.840.10003.3.1'"/>
<!--<xsl:param name="ad" select="document('attr.xml')"/>-->

<!-- Form creation parameters 
<xsl:param name="msg.form" select="document('form_msg.xml')"/>
<xsl:param name="ed" select="document('expand.xml')"/>
<xsl:param name="ld" select="document('lang.xml')"/>
<xsl:param name="md" select="document('materials.xml')"/>
<xsl:param name="help.URL" select="'/help.html'"/>
<xsl:param name="java.script.URL" select="'/js/zgate.js'"/>
<xsl:param name="include.help" select="true()"/>
<xsl:param name="include.profiles" select="true()"/>
<xsl:param name="include.ext.form" select="false()"/>
<xsl:param name="include.materials.list" select="true()"/>
<xsl:param name="include.languages.list" select="true()"/>
<xsl:param name="include.recsyn.list" select="false()"/>
<xsl:param name="include.relation.attrs" select="false()"/>
<xsl:param name="include.structure.attrs" select="true()"/>
<xsl:param name="dedup" select="true()"/>
<xsl:param name="sort" select="true()"/>
<xsl:param name="query.expansion" select="true()"/>
<xsl:param name="include.dialog" select="false()"/>
<xsl:param name="include.virtual.kbd" select="false()"/>
<xsl:param name="simplify.recsyn.list" select="false()"/>
<xsl:param name="term.size" select="'25'"/>
<xsl:param name="term.size.max" select="'100'"/>
<xsl:param name="num.records" select="'20'"/>
<xsl:param name="num.records.size" select="'5'"/>
<xsl:param name="list.size" select="'4'"/>
<xsl:param name="element.set.name" select="'B'"/>
<xsl:param name="logo.left.URL" select="''"/>
<xsl:param name="logo.right.URL" select="''"/>
<xsl:param name="query.filter" select="''"/>
<xsl:param name="term.1" select="''"/>
<xsl:param name="term.2" select="''"/>
<xsl:param name="term.3" select="''"/>
<xsl:param name="use.1" select="''"/>
<xsl:param name="use.2" select="''"/>
<xsl:param name="use.3" select="''"/>
<xsl:param name="pda.mode" select="false()"/>
<xsl:param name="onload" select="''"/>
<xsl:param name="extra.template" select="false()"/>
<xsl:param name="extra.header" select="''"/>
<xsl:param name="extra.js" select="''"/>-->
<xsl:param name="circ.db" select="'circ'"/>


<!-- Workflow and record representation parameters -->
<xsl:param name="fmt" select="'F'"/>
<xsl:param name="result.set.name" select="'default'"/>
<xsl:param name="start" select="1"/>
<xsl:param name="scan.to.form" select="false()"/>
<xsl:param name="hide.diag" select="true()"/>
<xsl:param name="hide.record.warnings" select="true()"/>
<xsl:param name="diag.threshold" select="2"/>
<xsl:param name="max.records" select="10"/>
<xsl:param name="step.size" select="0"/>
<xsl:param name="record.syntax" select="'!'"/>
<xsl:param name="ht" select="true()"/>
<xsl:param name="abstract" select="true()"/>
<xsl:param name="subject" select="false()"/>
<xsl:param name="class" select="true()"/>
<xsl:param name="record.source" select="false()"/>
<xsl:param name="holdings" select="false()"/>
<xsl:param name="marc.labels" select="false()"/>
<xsl:param name="marc.download" select="false()"/>
<xsl:param name="download.all" select="false()"/>
<xsl:param name="download.selected" select="false()"/>
<xsl:param name="follow.subject" select="true()"/>
<xsl:param name="follow.header" select="true()"/>
<xsl:param name="follow.attrs" select="'[1,12]'"/>
<xsl:param name="personal.author.attrs" select="'[1,1004,4,101]'"/>
<xsl:param name="corporate.author.attrs" select="'[1,1005,4,101]'"/>
<xsl:param name="link.to.related" select="true()"/>
<xsl:param name="link.attrs" select="'[1,1049]'"/>
<xsl:param name="resource.reports" select="false()"/>
<xsl:param name="report" select="'report.html'"/>
<xsl:param name="item.order" select="true()"/>
<xsl:param name="author.link" select="true()"/>
<xsl:param name="schemaId" select="''"/>
<xsl:param name="user.id" select="''"/>
<xsl:param name="profile" select="'simple.xsl'"/>
<xsl:param name="msg" select="document('zgate_msg.xml')"/>
<xsl:param name="org" select="document('zgate_org.xml')"/>
<!--<xsl:param name="dia" select="document('diag.xml')"/>
 <xsl:param name="units" select="document('zgate_units.xml')"/>
<xsl:param name="country" select="document('zgate_countries.xml')"/>
<xsl:param name="ia" select="document('zgate_id2addr.xml')"/>-->
<xsl:param name="order.restriction" select="'Электронный заказ на книговыдачу невозможен'"/>
<!--<xsl:param name="circ.desk" select="document('circ_desk.xml')"/>-->
<xsl:param name="check.records" select="'checkRecords();'"/>
<xsl:param name="org.link.URL" select="'http://arbicon.ru/ajax/getOrgFullInfo.php?code='"/>
<xsl:param name="cover" select="'Обложка'"/>
<xsl:param name="opac.holdings.reconstruction" select="true()"/>
</xsl:stylesheet>
