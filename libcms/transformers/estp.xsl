<?xml version="1.0" encoding="utf-8"?>
<!--
 * $Log: estp.xsl,v $
 * Revision 1.5  2010/12/18 16:29:58  rustam
 * Persistent query
 *
 * Revision 1.4  2009/12/23 09:23:10  rustam
 * Actual query representation
 *
 * Revision 1.3  2009/12/08 14:12:25  rustam
 * PQS TP representation
 *
 * Revision 1.2  2003/05/06 10:47:13  rustam
 * Added statusOrErrorReport representation
 *
 * Revision 1.1  2003/01/31 14:11:29  rustam
 * New pre-release
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

<xsl:template name="record.estp">
  <table class="order">
    <xsl:apply-templates/>
  </table>
</xsl:template>

<xsl:template match="packageType">
</xsl:template>

<xsl:template match="packageName">
</xsl:template>

<xsl:template match="userId">
  <tr>
  <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_USERID']"/></td>
  <td class="data"><xsl:value-of select="."/></td>
  </tr>
</xsl:template>

<xsl:template match="retentionTime">
</xsl:template>

<xsl:template match="permissions">
</xsl:template>

<xsl:template match="description">
  <tr>
  <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DESCR']"/></td>
  <td class="data"><xsl:value-of select="."/></td>
  </tr>
</xsl:template>

<xsl:template match="targetReference">
  <tr>
  <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_NUM']"/></td>
  <td class="data"><xsl:value-of select="."/></td>
  </tr>
</xsl:template>

<xsl:template match="creationDateTime">
  <tr>
  <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_DAT']"/></td>
  <td class="data">
    <xsl:variable name="date" select="substring(.,1,8)"/>
    <xsl:variable name="time" select="substring(.,9,6)"/>
    <xsl:value-of select="substring($date,7,2)"/><xsl:text>.</xsl:text>
    <xsl:value-of select="substring($date,5,2)"/><xsl:text>.</xsl:text>
    <xsl:value-of select="substring($date,1,4)"/><xsl:text> </xsl:text>
    <xsl:value-of select="substring($time,1,2)"/><xsl:text>:</xsl:text>
    <xsl:value-of select="substring($time,3,2)"/><xsl:text>:</xsl:text>
    <xsl:value-of select="substring($time,5,2)"/>
  </td>
  </tr>
</xsl:template>

<xsl:template match="taskStatus">
  <tr>
  <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_ST']"/></td>
  <td class="data"><xsl:value-of select="$msg/messages/localization[@language=$lang]/estp[@id=current()]"/></td>
  </tr>
</xsl:template>

<xsl:template match="packageDiagnostics">
  <tr>
  <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_DIAG']"/></td>
  <td><xsl:call-template name="record.selector" select="package/record"/></td>
  </tr>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/targetPart/statusOrErrorReport">
  <xsl:if test="$fmt='F'">
    <tr>
    <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_SE']"/></td>
    <td class="data"><xsl:value-of select="."/></td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/targetPart/itemRequest/record">
  <xsl:if test="$fmt='F'">
    <tr>
    <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_ORDER_ITM']"/></td>
    <td class="data"><xsl:call-template name="record.selector"/></td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/originPart/activeFlag">
  <xsl:if test=". = 0">
    <tr>
    <td class="label"></td>
    <td class="data"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_ACTIVE_FLAG']"/></td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/originPart/databaseNames">
  <xsl:if test="$fmt='F'">
    <tr>
    <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DB']"/></td>
    <td class="data">
       <xsl:for-each select="database">
         <xsl:if test="position() != 1">
           <xsl:text>, </xsl:text>
         </xsl:if>
         <xsl:value-of select="."/>
       </xsl:for-each>
    </td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/targetPart/actualQuery | taskSpecificParameters/taskPackage/targetPart/query">
  <xsl:if test="$fmt='F'">
    <tr>
    <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_QUERY']"/></td>
    <td class="data"><xsl:value-of select="."/></td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/targetPart/targetStatedPeriod">
  <xsl:if test="$fmt='F'">
    <tr>
    <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_PERIOD']"/></td>
    <td class="data">
      <xsl:choose>
        <xsl:when test=". = 86400">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/period[@id='DAILY']"/>
        </xsl:when>
        <xsl:when test=". = 604800">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/period[@id='WEEKLY']"/>
        </xsl:when>
        <xsl:when test=". = 2592000">
          <xsl:value-of select="$msg/messages/localization[@language=$lang]/period[@id='MONTHLY']"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
    </td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="taskSpecificParameters/taskPackage/originPart/alertDestination">
  <xsl:if test="$fmt='F'">
    <tr>
    <td class="label"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='LBL_DEST']"/></td>
    <td class="data"><xsl:value-of select="."/></td>
    </tr>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
