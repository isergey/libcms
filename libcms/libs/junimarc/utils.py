# coding=utf-8
def beautify(libcard):
    replaces = [
        (u'. :', u'.:'),
        (u', .', u'. '),
        (u'. .', u'. '),
        (u'.  .', u'. '),
        (u'— , ', u'— '),
        (u'.. ', u'. '),
        (u'..,', u'.,'),
        (u"..\n", u".\n"),
        (u"..<", u".<"),
        (u"..<", u".<"),
        (u".</a>\n", u".</a>"),
        (u".</p>\n", u".</p>"),
        (u".</a>.", u".</a>"),
        (u".</div>.", u".</div>"),
        (u".<div class=\"links\">.", u".<div class=\"links\">"),
        (u"<b></b>. ", u""),
        (u".</b>.", u".</b>"),
        (u".</p>.", u".</p>"),
        (u".</a><p></p>.", u".</a><p></p>"),
        (u".</a></div>.", u".</a></div>"),
        (u"%2B", u"+"),
    ]
    r = libcard
    for replace in replaces:
        r = r.replace(replace[0], replace[1])
    return r
