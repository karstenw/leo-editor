#!/usr/bin/env python
# -*- coding: utf8 -*-
# :Copyright: © 2011 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: http://www.spdx.org/licenses/BSD-2-Clause

# :Id: $Id: punctuation_chars.py 7463 2012-06-22 19:49:51Z milde $

import sys, re
import unicodedata

# punctuation characters around inline markup
# ===========================================
#
# This module provides the lists of characters for the implementation of
# the `inline markup recognition rules`_ in the reStructuredText parser
# (states.py)
#
# .. _inline markup recognition rules:
#     ../../../docs/ref/rst/restructuredtext.html#inline-markup

# Docutils punctuation category sample strings
# --------------------------------------------
#
# The sample strings are generated by punctuation_samples() and put here
# literal to avoid the time-consuming generation with every Docutils
# run. Running this file as a standalone module checks the definitions below
# against a re-calculation.

openers = ur"""\"\'\(\<\[\{༺༼᚛⁅⁽₍〈❨❪❬❮❰❲❴⟅⟦⟨⟪⟬⟮⦃⦅⦇⦉⦋⦍⦏⦑⦓⦕⦗⧘⧚⧼⸢⸤⸦⸨〈《「『【〔〖〘〚〝〝﴾︗︵︷︹︻︽︿﹁﹃﹇﹙﹛﹝（［｛｟｢«‘“‹⸂⸄⸉⸌⸜⸠‚„»’”›⸃⸅⸊⸍⸝⸡‛‟"""
closers = ur"""\"\'\)\>\]\}༻༽᚜⁆⁾₎〉❩❫❭❯❱❳❵⟆⟧⟩⟫⟭⟯⦄⦆⦈⦊⦌⦎⦐⦒⦔⦖⦘⧙⧛⧽⸣⸥⸧⸩〉》」』】〕〗〙〛〞〟﴿︘︶︸︺︼︾﹀﹂﹄﹈﹚﹜﹞）］｝｠｣»’”›⸃⸅⸊⸍⸝⸡‛‟«‘“‹⸂⸄⸉⸌⸜⸠‚„"""

# All unit tests pass with this definition.
# original_delimiters = ur"\-\/\:֊־᐀᠆‐‑‒–—―⸗⸚〜〰゠︱︲﹘﹣－¡·¿;·՚՛՜՝՞՟։׀׃׆׳״؉؊،؍؛؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾।॥॰෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒྅࿐࿑࿒࿓࿔၊။၌၍၎၏჻፡።፣፤፥፦፧፨᙭᙮᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠇᠈᠉᠊᥄᥅᧞᧟᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᰻᰼᰽᰾᰿᱾᱿᳓‖‗†‡•‣․‥…‧‰‱′″‴‵‶‷‸※‼‽‾⁁⁂⁃⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⳹⳺⳻⳼⳾⳿⸀⸁⸆⸇⸈⸋⸎⸏⸐⸑⸒⸓⸔⸕⸖⸘⸙⸛⸞⸟⸪⸫⸬⸭⸮⸰⸱、。〃〽・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꣸꣹꣺꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꯫︐︑︒︓︔︕︖︙︰﹅﹆﹉﹊﹋﹌﹐﹑﹒﹔﹕﹖﹗﹟﹠﹡﹨﹪﹫！＂＃％＆＇＊，．／：；？＠＼｡､･𐄀𐄁𐎟𐏐𐡗𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕𐩖𐩗𐩘𐩿𐬹𐬺𐬻𐬼𐬽𐬾𐬿𑂻𑂼𑂾𑂿𑃀𑃁𒑰𒑱𒑲𒑳"
# All unit tests pass with this definition.
# delimiters = ur"\-\/\:֊־᐀᠆‐‑‒–—―⸗⸚〜〰゠︱︲﹘﹣－¡·¿;·՚՛՜՝՞՟։׀׃׆׳״؉؊،؍؛؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾।॥॰෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒྅࿐࿑࿒࿓࿔၊။၌၍၎၏჻፡።፣፤፥፦፧፨᙭᙮᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠇᠈᠉᠊᥄᥅᧞᧟᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᰻᰼᰽᰾᰿᱾᱿᳓‖‗†‡•‣․‥…‧‰‱′″‴‵‶‷‸※‼‽‾⁁⁂⁃⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⳹⳺⳻⳼⳾⳿⸀⸁⸆⸇⸈⸋⸎⸏⸐⸑⸒⸓⸔⸕⸖⸘⸙⸛⸞⸟⸪⸫⸬⸭⸮⸰⸱、。〃〽・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꣸꣹꣺꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꯫︐︑︒︓︔︕︖︙︰﹅﹆﹉﹊﹋﹌﹐﹑﹒﹔﹕﹖﹗﹟﹠﹡﹨﹪﹫！＂＃％＆＇＊，．／：；？＠＼｡､･"

