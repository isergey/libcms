<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output indent="yes" encoding="UTF-8" standalone="no"/>
  <!-- Parameters -->
  <xsl:variable name="ARLICON_LABEL" select="'АРБИКОН'"/>
  <xsl:variable name="LANGUAGE_LABEL" select="'rus'"/>
  <xsl:variable name="stylesheet.FORM" select="'/inc/css/form.css'"/>
  <xsl:variable name="stylesheet.COLOURS" select="'/inc/css/colours.css'"/>
  <xsl:variable name="stylesheet.FORMEXT" select="'/inc/css/formext.css'"/>
  <xsl:variable name="javascript.COOKIE" select="'/inc/javascript/jscookie.js'"/>
  <xsl:variable name="javascript.JSUTILS" select="'/inc/javascript/jscssutils.js'"/>
  <xsl:variable name="javascript.JSFORMEXT" select="'/inc/javascript/jsformext.js'"/>  

 <xsl:variable name="filestree">
    <xsl:copy-of select="document('files.xml')"/>  
  </xsl:variable>
  
  <xsl:variable name="filesset" select="exslt:node-set($filestree)" xmlns:exslt="http://exslt.org/common"/>
  
  <xsl:variable name="expltree">
    <xsl:for-each select="$filesset/documents/file">
      <xsl:copy-of select="document(string(.))/explain"/>
    </xsl:for-each>
  </xsl:variable>
  <xsl:variable name="explset" select="exslt:node-set($expltree)" xmlns:exslt="http://exslt.org/common"/>

  <xsl:variable name="servtree">
    <servers>
      <xsl:for-each select="($explset)/explain[databaseInfo/subjects/subject = $ARLICON_LABEL]">
        <xsl:sort select="databaseInfo/subjects[1]"/>    
        <server>
          <zurl>z39.50s://<xsl:value-of select="serverInfo/host"/>:<xsl:value-of select="serverInfo/port"/>/<xsl:value-of select="translate(string(serverInfo/database), ',', '+')"/><xsl:if test="configInfo/setting[@type = 'charset']">?cs=<xsl:value-of select="configInfo/setting[@type = 'charset']"/></xsl:if>
          </zurl>
          <title><xsl:value-of select="translate(string(databaseInfo/title[@lang=$LANGUAGE_LABEL]), '&#x22;', '&#xb4;')"/></title>
          <xsl:choose>
            <xsl:when test="count(databaseInfo/author[@lang=$LANGUAGE_LABEL]) = 0">
              <label><xsl:value-of select="translate(string(databaseInfo/subjects/subject[1]), '&#x22;', '&#xb4;')"/> - <xsl:value-of select="translate(string(databaseInfo/title[@lang=$LANGUAGE_LABEL]), '&#x22;', '&#xb4;')"/></label>
            </xsl:when>
            <xsl:otherwise>
              <label><xsl:value-of select="translate(string(databaseInfo/author[@lang=$LANGUAGE_LABEL]), '&#x22;', '&#xb4;')"/></label>
            </xsl:otherwise>
          </xsl:choose>
          <consortium><xsl:value-of select="translate(string(databaseInfo/subjects/subject[1]), '&#x22;', '&#xb4;')"/></consortium>
          <connection>
            <xsl:copy-of select="serverInfo"/>
            <xsl:copy-of select="configInfo"/>
          </connection>
        </server>
      </xsl:for-each>
    </servers>
  </xsl:variable>
  <xsl:variable name="servset" select="exslt:node-set($servtree)" xmlns:exslt="http://exslt.org/common"/>
  
  <xsl:variable name="constree">
    <consortiums>
      <xsl:for-each select="($servset)/servers/server">
        <xsl:choose>
          <xsl:when test="preceding-sibling::server[consortium = current()/consortium]"/>
          <xsl:otherwise>
            <consortium>
              <xsl:attribute name="label"><xsl:value-of select="consortium"/></xsl:attribute>
              <xsl:copy-of select="self::node() | following-sibling::server[consortium = current()/consortium]"/>
            </consortium>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>      
    </consortiums>
  </xsl:variable>
  
  <xsl:variable name="consset" select="exslt:node-set($constree)" xmlns:exslt="http://exslt.org/common"/>
  
  <xsl:variable name="adoptedconstree">
    <target>
      <xsl:for-each select="($consset)/consortiums/consortium">
        <explain>
          <serverInfo>
            <host>olsc3.unilib.neva.ru</host>
            <port>210</port>
            <database>
              <xsl:for-each select="server">
                <xsl:choose>
                  <xsl:when test="preceding-sibling::server[string(connection/serverInfo/host)=string(current()/connection/serverInfo/host)][string(connection/serverInfo/port)=string(current()/connection/serverInfo/port)]"/>
                  <xsl:otherwise>
                    <xsl:if test="position() > 1">,</xsl:if>z39.50s://<xsl:value-of select="connection/serverInfo/host"/>:<xsl:value-of select="connection/serverInfo/port"/>/<xsl:apply-templates select="self::node() | following-sibling::server[string(connection/serverInfo/host)=string(current()/connection/serverInfo/host)][string(connection/serverInfo/port)=string(current()/connection/serverInfo/port)]"/><xsl:if test="connection/configInfo/setting[@type = 'charset']">?cs=<xsl:value-of select="connection/configInfo/setting[@type = 'charset']"/></xsl:if>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:for-each>
            </database>
          </serverInfo>
          <databaseInfo>
            <title primary="true" lang="{$LANGUAGE_LABEL}">
              <xsl:value-of select="@label"/> (<xsl:value-of select="count(server)"/>)
            </title>
          </databaseInfo>
          <membersInfo>
            <xsl:copy-of select="server"/>
          </membersInfo>
          <indexInfo>
            <index search="true">
              <map primary="true">
                <attr type="1">4</attr>
                <attr type="4">1</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">4</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">4</attr>
                <attr type="4">6</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">7</attr>
                <attr type="4">1</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">8</attr>
                <attr type="4">1</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">12</attr>
                <attr type="4">1</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">21</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">31</attr>
                <attr type="4">4</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">54</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">59</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1001</attr>
                <attr type="4">108</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1003</attr>
                <attr type="4">101</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1007</attr>
                <attr type="4">1</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1011</attr>
                <attr type="4">5</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1016</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1018</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1019</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1021</attr>
                <attr type="4">108</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1032</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1034</attr>
                <attr type="4">108</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1035</attr>
                <attr type="4">2</attr>
              </map>
            </index>
            <index search="true">
              <map primary="true">
                <attr type="1">1044</attr>
                <attr type="4">2</attr>
              </map>
            </index>
          </indexInfo>
          <recordInfo>
            <recordSyntax name="RUSMARC" oid="1.2.840.10003.5.28">
              <elementSet name="B"></elementSet>
              <elementSet name="F"></elementSet>
            </recordSyntax>
          </recordInfo>          
          <configInfo>
            <setting type="title" lang="eng">Russian Library Consortia Resources</setting>
            <setting type="title" lang="rus">Ресурсы российских корпоративных библиотечных систем</setting>
            <setting type="query.expansion">false</setting>
            <supports type="option">resourceCtrl</supports>
          </configInfo>
        </explain>        
      </xsl:for-each>
    </target>
  </xsl:variable>
  <xsl:variable name="adoptedconsset" select="exslt:node-set($adoptedconstree)" xmlns:exslt="http://exslt.org/common"/>
  
  <xsl:template match="server">
    <xsl:value-of select="translate(string(connection/serverInfo/database), ',', '+')"/>
    <xsl:if test="position()!=last()">+</xsl:if>
  </xsl:template>

  <!-- xsl:template match="documents">
    <xsl:copy-of select="$adoptedconsset"/>
  </xsl:template -->
  
  <xsl:template match="target">
    <xsl:apply-templates select="$adoptedconsset" mode="FORM_MODE"/>    
  </xsl:template>
</xsl:stylesheet>  