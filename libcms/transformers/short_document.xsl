<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:marc="http://www.loc.gov/MARC21/slim"
                xmlns:exsl="http://exslt.org/common"
                exclude-result-prefixes="marc exsl">
    <xsl:output
            method="html"
            indent="yes"
            encoding="utf-8"
            standalone="no"
            omit-xml-declaration="no"
            />

    <xsl:template name="replace">
        <xsl:param name="input"/>
        <xsl:param name="from"/>
        <xsl:param name="to"/>

        <xsl:choose>
            <xsl:when test="contains($input, $from)">
                <!--   вывод подстроки предшествующей образцу  + вывод строки замены -->
                <xsl:value-of select="substring-before($input, $from)"/>
                <xsl:value-of select="$to"/>


                <!--   вход в итерацию -->
                <xsl:call-template name="replace">
                    <!--  в качестве входного параметра задается подстрока после образца замены  -->
                    <xsl:with-param name="input" select="substring-after($input, $from)"/>
                    <xsl:with-param name="from" select="$from"/>
                    <xsl:with-param name="to" select="$to"/>
                </xsl:call-template>

            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$input"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <xsl:template match="/record">


        <!-- Для МНОГОТОМНИКА с индикатором 1 -->
        <xsl:if test="field[@id='200']/indicator[@id='1'] = 1 and field[@id='461']/subfield[@id='1'] and not(field[@id='463']/subfield[@id='1']) and leader/type='a'">
            <!-- 700а фамилия -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='a']">
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='a']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>
            <!-- 700b инициалы -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b']">
                <xsl:choose>
                    <xsl:when
                            test="contains(field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b'], '.')">
                        <xsl:value-of
                                select="substring-before(field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b'], '.')"/>
                        <xsl:text disable-output-escaping="yes">. </xsl:text>
                        <xsl:value-of
                                select="normalize-space(substring-after(field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b'], '.'))"/>
                        <xsl:text disable-output-escaping="yes"> </xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b']"/>
                        <xsl:text disable-output-escaping="yes"></xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>

            <!-- 200a основное заглавие -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>

            <!-- маркер записи - тип документа -->

            <xsl:if test="leader/type = 'a'">
                [Текст]
            </xsl:if>

            <!-- 200v номер тома -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
                <xsl:text disable-output-escaping="yes">:</xsl:text>
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
            </xsl:if>

            <!-- 200a основное заглавие -->
            <xsl:if test="field[@id='200']/subfield[@id='a']">
                <xsl:text disable-output-escaping="yes"></xsl:text>
                <xsl:value-of select="field[@id='200']/subfield[@id='a']"/>
            </xsl:if>

            <!-- 210a город издания тома -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                <xsl:text disable-output-escaping="yes">. —</xsl:text>


                <xsl:for-each select="field[@id='461']/subfield[@id='1']/field[@id='210'][subfield[@id='a']]">
                    <xsl:for-each select="subfield[@id='a']">
                        <xsl:if test="position()>1">
                            <xsl:text disable-output-escaping="yes">;</xsl:text>
                        </xsl:if>
                        <xsl:choose>
                            <!-- если москва -->
                            <xsl:when test=".='Москва'">
                                <xsl:text disable-output-escaping="yes">М.</xsl:text>
                            </xsl:when>
                            <xsl:when test=".='Ленинград'">
                                <xsl:text disable-output-escaping="yes">Л.</xsl:text>
                            </xsl:when>
                            <xsl:when test=".='Санкт-Петербург'">
                                <xsl:text disable-output-escaping="yes">СПб.</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:if test=".">
                                    <xsl:value-of select="."/>
                                </xsl:if>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:for-each>
            </xsl:if>

            <!-- 210c имя издательства -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='c']">
                <xsl:text disable-output-escaping="yes">:</xsl:text>
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='c']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>

            <!-- 210d год издания -->
            <xsl:if test="not(field[@id='210']/subfield[@id='d'])">
                <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                    <xsl:text disable-output-escaping="yes">,</xsl:text>
                    <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                    <xsl:choose>
                        <xsl:when
                                test="substring(field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d'], string-length(field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d'])) = '.'">
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text disable-output-escaping="yes">.</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:if>
            </xsl:if>


        </xsl:if>

        <!-- конец многотомника -->

        <!-- Для конференций - название конференции -->
        <xsl:if test="field[@id='710']/subfield[@id='a']">
            <xsl:value-of select="field[@id='710']/subfield[@id='a']"/>
            <xsl:text disable-output-escaping="yes">.</xsl:text>
        </xsl:if>

        <!-- 700а фамилия -->
        <xsl:if test="field[@id='700']/subfield[@id='a']">
            <xsl:value-of select="field[@id='700']/subfield[@id='a']"/>
            <xsl:text disable-output-escaping="yes"> </xsl:text>
        </xsl:if>
        <!-- 700b инициалы -->
        <xsl:if test="field[@id='700']/subfield[@id='b']">
            <xsl:choose>
                <xsl:when test="contains(field[@id='700']/subfield[@id='b'], '.')">
                    <xsl:value-of select="substring-before(field[@id='700']/subfield[@id='b'], '.')"/>
                    <xsl:text disable-output-escaping="yes">.</xsl:text>
                    <xsl:value-of select="normalize-space(substring-after(field[@id='700']/subfield[@id='b'], '.'))"/>
                    <xsl:text disable-output-escaping="yes"> </xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="field[@id='700']/subfield[@id='b']"/>
                    <xsl:text disable-output-escaping="yes"> 111</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>

        <!-- еСли ГОСТ -->

            <xsl:if test="field[@id='029']/subfield[@id='c']">
                <xsl:value-of select="field[@id='029']/subfield[@id='c']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>
            <xsl:if test="field[@id='029']/subfield[@id='b']">
                <xsl:value-of select="field[@id='029']/subfield[@id='b']"/>
                <xsl:text disable-output-escaping="yes">.</xsl:text>
            </xsl:if>

        <!-- конец названия ГОСТа -->

        <!-- 200a основное заглавие -->
        <xsl:if test="field[@id='200']/indicator[@id='1']=1"> <!-- если не многотомник -->
            <xsl:choose>
                <xsl:when test="field[@id='461']/subfield[@id='1'] and not(field[@id='463']/subfield[@id='1'])">
                </xsl:when>
                <xsl:otherwise>
                    <xsl:if test="field[@id='200']/subfield[@id='a'] and leader/type='a'">
                        <xsl:value-of select="field[@id='200']/subfield[@id='a']"/>
                        <xsl:text disable-output-escaping="yes"> </xsl:text>
                    </xsl:if>


                    <!-- маркер записи - тип документа -->

                    <xsl:if test="leader/type = 'a'"><xsl:text>[Текст]</xsl:text></xsl:if>
                </xsl:otherwise>
            </xsl:choose>

            <xsl:choose>
                <!-- Link Source -->
                <xsl:when test="leader/type = 'l'">

                    <xsl:if test="field[@id='200']/subfield[@id='a']">
                        <xsl:text disable-output-escaping="yes"></xsl:text>
                        <xsl:value-of select="field[@id='200']/subfield[@id='a']"/>
                        <xsl:text disable-output-escaping="yes"></xsl:text>
                    </xsl:if>

                    <xsl:if test="field[@id='200']/subfield[@id='b']">
                        <xsl:text disable-output-escaping="yes">[</xsl:text>
                        <xsl:value-of select="field[@id='200']/subfield[@id='b']"/>
                        <xsl:text disable-output-escaping="yes">]</xsl:text>
                    </xsl:if>

                    <!-- если электронный ресурс содержит 461 поле -->

                    <xsl:if test="field[@id='461']/subfield[@id='1'] and not(field[@id='463']/subfield[@id='1'])">

                        <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                            <xsl:text disable-output-escaping="yes">//</xsl:text>
                            <xsl:value-of
                                    select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>

                            <!-- 200e  -->
                            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='e']">
                                <xsl:text disable-output-escaping="yes">:</xsl:text>
                                <xsl:value-of
                                        select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='e']"/>
                            </xsl:if>

                            <!-- 210a место издания -->
                            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                                <xsl:text disable-output-escaping="yes">. —</xsl:text>


                                <xsl:for-each
                                        select="field[@id='461']/subfield[@id='1']/field[@id='210'][subfield[@id='a']]">
                                    <xsl:for-each select="subfield[@id='a']">
                                        <xsl:if test="position()>1">
                                            <xsl:text disable-output-escaping="yes">;</xsl:text>
                                        </xsl:if>
                                        <xsl:choose>
                                            <!-- если москва -->
                                            <xsl:when test=".='Москва'">
                                                <xsl:text disable-output-escaping="yes">М.</xsl:text>
                                            </xsl:when>
                                            <xsl:when test=".='Ленинград'">
                                                <xsl:text disable-output-escaping="yes">Л.</xsl:text>
                                            </xsl:when>
                                            <xsl:when test=".='Санкт‑Петербург'">
                                                <xsl:text disable-output-escaping="yes">СПб.</xsl:text>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:if test=".">
                                                    <xsl:value-of select="."/>
                                                </xsl:if>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </xsl:for-each>
                                </xsl:for-each>
                            </xsl:if>
                        </xsl:if>


                        <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                            <xsl:text disable-output-escaping="yes">,</xsl:text>
                            <xsl:value-of
                                    select="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                            <!--		<xsl:text disable-output-escaping="yes">. —</xsl:text>  -->
                        </xsl:if>
                    </xsl:if>


                    <!-- end of link 461 -->
                    <!-- <xsl:if test = "field[@id='200']/subfield[@id='e']"> <xsl:text disable-output-escaping="yes"> : </xsl:text>
             <xsl:choose>
             <xsl:when test="substring(normalize-space(field[@id='200']/subfield[@id='e']), string-length(normalize-space(field[@id='200']/subfield[@id='e']))) = '.'">
             <xsl:value-of select="substring(normalize-space(field[@id='200']/subfield[@id='e']), 0, string-length(normalize-space(field[@id='200']/subfield[@id='e'])))" />
             </xsl:when>
             <xsl:otherwise>
             <xsl:value-of select="field[@id='200']/subfield[@id='e']" />
             </xsl:otherwise>
             </xsl:choose>
                 </xsl:if> -->

                    <xsl:if test="field[@id='452']/subfield[@id='1']/field[@id='229']/subfield[@id='a']">
                        <xsl:text disable-output-escaping="yes">:</xsl:text>
                        <xsl:value-of select="field[@id='200']/subfield[@id='e']"/>
                        <xsl:text disable-output-escaping="yes"></xsl:text>
                    </xsl:if>

                    <xsl:if test="field[@id='700']/subfield[@id='a'] or field[@id='701']/subfield[@id='a']">
                        <xsl:if test="contains(field[@id='200']/subfield[@id='f'], ',') or contains(field[@id='200']/subfield[@id='f'], 'и др.')">
                            <xsl:text disable-output-escaping="yes">/</xsl:text>

                            <!-- Замена точки на точку-пробел -->
                            <xsl:call-template name="replace">
                                <xsl:with-param name="input" select="field[@id='200']/subfield[@id='f']"/>
                                <xsl:with-param name="from" select="'.'"/>
                                <xsl:with-param name="to" select="'. '"/>
                            </xsl:call-template>

                        </xsl:if>
                    </xsl:if>

                    <xsl:if test="field[@id='210']/subfield[@id='a']">
                        <xsl:text disable-output-escaping="yes">. —</xsl:text>
                        <xsl:value-of select="field[@id='210']/subfield[@id='a']"/>
                    </xsl:if>

                    <xsl:if test="field[@id='210']/subfield[@id='d']">
                        <xsl:text disable-output-escaping="yes">,</xsl:text>
                        <xsl:value-of select="field[@id='210']/subfield[@id='d']"/>
                        <!-- определение точки в конце -->
                        <xsl:choose>
                            <xsl:when
                                    test="substring(field[@id='210']/subfield[@id='d'], string-length(field[@id='210']/subfield[@id='d'])) = '.'">

                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text disable-output-escaping="yes"></xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>

                    <!-- 215a объем -->
                    <xsl:if test="field[@id='215']/subfield[@id='a']">
                        <xsl:choose>
                            <xsl:when
                                    test="substring(field[@id='215']/subfield[@id='a'], string-length(field[@id='215']/subfield[@id='a'])) = '.'">
                                <xsl:text disable-output-escaping="yes"> —</xsl:text>
                                <xsl:value-of select="field[@id='215']/subfield[@id='a']"/>

                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text disable-output-escaping="yes"> —</xsl:text>
                                <xsl:value-of select="field[@id='215']/subfield[@id='a']"/>
                                <xsl:text disable-output-escaping="yes">.</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>

                    <!-- если электронный ресурс содержит 461+463 поле -->

                    <xsl:if test="field[@id='461']/subfield[@id='1'] and field[@id='463']/subfield[@id='1']">

                        <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                            <xsl:text disable-output-escaping="yes">//</xsl:text>
                            <xsl:value-of
                                    select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                        </xsl:if>
                        <!-- 200e  -->
                        <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='e']">
                            <xsl:text disable-output-escaping="yes">:</xsl:text>
                            <xsl:value-of
                                    select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='e']"/>
                        </xsl:if>

                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                            <xsl:text disable-output-escaping="yes">. —</xsl:text>
                            <xsl:value-of
                                    select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']"/>
                        </xsl:if>

                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                            <xsl:if test="not(field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a'])">
                                <xsl:text disable-output-escaping="yes">. —</xsl:text>
                            </xsl:if>
                            <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                                <xsl:text disable-output-escaping="yes">,</xsl:text>
                            </xsl:if>
                            <xsl:value-of
                                    select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                        </xsl:if>

                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                            <xsl:text disable-output-escaping="yes">. —</xsl:text>
                            <xsl:choose>
                                <xsl:when
                                        test="substring(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a'], 1, 1) = '№'">
                                    <xsl:text disable-output-escaping="yes">№ </xsl:text>
                                    <!-- <xsl:value-of select="substring(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a'], 2)" />  -->

                                    <!-- Замена двоеточия на пробел-двоеточие -->
                                    <xsl:call-template name="replace">
                                        <xsl:with-param name="input"
                                                        select="substring(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a'], 2)"/>
                                        <xsl:with-param name="from" select="':'"/>
                                        <xsl:with-param name="to" select="' :'"/>
                                    </xsl:call-template>

                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:if>

                    </xsl:if>
                    <!-- end of -->

                    <xsl:if test="field[@id='463']/subfield[@id='1'] and not(field[@id='461']/subfield[@id='1'])">
                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                            <xsl:text disable-output-escaping="yes">//</xsl:text>
                            <xsl:value-of
                                    select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                        </xsl:if>

                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='f']">
                            <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='700']/subfield[@id='a'] or field[@id='463']/subfield[@id='1']/field[@id='701']/subfield[@id='a']">
                                <xsl:text disable-output-escaping="yes">/</xsl:text>
                                <xsl:value-of
                                        select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='f']"/>
                            </xsl:if>
                        </xsl:if>

                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                            <xsl:text disable-output-escaping="yes">. —</xsl:text>
                            <xsl:value-of
                                    select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']"/>
                        </xsl:if>

                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                            <xsl:text disable-output-escaping="yes">,</xsl:text>
                            <xsl:value-of
                                    select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                        </xsl:if>

                    </xsl:if>
                    <xsl:if test="field[@id='856']/subfield[@id='u']">
                        <xsl:text disable-output-escaping="yes">. — Режим доступа:</xsl:text>
                        <a href="#">
                            <xsl:value-of select="field[@id='856']/subfield[@id='u']"/>
                        </a>
                        <xsl:text disable-output-escaping="yes">.</xsl:text>
                    </xsl:if>

                </xsl:when>
                <!-- end of link source -->
                <xsl:otherwise>

                    <!-- 200e сведения относящиеся к заглавию -->
                    <xsl:variable name="smallcase" select="'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'"/>
                    <xsl:variable name="uppercase" select="'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'"/>
                    <xsl:for-each select="field[@id='200'][subfield[@id='e']]">
                        <xsl:for-each select="subfield[@id='e']">
                            <xsl:text disable-output-escaping="yes">:</xsl:text>
                            <xsl:value-of select="translate(substring(., 1, 1), $uppercase, $smallcase)"/>
                            <!-- <xsl:value-of select="substring(., 2)" /> -->

                            <xsl:choose>
                                <xsl:when test="substring(substring(., 2), string-length(substring(., 2))) = '.'">
                                    <xsl:value-of select="substring(., 2, string-length(substring(., 2))-1)"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="substring(., 2)"/>
                                </xsl:otherwise>
                            </xsl:choose>

                        </xsl:for-each>
                    </xsl:for-each>

                    <!-- 200f первые сведения об ответственности -->
                    <xsl:if test="field[@id='700']/subfield[@id='a'] or field[@id='701']/subfield[@id='a']">
                        <xsl:if test="field[@id='200']/subfield[@id='f']">
                            <xsl:if test="contains(field[@id='200']/subfield[@id='f'], ',') or contains(field[@id='200']/subfield[@id='f'], '[')">
                                <xsl:text disable-output-escaping="yes">/</xsl:text>
                                <xsl:choose>
                                    <xsl:when
                                            test="contains(field[@id='200']/subfield[@id='f'], 'и др.') and contains(field[@id='200']/subfield[@id='f'], ',')">
                                        <xsl:value-of
                                                select="substring-before(field[@id='200']/subfield[@id='f'], ',')"/>
                                        <xsl:text disable-output-escaping="yes">[и др.]</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise>

                                        <!-- Замена точки на точку-пробел -->
                                        <xsl:call-template name="replace">
                                            <xsl:with-param name="input" select="field[@id='200']/subfield[@id='f']"/>
                                            <xsl:with-param name="from" select="'.'"/>
                                            <xsl:with-param name="to" select="'. '"/>
                                        </xsl:call-template>


                                        <!--<xsl:value-of select="field[@id='200']/subfield[@id='f']" />   <xsl:text disable-output-escaping="yes">. - </xsl:text> -->
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:if>
                        </xsl:if>
                    </xsl:if>
                    <!-- 205ab сведения относящиеся к заглавию -->
                    <xsl:if test="field[@id='205']/subfield[@id='a']">
                        <xsl:text disable-output-escaping="yes">. —</xsl:text>
                        <!-- <xsl:value-of select="normalize-space(field[@id='205']/subfield[@id='a'])" /> -->

                        <!-- определение точки в конце -->
                        <xsl:choose>
                            <xsl:when
                                    test="substring(field[@id='205']/subfield[@id='a'], string-length(field[@id='205']/subfield[@id='a'])) = '.'">
                                <xsl:value-of
                                        select="normalize-space(substring(field[@id='205']/subfield[@id='a'], string-length(field[@id='205']/subfield[@id='a'])))"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="normalize-space(field[@id='205']/subfield[@id='a'])"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>

                    <xsl:if test="field[@id='205']/subfield[@id='b']">
                        <xsl:text disable-output-escaping="yes">.,</xsl:text>
                        <xsl:choose>
                            <xsl:when
                                    test="substring(field[@id='205']/subfield[@id='b'], string-length(field[@id='205']/subfield[@id='b'])) = '.'">
                                <xsl:value-of
                                        select="normalize-space(substring(field[@id='205']/subfield[@id='b'], 0, string-length(field[@id='205']/subfield[@id='b'])))"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="normalize-space(field[@id='205']/subfield[@id='b'])"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>


                    <!-- журнал -->
                    <!-- НАЧАЛО ЖУРНАЛА -->
                    <xsl:if test="field[@id='461']/subfield[@id='1'] or field[@id='463']/subfield[@id='1']">

                        <xsl:choose>
                            <xsl:when test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                                <xsl:text disable-output-escaping="yes">//</xsl:text>
                                <xsl:value-of
                                        select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                                <!-- <xsl:text disable-output-escaping="yes">. — </xsl:text>   -->


                                <!-- 210a место издания -->
                                <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                                    <xsl:text disable-output-escaping="yes">. —</xsl:text>


                                    <xsl:for-each
                                            select="field[@id='461']/subfield[@id='1']/field[@id='210'][subfield[@id='a']]">
                                        <xsl:for-each select="subfield[@id='a']">
                                            <xsl:if test="position()>1">
                                                <xsl:text disable-output-escaping="yes">;</xsl:text>
                                            </xsl:if>
                                            <xsl:choose>
                                                <!-- если москва -->
                                                <xsl:when test=".='Москва'">
                                                    <xsl:text disable-output-escaping="yes">М.</xsl:text>
                                                </xsl:when>
                                                <xsl:when test=".='Ленинград'">
                                                    <xsl:text disable-output-escaping="yes">Л.</xsl:text>
                                                </xsl:when>
                                                <xsl:when test=".='Санкт-Петербург'">
                                                    <xsl:text disable-output-escaping="yes">СПб.</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:if test=".">
                                                        <xsl:value-of select="."/>
                                                    </xsl:if>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:for-each>
                                    </xsl:for-each>
                                </xsl:if>


                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                                    <xsl:text disable-output-escaping="yes">,</xsl:text>
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                                    <xsl:text disable-output-escaping="yes">. —</xsl:text>

                                    <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                                        <xsl:choose>
                                            <xsl:when
                                                    test="substring(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a'], 1, 1) = '№'">
                                                <xsl:text disable-output-escaping="yes">№ </xsl:text>
                                                <!-- <xsl:value-of select="substring(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a'], 2)" />  -->

                                                <!-- Замена двоеточия на пробел-двоеточие -->
                                                <xsl:call-template name="replace">
                                                    <xsl:with-param name="input"
                                                                    select="substring(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a'], 2)"/>
                                                    <xsl:with-param name="from" select="':'"/>
                                                    <xsl:with-param name="to" select="' :'"/>
                                                </xsl:call-template>

                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of
                                                        select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                                            </xsl:otherwise>
                                        </xsl:choose>

                                        <!-- Номер станицы в журнале 463-200v или 463-200i-->

                                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
                                            <xsl:text disable-output-escaping="yes">. —</xsl:text>

                                            <!-- Замена точки на точку-пробел -->
                                            <xsl:choose>
                                                <xsl:when
                                                        test="contains(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v'], ':')">
                                                    <xsl:call-template name="replace">
                                                        <xsl:with-param name="input"
                                                                        select="normalize-space(substring-before(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v'], ':'))"/>
                                                        <xsl:with-param name="from" select="'.'"/>
                                                        <xsl:with-param name="to" select="'. '"/>
                                                    </xsl:call-template>
                                                    <!-- <xsl:value-of select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']" />   -->
                                                    <!-- определение точки в конце -->
                                                    <xsl:choose>
                                                        <xsl:when
                                                                test="substring(normalize-space(substring-before(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v'], ':')), string-length(normalize-space(substring-before(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v'], ':')))) = '.'">

                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:text disable-output-escaping="yes">.</xsl:text>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:call-template name="replace">
                                                        <xsl:with-param name="input"
                                                                        select="normalize-space(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v'])"/>
                                                        <xsl:with-param name="from" select="'.'"/>
                                                        <xsl:with-param name="to" select="'. '"/>
                                                    </xsl:call-template>

                                                    <!-- определение точки в конце -->
                                                    <xsl:choose>
                                                        <xsl:when
                                                                test="substring(normalize-space(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']), string-length(normalize-space(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']))) = '.'">

                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:text disable-output-escaping="yes">.</xsl:text>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:if>
                                        <!-- 200i -->
                                        <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i']">
                                            <xsl:text disable-output-escaping="yes">. —</xsl:text>
                                            <xsl:choose>
                                                <xsl:when
                                                        test="contains(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i'], ':')">
                                                    <xsl:call-template name="replace">
                                                        <xsl:with-param name="input"
                                                                        select="normalize-space(substring-before(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i'], ':'))"/>
                                                        <xsl:with-param name="from" select="'.'"/>
                                                        <xsl:with-param name="to" select="'. '"/>
                                                    </xsl:call-template>
                                                    <!-- <xsl:value-of select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']" />   -->
                                                    <!-- определение точки в конце -->
                                                    <xsl:choose>
                                                        <xsl:when
                                                                test="substring(normalize-space(substring-before(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i'], ':')), string-length(normalize-space(substring-before(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i'], ':')))) = '.'">

                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:text disable-output-escaping="yes">.</xsl:text>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:call-template name="replace">
                                                        <xsl:with-param name="input"
                                                                        select="normalize-space(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i'])"/>
                                                        <xsl:with-param name="from" select="'.'"/>
                                                        <xsl:with-param name="to" select="'. '"/>
                                                    </xsl:call-template>

                                                    <!-- определение точки в конце -->
                                                    <xsl:choose>
                                                        <xsl:when
                                                                test="substring(normalize-space(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i']), string-length(normalize-space(field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='i']))) = '.'">

                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:text disable-output-escaping="yes">.</xsl:text>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:if>
                                    </xsl:if>
                                </xsl:if>
                            </xsl:when>

                            <!-- конференция/выступление,доклад итд -->
                            <xsl:otherwise>
                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                                    <xsl:text disable-output-escaping="yes">//</xsl:text>
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                                    <xsl:text disable-output-escaping="yes">:</xsl:text>
                                </xsl:if>
                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='e']">
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='e']"/>
                                    <xsl:text disable-output-escaping="yes">/</xsl:text>
                                </xsl:if>
                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='f']">
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='f']"/>
                                    <xsl:text disable-output-escaping="yes">. —</xsl:text>
                                </xsl:if>
                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='a']"/>
                                    <xsl:text disable-output-escaping="yes">,</xsl:text>
                                </xsl:if>
                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                                    <xsl:text disable-output-escaping="yes">. —</xsl:text>
                                </xsl:if>
                                <xsl:if test="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
                                    <xsl:value-of
                                            select="field[@id='463']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
                                    <xsl:text disable-output-escaping="yes">.</xsl:text>
                                </xsl:if>
                            </xsl:otherwise>
                        </xsl:choose>

                    </xsl:if>
                    <!-- КОНЕЦ ЖУРНАЛА -->

                    <!-- 200g последующие сведения об ответственности
             <xsl:if test="field[@id='200']/subfield[@id='g']">
             <xsl:text disable-output-escaping="yes"> : </xsl:text> <xsl:value-of select="field[@id='200']/subfield[@id='g']" />  <xsl:text disable-output-escaping="yes"> </xsl:text>
             </xsl:if>-->

                    <!-- если гост то поле 229а - дата введения -->
                    <xsl:if test="field[@id='029']/subfield[@id='c'] and field[@id='229']/subfield[@id='a']">
                        <xsl:text disable-output-escaping="yes">. —</xsl:text>
                        <xsl:for-each select="field[@id='229'][subfield[@id='a']]">
                            <xsl:for-each select="subfield[@id='a']">
                                <xsl:if test="position()>1">
                                    <xsl:text disable-output-escaping="yes">;</xsl:text>
                                </xsl:if>
                                <xsl:value-of select="."/>
                            </xsl:for-each>
                        </xsl:for-each>
                    </xsl:if>

                    <!-- 210a место издания -->
                    <xsl:if test="field[@id='210']/subfield[@id='a']">
                        <xsl:text disable-output-escaping="yes">. —</xsl:text>


                        <xsl:for-each select="field[@id='210'][subfield[@id='a']]">
                            <xsl:for-each select="subfield[@id='a']">
                                <xsl:if test="position()>1">
                                    <xsl:text disable-output-escaping="yes">;</xsl:text>
                                </xsl:if>
                                <xsl:choose>
                                    <!-- если москва -->
                                    <xsl:when test=".='Москва'">
                                        <xsl:text disable-output-escaping="yes">М.</xsl:text>
                                    </xsl:when>
                                    <xsl:when test=".='Ленинград'">
                                        <xsl:text disable-output-escaping="yes">Л.</xsl:text>
                                    </xsl:when>
                                    <xsl:when test=".='Санкт-Петербург'">
                                        <xsl:text disable-output-escaping="yes">СПб.</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:if test=".">
                                            <xsl:value-of select="."/>
                                        </xsl:if>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:for-each>
                        </xsl:for-each>
                        <!-- <xsl:text disable-output-escaping="yes">: </xsl:text> -->
                    </xsl:if>

                    <!-- 210c имя издательства -->
                    <xsl:if test="field[@id='210']/subfield[@id='c']">
                        <xsl:text disable-output-escaping="yes">:</xsl:text>
                        <xsl:value-of select="field[@id='210']/subfield[@id='c']"/>
                        <xsl:text disable-output-escaping="yes"></xsl:text>
                    </xsl:if>

                    <!-- 210d год издания -->
                    <xsl:if test="field[@id='210']/subfield[@id='d']">
                        <xsl:text disable-output-escaping="yes">,</xsl:text>
                        <xsl:value-of select="field[@id='210']/subfield[@id='d']"/>
                        <xsl:choose>
                            <xsl:when
                                    test="substring(field[@id='210']/subfield[@id='d'], string-length(field[@id='210']/subfield[@id='d'])) = '.'">
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text disable-output-escaping="yes">.</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>

                    <!-- 215a объем -->
                    <xsl:if test="field[@id='215']/subfield[@id='a']">
                        <xsl:choose>
                            <xsl:when
                                    test="substring(normalize-space(field[@id='215']/subfield[@id='a']), string-length(normalize-space(field[@id='215']/subfield[@id='a']))) = '.'">
                                <xsl:text disable-output-escaping="yes"> —</xsl:text>
                                <xsl:value-of select="normalize-space(field[@id='215']/subfield[@id='a'])"/>

                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text disable-output-escaping="yes"> —</xsl:text>
                                <xsl:value-of select="normalize-space(field[@id='215']/subfield[@id='a'])"/>
                                <xsl:text disable-output-escaping="yes">.</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>

                    <!-- определение точки в конце
             <xsl:choose>
             <xsl:when test="substring(field[@id='215']/subfield[@id='c'], string-length(field[@id='215']/subfield[@id='c'])) = '.'">

             </xsl:when>
             <xsl:otherwise>
             <xsl:text disable-output-escaping="yes">. </xsl:text>
             </xsl:otherwise>
             </xsl:choose>-->


                </xsl:otherwise>
            </xsl:choose>
            <!-- end of otherwise link -->

        </xsl:if>

        <!-- Если многотомник indicator=0 -->
        <xsl:if test="field[@id='200']/indicator[@id='1']=0"> <!-- если многотомник -->

            <!-- 700а фамилия -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='a']">
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='a']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>
            <!-- 700b инициалы -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b']">
                <xsl:choose>
                    <xsl:when
                            test="contains(field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b'], '.')">
                        <xsl:value-of
                                select="substring-before(field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b'], '.')"/>
                        <xsl:text disable-output-escaping="yes">. </xsl:text>
                        <xsl:value-of
                                select="normalize-space(substring-after(field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b'], '.'))"/>
                        <xsl:text disable-output-escaping="yes"> </xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='700']/subfield[@id='b']"/>
                        <xsl:text disable-output-escaping="yes"></xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>

            <!-- 200a основное заглавие -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']">
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='a']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>

            <!-- маркер записи - тип документа -->

            <xsl:if test="leader/type = 'a'">
                [Текст]
            </xsl:if>

            <!-- 200v номер тома -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']">
                <xsl:text disable-output-escaping="yes">:</xsl:text>
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
            </xsl:if>

            <!-- 210a город издания тома -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                <xsl:text disable-output-escaping="yes">. —</xsl:text>


                <xsl:for-each select="field[@id='461']/subfield[@id='1']/field[@id='210'][subfield[@id='a']]">
                    <xsl:for-each select="subfield[@id='a']">
                        <xsl:if test="position()>1">
                            <xsl:text disable-output-escaping="yes">;</xsl:text>
                        </xsl:if>
                        <xsl:choose>
                            <!-- если москва -->
                            <xsl:when test=".='Москва'">
                                <xsl:text disable-output-escaping="yes">М.</xsl:text>
                            </xsl:when>
                            <xsl:when test=".='Ленинград'">
                                <xsl:text disable-output-escaping="yes">Л.</xsl:text>
                            </xsl:when>
                            <xsl:when test=".='Санкт-Петербург'">
                                <xsl:text disable-output-escaping="yes">СПб.</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:if test=".">
                                    <xsl:value-of select="."/>
                                </xsl:if>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:for-each>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>

            <!-- 210c имя издательства -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='c']">
                <xsl:text disable-output-escaping="yes">:</xsl:text>
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='c']"/>
                <xsl:text disable-output-escaping="yes"></xsl:text>
            </xsl:if>

            <!-- 210d год издания -->
            <xsl:if test="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d']">
                <xsl:text disable-output-escaping="yes">,</xsl:text>
                <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
                <xsl:choose>
                    <xsl:when
                            test="substring(field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d'], string-length(field[@id='461']/subfield[@id='1']/field[@id='210']/subfield[@id='d'])) = '.'">
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text disable-output-escaping="yes">.</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>

            <!-- 215a объем -->
            <xsl:if test="field[@id='215']/subfield[@id='a']">
                <xsl:choose>
                    <xsl:when
                            test="substring(normalize-space(field[@id='215']/subfield[@id='a']), string-length(normalize-space(field[@id='215']/subfield[@id='a']))) = '.'">
                        <xsl:text disable-output-escaping="yes"> —</xsl:text>
                        <xsl:value-of select="normalize-space(field[@id='215']/subfield[@id='a'])"/>

                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text disable-output-escaping="yes"> —</xsl:text>
                        <xsl:value-of select="normalize-space(field[@id='215']/subfield[@id='a'])"/>
                        <xsl:text disable-output-escaping="yes">.</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>
        </xsl:if>
        <!-- КОНЕЦ МНОГОТОМНИКА с индикатором 0 -->

    </xsl:template>

</xsl:stylesheet>
