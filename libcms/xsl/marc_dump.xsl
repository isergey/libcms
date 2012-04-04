<?xml version="1.0" encoding="UTF-8"?>
<!--
 Представление записи при выводе в результате поиска
 Структура результирующего документа должна быть следующей:
<doc>
    <field name='field_name_1'>
        <item>Содержимое поля 1 </item>
        <item>Содержимое поля 2 </item>
    </field>
    <field name='field_name_2'>
        <item>Содержимое поля 1 </item>
        <item>Содержимое поля 2 </item>
    </field>
</doc>

Для того, чтобы можно было искать по полю, необходимо задавать ему имя соответвующей точке доступа
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml"/>

    <!--<xsl:template match="/">
        <add>
            <xsl:for-each select="record">
                <xsl:apply-templates select="record"/>
            </xsl:for-each>
        </add>
    </xsl:template>-->


    <xsl:output indent="yes" method="xml" version="1.0" encoding="UTF-8"/>

    <!-- disable all default text node output -->
    <xsl:template match="text()"/>

    <xsl:template match="/">
        <xsl:if test="record">
            <xsl:variable name="leader7" select="leader/leader07"/>

            <xsl:apply-templates select="record"/>
        </xsl:if>
    </xsl:template>

    <!-- match on marcxml record -->
    <xsl:template match="record">
        <div class="marc_dump">
            <xsl:call-template name="dump"/>
        </div>
    </xsl:template>

    <xsl:template name="dump">
        <xsl:param name="r"/>
        <xsl:param name="break" select="true()"/>
        <xsl:variable name="stx" select="@syntax"/>

        <span class="data"><xsl:for-each select="leader/*">
            <xsl:value-of select="translate(., ' ', '#')"/>
        </xsl:for-each> </span><br/>
        <xsl:for-each select="field">
            <xsl:variable name="label" select="@id"/>
            <span class="fieldlabel"><xsl:value-of select="$label"/> </span>
            <xsl:choose>
                <xsl:when test="indicator">
                    <xsl:variable name="i1" select="indicator[@id='1']"/>
                    <xsl:variable name="i2" select="indicator[@id='2']"/>
        <span class="indicator">
          <xsl:value-of select="translate($i1, ' ', '#')"/>
          <xsl:value-of select="translate($i2, ' ', '#')"/>
        </span>
                    <xsl:for-each select="subfield">
                        <span class="subfieldlabel"><xsl:text>$</xsl:text><xsl:value-of select="@id"/> </span>
                        <xsl:choose>
                            <xsl:when test="field">
                                <xsl:call-template name="dump">
                                    <xsl:with-param name="r" select="field"/>
                                    <xsl:with-param name="break" select="false()"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:variable name="data" select="."/>
              <span class="data">
              <xsl:choose>
                  <xsl:when test="substring($label, 1, 1)='1' and
($stx='1.2.840.10003.5.1' or $stx='Unimarc' or $stx='1.2.840.10003.5.28' or $stx='RUSmarc')">
                      <xsl:value-of select="translate($data, ' ', '#')"/>
                  </xsl:when>
                  <xsl:otherwise>
                      <xsl:value-of select="$data"/>
                  </xsl:otherwise>
              </xsl:choose>
              </span>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <span class="data"><xsl:value-of select="."/> </span>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="$break">
                <br/>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>