# Delete redundant backslashes.
ur_delims = ur"\-/:֊־᐀᠆‐‑‒–—―⸗⸚〜〰゠︱︲﹘﹣－¡·¿;·՚՛՜՝՞՟։׀׃׆׳״؉؊،؍؛؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾।॥॰෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒྅࿐࿑࿒࿓࿔၊။၌၍၎၏჻፡።፣፤፥፦፧፨᙭᙮᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠇᠈᠉᠊᥄᥅᧞᧟᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᰻᰼᰽᰾᰿᱾᱿᳓‖‗†‡•‣․‥…‧‰‱′″‴‵‶‷‸※‼‽‾⁁⁂⁃⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⳹⳺⳻⳼⳾⳿⸀⸁⸆⸇⸈⸋⸎⸏⸐⸑⸒⸓⸔⸕⸖⸘⸙⸛⸞⸟⸪⸫⸬⸭⸮⸰⸱、。〃〽・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꣸꣹꣺꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꯫︐︑︒︓︔︕︖︙︰﹅﹆﹉﹊﹋﹌﹐﹑﹒﹔﹕﹖﹗﹟﹠﹡﹨﹪﹫！＂＃％＆＇＊，．／：；？＠＼｡､･"

# Now change ur to u, doubling the initial backslash.
delimiters = u"\\-/:֊־᐀᠆‐‑‒–—―⸗⸚〜〰゠︱︲﹘﹣－¡·¿;·՚՛՜՝՞՟։׀׃׆׳״؉؊،؍؛؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾।॥॰෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒྅࿐࿑࿒࿓࿔၊။၌၍၎၏჻፡።፣፤፥፦፧፨᙭᙮᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠇᠈᠉᠊᥄᥅᧞᧟᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᰻᰼᰽᰾᰿᱾᱿᳓‖‗†‡•‣․‥…‧‰‱′″‴‵‶‷‸※‼‽‾⁁⁂⁃⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⳹⳺⳻⳼⳾⳿⸀⸁⸆⸇⸈⸋⸎⸏⸐⸑⸒⸓⸔⸕⸖⸘⸙⸛⸞⸟⸪⸫⸬⸭⸮⸰⸱、。〃〽・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꣸꣹꣺꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꯫︐︑︒︓︔︕︖︙︰﹅﹆﹉﹊﹋﹌﹐﹑﹒﹔﹕﹖﹗﹟﹠﹡﹨﹪﹫！＂＃％＆＇＊，．／：；？＠＼｡､･"

assert ur_delims == delimiters

# assert delimiters1 == delimiters
closing_delimiters = ur"\.\,\;\!\?"

# Unicode punctuation character categories
# ----------------------------------------

unicode_punctuation_categories = {
    # 'Pc': 'Connector', # not used in Docutils inline markup recognition
    'Pd': 'Dash',
    'Ps': 'Open',
    'Pe': 'Close',
    'Pi': 'Initial quote', # may behave like Ps or Pe depending on usage
    'Pf': 'Final quote', # may behave like Ps or Pe depending on usage
    'Po': 'Other'
    }
"""Unicode character categories for punctuation"""


# generate character pattern strings
# ==================================

def unicode_charlists(categories, cp_min=0, cp_max=None):
    """Return dictionary of Unicode character lists.

    For each of the `catagories`, an item contains a list with all Unicode
    characters with `cp_min` <= code-point <= `cp_max` that belong to the
    category. (The default values check every code-point supported by Python.)
    """
    # Determine highest code point with one of the given categories
    # (may shorten the search time considerably if there are many
    # categories with not too high characters):
    if cp_max is None:
        cp_max = max(x for x in xrange(sys.maxunicode + 1)
                     if unicodedata.category(unichr(x)) in categories)
        # print cp_max # => 74867 for unicode_punctuation_categories
    charlists = {}
    for cat in categories:
        charlists[cat] = [unichr(x) for x in xrange(cp_min, cp_max+1)
                          if unicodedata.category(unichr(x)) == cat]
    return charlists


# Character categories in Docutils
# --------------------------------

