<?xml version="1.0"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt" xmlns:usr="urn:the-xml-files:xslt" version="1.0">
  <xsl:output method="html" encoding="utf-8" indent="yes" />

  <!-- Код вида отчета -->
  <xsl:param name="baseURL" select="'/'" />
  <xsl:param name="view" select="'modern'" />

  <xsl:template match="/"><xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html>
</xsl:text>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>
          <xsl:value-of select="/Reports/Summary/Title"/>
        </title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet">
          <xsl:attribute name="href">
            <xsl:value-of select="$baseURL"/>
            <xsl:text>css/bootstrap.min.css</xsl:text>
          </xsl:attribute>
        </link>
        <!-- Optional theme -->
        <link rel="stylesheet">
          <xsl:attribute name="href">
            <xsl:value-of select="$baseURL"/>
            <xsl:text>css/bootstrap-theme.min.css</xsl:text>
          </xsl:attribute>
        </link>
        <!-- -->
        <link rel="stylesheet">
          <xsl:attribute name="href">
            <xsl:value-of select="$baseURL"/>
            <xsl:text>css/report-modern.css</xsl:text>
          </xsl:attribute>
        </link>
        <!-- jQuery -->
        <script type="text/javascript">
          <xsl:attribute name="src">
            <xsl:value-of select="$baseURL"/>
            <xsl:text>js/jquery-1.11.2.min.js</xsl:text>
          </xsl:attribute>
        </script>
        <!-- -->
        <script type="text/javascript">
          <xsl:attribute name="src">
            <xsl:value-of select="$baseURL"/>
            <xsl:text>js/report-modern.js</xsl:text>
          </xsl:attribute>
        </script>
      </head>
      <body>
        <!--<div class="stat-parameters">
          <xsl:call-template name="PrintParameters" />
        </div>-->
        <div class="stat-main">
          <xsl:apply-templates select="Reports/Report" />
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Report">

    <xsl:call-template name="PrintTitle" />

    <xsl:call-template name="PrintMultiLevelParameters"/>
    <div class="stat-data">
      <xsl:if test="TableHeader[@Type='Vertical']/@MaxLevel > 1">
        <xsl:call-template name="PrintLevelControls">
          <xsl:with-param name="MaxLevel" select="TableHeader[@Type='Vertical']/@MaxLevel"/>
        </xsl:call-template>
      </xsl:if>
      <table class="table table-striped table-bordered stat-main-table">
        <thead>
          <xsl:call-template name="PrintHeader" />
        </thead>
        <tbody>
          <xsl:call-template name="PrintBody" />
        </tbody>
      </table>
    </div>

    <xsl:if test="position()!=last()">
      <hr class="stat-nextreport"/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="PrintTitle">

    <h1>
      <xsl:value-of select="/Reports/Summary/Title"/>
    </h1>
    <xsl:if test="/Reports/Summary/Subtitle">
      <div class="stat-subtitle">
        <xsl:value-of select="/Reports/Summary/Subtitle"/>
      </div>
    </xsl:if>
    <p />

    <xsl:if test="count(Parameters/Parameter)>=1">
      <table class="table table-striped table-bordered stat-parameters-table">
        <xsl:for-each select="Parameters/Parameter">
          <xsl:call-template name="PrintTitle_Parameter">
            <xsl:with-param name="DimensionCode" select="@DimensionCode"/>
            <xsl:with-param name="SelectedElement" select="@SelectedElement"/>
            <xsl:with-param name="MultiLevel" select="@MultiLevel"/>
          </xsl:call-template>
        </xsl:for-each>
      </table>
    </xsl:if>
  </xsl:template>

  <xsl:template name="PrintLevelControls">
    <xsl:param name="MaxLevel"/>
    <div class="btn-group stat-levels-panel" role="group" aria-label="Уровни">
      <xsl:call-template name="PrintLevelControl">
        <xsl:with-param name="Level" select="1"/>
      </xsl:call-template>
      <xsl:call-template name="PrintLevelControl">
        <xsl:with-param name="Level" select="2"/>
      </xsl:call-template>
      <xsl:if test="$MaxLevel > 2">
        <xsl:call-template name="PrintLevelControl">
          <xsl:with-param name="Level" select="3"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:if test="$MaxLevel > 3">
        <xsl:call-template name="PrintLevelControl">
          <xsl:with-param name="Level" select="4"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:if test="$MaxLevel > 4">
        <xsl:call-template name="PrintLevelControl">
          <xsl:with-param name="Level" select="5"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:if test="$MaxLevel > 5">
        <xsl:call-template name="PrintLevelControl">
          <xsl:with-param name="Level" select="6"/>
        </xsl:call-template>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template name="PrintLevelControl">
    <xsl:param name="Level"/>
    <button type="button" class="btn btn-default stat-level-control">
      <xsl:attribute name="value">
        <xsl:value-of select="$Level"/>
      </xsl:attribute>
      <xsl:value-of select="$Level"/>
    </button>
  </xsl:template>

  <xsl:template name="PrintTitle_Parameter">
    <xsl:param name="DimensionCode"/>
    <xsl:param name="SelectedElement"/>
    <xsl:param name="MultiLevel"/>

    <tr>
      <th>
        <xsl:value-of select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/@Name"/>
      </th>
      <td>
        <xsl:choose>
          <xsl:when test="@AllowChange and $MultiLevel!='true'">
              <select class="stat-parameters-select">
                <xsl:for-each select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/Element[@ReportUrl]">
                  <option>
                    <xsl:if test="@Code=$SelectedElement">
                      <xsl:attribute name="selected">selected</xsl:attribute>
                    </xsl:if>
                    <xsl:attribute name="value">
                      <xsl:call-template name="string-replace-all">
                        <xsl:with-param name="text" select="@ReportUrl"/>
                        <xsl:with-param name="replace" select="'%7bview%7d'"/>
                        <xsl:with-param name="by" select="$view"/>
                      </xsl:call-template>
                    </xsl:attribute>
                    <xsl:call-template name="PrintName">
                      <xsl:with-param name="DimensionCode" select="$DimensionCode"/>
                      <xsl:with-param name="ElementCode" select="@Code"/>
                    </xsl:call-template>
                  </option>
                </xsl:for-each>
              </select>
          </xsl:when>
          <xsl:otherwise>
            <div class="stat-parameter-value">
              <xsl:call-template name="PrintFullName">
                <xsl:with-param name="DimensionCode" select="$DimensionCode"/>
                <xsl:with-param name="ElementCode" select="@SelectedElement"/>
              </xsl:call-template>
            </div>
            <xsl:if test="@AllowChange">
              <button type="button" class="btn btn-default stat-parameter-change">
                <xsl:attribute name="data-dimension">
                  <xsl:value-of select="$DimensionCode"/>
                </xsl:attribute>
                <xsl:text>...</xsl:text>
              </button>
            </xsl:if>
          </xsl:otherwise>
        </xsl:choose>
      </td>
    </tr>

  </xsl:template>

  <xsl:template name="PrintMultiLevelParameters">
    <xsl:if test="count(Parameters/Parameter[@MultiLevel='true'])>=1">
      <div class="stat-multilevel-parameters">
        <xsl:for-each select="Parameters/Parameter[@MultiLevel='true']">
          <xsl:variable name="DimensionCode" select="@DimensionCode"/>
          <div class="stat-multilevel-parameter">
            <xsl:attribute name="data-dimension">
              <xsl:value-of select="@DimensionCode"/>
            </xsl:attribute>
            <xsl:if test="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/@MaxLevel > 1">
              <xsl:call-template name="PrintLevelControls">
                <xsl:with-param name="MaxLevel" select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/@MaxLevel"/>
              </xsl:call-template>
            </xsl:if>
            <xsl:call-template name="PrintMultiLevelParameter">
              <xsl:with-param name="DimensionCode" select="$DimensionCode"/>
            </xsl:call-template>
          </div>
        </xsl:for-each>
      </div>
    </xsl:if>
   </xsl:template>

  <xsl:template name="PrintMultiLevelParameter">
    <xsl:param name="DimensionCode"/>
    <xsl:param name="ElementCode"/>

    <xsl:variable name="Dimension" select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]"/>
    <ul>
      <xsl:for-each select="$Dimension/Element[@ReportUrl and (Parent/@Code=$ElementCode or (count(Parent/@Code)=0 and not($ElementCode)))]">
        <li>
          <xsl:attribute name="data-elementCode">
            <xsl:value-of select="@Code"/>
          </xsl:attribute>
          <xsl:variable name="Code" select="@Code"/>
          <xsl:if test="$Dimension/Element[@ReportUrl and (Parent/@Code=$Code)]">
            <xsl:call-template name="PrintCollapseControl">
              <xsl:with-param name="IsOpen" select="true()"/>
            </xsl:call-template>
          </xsl:if>
          <a>
            <xsl:attribute name="href">
              <xsl:call-template name="string-replace-all">
                <xsl:with-param name="text" select="@ReportUrl"/>
                <xsl:with-param name="replace" select="'%7bview%7d'"/>
                <xsl:with-param name="by" select="$view"/>
              </xsl:call-template>
            </xsl:attribute>
            <xsl:call-template name="PrintName">
              <xsl:with-param name="DimensionCode" select="$DimensionCode"/>
              <xsl:with-param name="ElementCode" select="@Code"/>
            </xsl:call-template>
          </a>
          <xsl:call-template name="PrintMultiLevelParameter">
            <xsl:with-param name="DimensionCode" select="$DimensionCode" />
            <xsl:with-param name="ElementCode" select="@Code"/>
          </xsl:call-template>
        </li>

      </xsl:for-each>
    </ul>

  </xsl:template>

  <xsl:template name="PrintHeader">

    <xsl:for-each select="TableHeader[@Type='Horizontal']/Header[position()=1]/Element">

      <xsl:variable name="rowNum" select="position()"/>

      <tr>

        <!-- Ячейка в левом верхнем углу таблицы-->
        <xsl:if test="$rowNum=1 and count(../../../TableHeader[@Type='Vertical']/Header)>0">

          <th class="stat-level-1">
            <!--<xsl:attribute name="ColSpan"><xsl:value-of select="count(../../../TableHeader[@Type='Vertical']/Header[position()=1]/Element)"/></xsl:attribute>-->
            <xsl:attribute name="RowSpan">
              <xsl:value-of select="count(../../../TableHeader[@Type='Horizontal']/Header[position()=1]/Element)"/>
            </xsl:attribute>

            <xsl:for-each select="../../../TableHeader[@Type='Vertical']/Header[position()=1]/Element">

              <xsl:variable name="dimCode" select="@DimensionCode"/>

              <xsl:choose>
                <xsl:when test="count(@CustomName) &gt; 0">
                  <xsl:value-of select="@CustomName"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="/Reports/Dimensions/Dimension[@Code=$dimCode]/@Name"/>
                </xsl:otherwise>
              </xsl:choose>

              <xsl:if test="position()!=last()">
                <xsl:text> / </xsl:text>
              </xsl:if>

            </xsl:for-each>
          </th>
        </xsl:if>

        <xsl:for-each select="../../Header/Element[position()=$rowNum]">
          <xsl:if test="@Span1!=-1 and @Span2!=-1">
            <th>
              <xsl:attribute name="class">
                <xsl:text>stat-level-</xsl:text>
                <xsl:value-of select="@Level"/>
              </xsl:attribute>
              <xsl:attribute name="ColSpan">
                <xsl:value-of select="@Span1"/>
              </xsl:attribute>
              <xsl:attribute name="RowSpan">
                <xsl:value-of select="@Span2"/>
              </xsl:attribute>

              <xsl:call-template name="PrintHeaderElement">
                <xsl:with-param name="DimensionCode" select="@DimensionCode"/>
                <xsl:with-param name="ElementCode" select="@Code"/>
                <xsl:with-param name="DetailsReportURL" select="@DetailsReportURL"/>
                <xsl:with-param name="CustomName" select="@CustomName"/>
              </xsl:call-template>


            </th>
          </xsl:if>
        </xsl:for-each>

      </tr>

    </xsl:for-each>

    <xsl:if test="/Reports/Options/Option[@Code='WriteColumnNumbers']/@Value = 'true'">
      <xsl:variable name="columnNumbersFormat" select="/Reports/Options/Option[@Code='ColumnNumbersFormat']/@Value"/>
      <tr>
        <xsl:for-each select="TableHeader[@Type='Vertical']/Header[position()=1]/Element ">
          <th>
            <xsl:value-of select="format-number(position(), $columnNumbersFormat)"/>
          </th>
        </xsl:for-each>
        <xsl:variable name="countVertical" select="count(TableHeader[@Type='Vertical']/Header[position()=1]/Element)"/>
        <xsl:for-each select="TableHeader[@Type='Horizontal']/Header ">
          <th>
            <xsl:value-of select="format-number($countVertical + position(), $columnNumbersFormat)"/>
          </th>
        </xsl:for-each>
      </tr>
    </xsl:if>

  </xsl:template>

  <xsl:template name="PrintBody">
    <xsl:variable name="defaultLevel" select="TableHeader[@Type='Vertical']/@DefaultLevel"/>
    <xsl:variable name="maxLevel" select="TableHeader[@Type='Vertical']/@MaxLevel"/>
    <xsl:for-each select="TableHeader[@Type='Vertical']/Header">
      <xsl:variable name="rowNum" select="position()"/>
      <tr>

        <xsl:attribute name="class">
          <xsl:text>stat-row-level-</xsl:text>
          <xsl:value-of select="@Level"/>
          <xsl:if test="string-length(@CssClass) > 0">
            <xsl:text> </xsl:text>
            <xsl:value-of select="@CssClass"/>
          </xsl:if>
        </xsl:attribute>
        <xsl:attribute name="data-level">
          <xsl:value-of select="@Level"/>
        </xsl:attribute>
        <xsl:if test="@Level > $defaultLevel">
          <xsl:attribute name="style">
            <xsl:text>display: none;</xsl:text>
          </xsl:attribute>
        </xsl:if>


        <th>
          <xsl:attribute name="class">
            <xsl:text>stat-level-</xsl:text>
            <xsl:value-of select="@Level"/>
          </xsl:attribute>
          <xsl:if test="@HasNextLevels = 'true'">
            <xsl:call-template name="PrintCollapseControl">
              <xsl:with-param name="IsOpen" select="@Level &lt; $defaultLevel"/>
            </xsl:call-template>
          </xsl:if>
          <xsl:for-each select="Element[@Span1!=-1 and @Span2!=-1]">
            <xsl:if test="position() > 1">
              <span> / </span>
            </xsl:if>
            <xsl:call-template name="PrintHeaderElement">
              <xsl:with-param name="DimensionCode" select="@DimensionCode"/>
              <xsl:with-param name="ElementCode" select="@Code"/>
              <xsl:with-param name="ReportURL" select="@ReportURL"/>
              <xsl:with-param name="CustomName" select="@CustomName"/>
            </xsl:call-template>
          </xsl:for-each>
          <!--
          <xsl:attribute name="class">
            <xsl:text>stat-level-</xsl:text>
            <xsl:value-of select="$level"/>
            <xsl:if test="string-length(../@CssClass) > 0">
              <xsl:text> </xsl:text>
              <xsl:value-of select="../@CssClass"/>
            </xsl:if>
          </xsl:attribute>
          -->




          <!--<xsl:for-each select="Element[@Span1!=-1 and @Span2!=-1]">

            <xsl:variable name="dimCode" select="@DimensionCode"/>
            <xsl:variable name="elemCode" select="@Code"/>

            <xsl:if test="@Code!='0'">


            </xsl:if>
          </xsl:for-each>-->
        </th>

        <!-- Печать ячеек с показателями в строке -->
        <xsl:for-each select="../../TableData/Row[position()=$rowNum]/Cell">
          <xsl:call-template name="PrintTableCell">
            <xsl:with-param name="Value" select="."/>
            <xsl:with-param name="CssClass" select="@CssClass"/>
            <xsl:with-param name="Span" select="@Span"/>
          </xsl:call-template>
        </xsl:for-each>

      </tr>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="PrintCollapseControl">
    <xsl:param name="IsOpen"/>
    <a href="#" class="stat-collapse-control">
      <span class="glyphicon glyphicon-minus" aria-hidden="true">
        <xsl:attribute name="class">
          <xsl:choose>
            <xsl:when test="$IsOpen">
              <xsl:text>glyphicon glyphicon-minus</xsl:text>
            </xsl:when>
            <xsl:otherwise>
              <xsl:text>glyphicon glyphicon-plus</xsl:text>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
      </span>
    </a>
  </xsl:template>

  <xsl:template name="PrintHeaderElement">
    <xsl:param name="DimensionCode"/>
    <xsl:param name="ElementCode"/>
    <xsl:param name="ReportUrl"/>
    <xsl:param name="CustomName"/>

    <xsl:variable name="ReportUrl2" select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/Element[@Code=$ElementCode]/@ReportUrl"/>

    <xsl:choose>
      <xsl:when test="string-length($ReportUrl) > 0 or string-length($ReportUrl2) > 0">
        <a>
          <xsl:attribute name="href">
            <xsl:choose>
              <xsl:when test="string-length($ReportUrl) > 0">
                <xsl:call-template name="string-replace-all">
                  <xsl:with-param name="text" select="$ReportUrl"/>
                  <xsl:with-param name="replace" select="'%7bview%7d'"/>
                  <xsl:with-param name="by" select="$view"/>
                </xsl:call-template>
              </xsl:when>
              <xsl:otherwise>
                <xsl:call-template name="string-replace-all">
                  <xsl:with-param name="text" select="$ReportUrl2"/>
                  <xsl:with-param name="replace" select="'%7bview%7d'"/>
                  <xsl:with-param name="by" select="$view"/>
                </xsl:call-template>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:attribute>
          <xsl:choose>
            <xsl:when test="string-length($CustomName) > 0">
              <xsl:value-of select="$CustomName"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:call-template name="PrintName">
                <xsl:with-param name="DimensionCode" select="$DimensionCode"/>
                <xsl:with-param name="ElementCode" select="$ElementCode"/>
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <span>
          <xsl:choose>
            <xsl:when test="string-length($CustomName) > 0">
              <xsl:value-of select="$CustomName"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:call-template name="PrintName">
                <xsl:with-param name="DimensionCode" select="$DimensionCode"/>
                <xsl:with-param name="ElementCode" select="$ElementCode"/>
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>
        </span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="string-replace-all">
    <xsl:param name="text" />
    <xsl:param name="replace" />
    <xsl:param name="by" />
    <xsl:choose>
      <xsl:when test="contains($text, $replace)">
        <xsl:value-of select="substring-before($text,$replace)" />
        <xsl:value-of select="$by" />
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text"
          select="substring-after($text,$replace)" />
          <xsl:with-param name="replace" select="$replace" />
          <xsl:with-param name="by" select="$by" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="PrintTableCell">
    <xsl:param name="Value"/>
    <xsl:param name="CssClass"/>
    <xsl:param name="Span"/>
    <xsl:if test="$Span > 0">
      <td>
        <xsl:if test="string-length($CssClass) > 0">
          <xsl:attribute name="class">
            <xsl:value-of select="$CssClass"/>
          </xsl:attribute>
        </xsl:if>

        <xsl:if test="$Span > 0">
          <xsl:attribute name="rowSpan">
            <xsl:value-of select="$Span"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:value-of select="$Value"/>
      </td>
    </xsl:if>
  </xsl:template>

  <xsl:template name="PrintName">
    <xsl:param name="DimensionCode"/>
    <xsl:param name="ElementCode"/>

    <xsl:variable name="nameColumn" select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/@NameColumn"/>
    <xsl:variable name="name" select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/Element[@Code=$ElementCode]/@*[name()=$nameColumn]"/>
    <xsl:choose>
      <xsl:when test="string-length($name) > 0">
        <xsl:call-template name="PrintString">
          <xsl:with-param name="string" select="$name"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="PrintString">
          <xsl:with-param name="string" select="$ElementCode"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="PrintFullName">
    <xsl:param name="DimensionCode"/>
    <xsl:param name="ElementCode"/>

    <xsl:for-each select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/Element[@Code=$ElementCode]/Parent2/@Code">
      <div>
        <xsl:call-template name="PrintName">
          <xsl:with-param name="DimensionCode" select="$DimensionCode" />
          <xsl:with-param name="ElementCode" select="." />
        </xsl:call-template>
      </div>
    </xsl:for-each>
    <xsl:if test="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/Element[@Code=$ElementCode]/Parent/@Code">
      <div>
        <xsl:call-template name="PrintName">
          <xsl:with-param name="DimensionCode" select="$DimensionCode" />
          <xsl:with-param name="ElementCode" select="/Reports/Dimensions/Dimension[@Code=$DimensionCode]/Element[@Code=$ElementCode]/Parent/@Code" />
        </xsl:call-template>
      </div>
    </xsl:if>
    <div>
      <xsl:call-template name="PrintName">
        <xsl:with-param name="DimensionCode" select="$DimensionCode" />
        <xsl:with-param name="ElementCode" select="$ElementCode" />
      </xsl:call-template>
    </div>
  </xsl:template>

    <!-- Печать строки с заменой символа новой строки на тэг <br/> -->
  <xsl:template name="PrintString">
    <xsl:param name="string" />
    <xsl:choose>
      <xsl:when test="contains($string, '&#xa;')">
        <xsl:value-of select="substring-before($string, '&#xa;')"/>
        <br/>
        <xsl:call-template name="PrintString">
          <xsl:with-param name="string" select="substring-after($string, '&#xa;')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$string"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>