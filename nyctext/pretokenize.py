import re
'''Process to be done before tokenizing into sentences.
Transorm the text so the sentence tokenizer can break
sentences correctly.

Another alternative is to examine a wrapper for
sent_tokenize that could stitch sentence fragments
together.

'''


def do_cd(text):
    _rex_cd = re.compile(r'\s?(\d+)(n|s|e|w)(\.)?\s', re.I)
    return _rex_cd.sub('\\1 \\2 ', text)


def do_initials(text):
    _rex_initials = re.compile('(?<=[\s\.][A-Z])(\.)', re.I)
    return _rex_initials.sub(' ', text)


def do_title(text):
    _rex_reverend = re.compile('rev\.', re.I)
    return _rex_reverend.sub('Rev', text)


def do_suite(text):
    _rex_suite = re.compile('ste\.', re.I)
    return _rex_suite.sub('Suite', text)


def do_periods(text):
    _rex_periods = re.compile('(?<=[^\s\s])(\.)(?=\s)', re.I)
    return _rex_periods.sub('\\1 ', text)


def do_ordinal_indicator(text):
    '''Removes bad ordinal indicators that could be
    road(rd) or street(st)
    Transform yes:    22st -> 22 st
    Transform  no:    21st. -> 21st

    '''
    _rex_bad_ord_indic_st = re.compile('(\d+)(?<!1)(st\.?)', re.I)
    _rex_bad_ord_indic_rd = re.compile('(\d+)(?<!3)(rd\.?)', re.I)
    _rex_good_ord_indic_st = re.compile('(\d+)(?<=1)(st\.)', re.I)
    _rex_good_ord_indic_rd = re.compile('(\d+)(?<=3)(rd\.)', re.I)

    text = _rex_bad_ord_indic_st.sub('\\1 st', text)
    text = _rex_bad_ord_indic_rd.sub('\\1 rd', text)

    text = _rex_good_ord_indic_st.sub('\\1st', text)
    text = _rex_good_ord_indic_rd.sub('\\1rd', text)
    return text


def do_city_abbreviations(text):
    abr_brooklyn = re.compile('\s[\s,]*(bklyn|bkln)[\s,]', re.I)
    text = abr_brooklyn.sub(' Brooklyn ', text)
    return text


def do_occupancy_abbreviations(text):
    rex_floor = re.compile('([\s,]flr?\.?[\s\.]*)[\s,]', re.I)
    text = rex_floor.sub(' Floor ', text)
    return text


def transform(text, verbose=False):
    if verbose:
        print 'Source Text: %s' % text

    text = do_periods(text)
    if verbose:
        print '    Periods: %s' % text

    text = do_initials(text)
    if verbose:
        print '   Initials: %s' % text

    text = do_title(text)
    if verbose:
        print '   titlesub: %s' % text

    text = do_suite(text)
    if verbose:
        print '   suitesub: %s' % text

    text = do_ordinal_indicator(text)
    if verbose:
        print '  ord indic: %s' % text

    text = do_occupancy_abbreviations(text)
    if verbose:
        print 'occu abbrev: %s' % text

    text = do_city_abbreviations(text)
    if verbose:
        print '  city abbr: %s' % text

    text = do_cd(text)
    if verbose:
        print '    cd abbr: %s' % text

    return text