def punctuation_samples():

    """Docutils punctuation category sample strings.

    Return list of sample strings for the categories "Open", "Close",
    "Delimiters" and "Closing-Delimiters" used in the `inline markup
    recognition rules`_.
    """

    # Lists with characters in Unicode punctuation character categories
    cp_min = 160 # ASCII chars have special rules for backwards compatibility
    ucharlists = unicode_charlists(unicode_punctuation_categories, cp_min)

    # match opening/closing characters
    # --------------------------------
    # Rearange the lists to ensure matching characters at the same
    # index position.

    # low quotation marks are also used as closers (e.g. in Greek)
    # move them to category Pi:
    ucharlists['Ps'].remove(u'‚') # 201A  SINGLE LOW-9 QUOTATION MARK
    ucharlists['Ps'].remove(u'„') # 201E  DOUBLE LOW-9 QUOTATION MARK
    ucharlists['Pi'] += [u'‚', u'„']

    ucharlists['Pi'].remove(u'‛') # 201B  SINGLE HIGH-REVERSED-9 QUOTATION MARK
    ucharlists['Pi'].remove(u'‟') # 201F  DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    ucharlists['Pf'] += [u'‛', u'‟']

    # 301F  LOW DOUBLE PRIME QUOTATION MARK misses the opening pendant:
    ucharlists['Ps'].insert(ucharlists['Pe'].index(u'\u301f'), u'\u301d')

    # print u''.join(ucharlists['Ps']).encode('utf8')
    # print u''.join(ucharlists['Pe']).encode('utf8')
    # print u''.join(ucharlists['Pi']).encode('utf8')
    # print u''.join(ucharlists['Pf']).encode('utf8')

    # The Docutils character categories
    # ---------------------------------
    #
    # The categorization of ASCII chars is non-standard to reduce both
    # false positives and need for escaping. (see `inline markup recognition
    # rules`_)

    # matching, allowed before markup
    openers = [re.escape('"\'(<[{')]
    for cat in ('Ps', 'Pi', 'Pf'):
        openers.extend(ucharlists[cat])

    # matching, allowed after markup
    closers = [re.escape('"\')>]}')]
    for cat in ('Pe', 'Pf', 'Pi'):
        closers.extend(ucharlists[cat])

    # non-matching, allowed on both sides
    delimiters = [re.escape('-/:')]
    for cat in ('Pd', 'Po'):
        delimiters.extend(ucharlists[cat])

    # non-matching, after markup
    closing_delimiters = [re.escape('.,;!?')]

    # # Test open/close matching:
    # for i in range(min(len(openers),len(closers))):
    #     print '%4d    %s    %s' % (i, openers[i].encode('utf8'),
    #                                closers[i].encode('utf8'))

    return [u''.join(chars)
            for chars in (openers, closers, delimiters, closing_delimiters)]


# Matching open/close quotes
# --------------------------

# Rule (5) requires determination of matching open/close pairs. However,
# the pairing of open/close quotes is ambigue due to  different typographic
# conventions in different languages.

quote_pairs = {u'\xbb': u'\xbb', # Swedish
               u'\u2018': u'\u201a', # Greek
               u'\u2019': u'\u2019', # Swedish
               u'\u201a': u'\u2018\u2019', # German, Polish
               u'\u201c': u'\u201e', # German
               u'\u201e': u'\u201c\u201d',
               u'\u201d': u'\u201d', # Swedish
               u'\u203a': u'\u203a', # Swedish
              }

def match_chars(c1, c2):
    try:
        i = openers.index(c1)
    except ValueError:  # c1 not in openers
        return False
    return c2 == closers[i] or c2 in quote_pairs.get(c1, '')




# print results
# =============

if __name__ == '__main__':

    # (re) create and compare the samples:
    (o, c, d, cd) = punctuation_samples()
    if o != openers:
        print '- openers = ur"""%s"""' % openers.encode('utf8')
        print '+ openers = ur"""%s"""' % o.encode('utf8')
    if c != closers:
        print '- closers = ur"""%s"""' % closers.encode('utf8')
        print '+ closers = ur"""%s"""' % c.encode('utf8')
    if d != delimiters:
        print '- delimiters = ur"%s"' % delimiters.encode('utf8')
        print '+ delimiters = ur"%s"' % d.encode('utf8')
    if cd != closing_delimiters:
        print '- closing_delimiters = ur"%s"' % closing_delimiters.encode('utf8')
        print '+ closing_delimiters = ur"%s"' % cd.encode('utf8')

    # # test prints
    # print 'openers = ', repr(openers)
    # print 'closers = ', repr(closers)
    # print 'delimiters = ', repr(delimiters)
    # print 'closing_delimiters = ', repr(closing_delimiters)

    # ucharlists = unicode_charlists(unicode_punctuation_categories)
    # for cat, chars in ucharlists.items():
    #     # print cat, chars
    #     # compact output (visible with a comprehensive font):
    #     print (u":%s: %s" % (cat, u''.join(chars))).encode('utf8')
