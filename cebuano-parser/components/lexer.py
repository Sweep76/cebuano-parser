###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more inpput left for lexical analysis
CONJ              = 'CONJ'
DET               = 'DET'
DET_PLURAL        = 'DET_PLURAL'
PART              = 'PART'
PRON_DEM          = 'PRON_DEM'
PRON_POS          = 'PRON_POS'
PRON_POS_NG       = 'PRON_POS_NG'
PRON_POS_N        = 'PRON_POS_N'
PRON_PER          = 'PRON_PER'
NOUN              = 'NOUN'
PREP              = 'PREP'
VERB              = 'VERB'
VERB_EXT          = 'VERB_EXT'
ADJ               = 'ADJ'
ADV_SPE           = 'ADV_SPE'
ADV               = 'ADV'
PART_PLURAL       = 'PART_PLURAL'
PRON_PLURAL       = 'PRON_PLURAL'
PRON_PER_PLURAL   = 'PRON_PER_PLURAL'
PRON_POS_PLURAL   = 'PRON_POS_PLURAL'
PRON_POS_PLURAL_NG = 'PRON_POS_PLURAL_NG'
PRON_POS_PLURAL_N = 'PRON_POS_PLURAL_N'
VERB_PREF_PRES    = 'VERB_PREF_PRES'
VERB_PREF_PAST    = 'VERB_PREF_PAST'
VERB_PREF_FUT     = 'VERB_PREF_FUT'
VERB_SUFF_PRES    = 'VERB_SUFF_PRES'
VERB_SUFF_PAST    = 'VERB_SUFF_PAST'
VERB_SUFF_FUT     = 'VERB_SUFF_FUT'
NUM               = 'NUM'
MGA               = 'MGA'
KA                = 'KA'
IKA               = 'IKA'
NGA               = 'NGA'
CLIT_Y            = 'CLIT_Y'
CLIT_NG           = 'CLIT_NG'
DILI              = 'DILI'
I                 = 'I'
A                 = 'A'
HA                = 'HA'
UG                = 'UG'
HI                = 'HI'
TIME_FUT          = 'TIME_FUT'
TIME_PAST         = 'TIME_PAST'
TIME_PRES         = 'TIME_PRES'
NIAGING           = 'NIAGING'
SUNOD             = 'SUNOD'
POS_LINK          = 'POS_LINK'
KARONG            = 'KARONG'
TIME_NOUN         = 'TIME_NOUN'
TIME_NOUN_A       = 'TIME_NOUN_A'
TIME              = 'TIME'
DASH              = 'DASH'
COMMA             = 'COMMA'
MONTH             = 'MONTH'
DAY               = 'DAY'
TIME_OF_DAY       = 'TIME_OF_DAY'
IMPERATIVE        = 'IMPERATIVE'
YEAR              = 'YEAR'
INT               = 'INT'
HOUR              = 'HOUR'
ANG               = 'ANG'
EOF               = 'EOF'
PLACE             = 'PLACE'
branches             =[]
inCount           =0
errors            =[]

class Error(object):
    def __init__(self, error, fix, evalue, svalue=None):
        self.error = error
        self.correct = fix
        self.right_value = svalue
        self.wrong_value = evalue

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(NUMBER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

PRESENT_PREFIX = ['nag', 'na', 'gi', 'i', 'naga', 'nang']
PAST_PREFIX = ['ni', 'nag', 'naka', 'na', 'gi', 'naga', 'nang']
FUTURE_PREFIX = ['mo', 'mag', 'maka', 'ma', 'i', 'maga', 'mang']
PRESENT_SUFFIX = ['mo', 'mag', 'maka', 'ma', 'i']
PAST_SUFFIX = ["an"]
MONTHS = ["enero", "pebrero", "marso", "abril", "mayo", "hunyo", "hulyo", "agosto", "septiyembre", "oktubre", "nubiyembre", "disyembre"]
HOURS = ["uno", "dos", "tres", "kwatro", "singko", "sais", "siete", "otso", "nuwebe", "diyes", "onse", "dose"]
TIMES_OF_DAY = ["ka-adlawon", "buntag", "udto", "hapon" "gabi-i"]
FUTURE_SUFFIX = ["on", "hon", "an"]
INTER = ["unsa", "kinsa", "ngano", "kanusa", "asa", "hain", "diin" , "kon", "samtang", "pila", "ginusa", "unsaon", "tagpila"]
PREPS = ["sa", "kang", "kay", "batok", "de", "gawas", "gikan","imbes","kapin","minos","mura",
         "ngadto","nganha","para","puyra","pwera","sulod","supak","tungod","tupad","uban",
         "ubos"]
TIME_NOUNS = ["adlaw", "tuig", "semana"]
TIME_NOUNS_A = ["adlawa", "tuiga", "semanaha"]
TIMES = ["kagahapon", "karon", "ugma", "kaganina"]
PRON_DEMS = ["kiri", "kini", "kana", "kadto", "niiri", "niini", "niani", "niari", "niana", "niadto" ]
PLURAL_DETS = ["sina", "mga"]
DETS = ["sa"]
POS_LINKS = ['ni', 'sa']
PRON_POS_SINGS = ["ako", "imo", "iya", "nako", "nimo", "niya"]
PRON_POS_N_SINGS = ["nako", "nimo", "niya"]
PRON_PER_SINGS = ["ikaw", "ka", "siya", "ko"]+PRON_POS_SINGS
PRON_POS_PLURALS = ["amo", "ato", "inyo", "ila", "namo", "nato", "ninyo", "nila"]
PRON_POS_N_PLURALS = ["namo", "nato", "ninyo", "nila"]
PRON_PER_PLURALS = ["kami", "kita", "kamo", "sila", "ta", "mi"]+PRON_POS_PLURALS
PRON_POS_SINGS_NG = [pro+"ng" for pro in PRON_POS_SINGS]
ADV_SPECS = ['na', 'pa', 'man', 'ba']
PRON_POS_PLURALS_NG = [pro+"ng" for pro in PRON_POS_PLURALS]
RESERVED_WORDS = {
    'MGA': Token([MGA], 'mga'),
    'NGA': Token([NGA], 'nga'),
    'IKA-': Token([IKA], 'ika-'),
    'NIAGING': Token([NIAGING], 'niaging'),
    'SUNOD': Token([SUNOD], 'sunod'),
    'KARONG': Token([KARONG], 'karong')
}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self, add=0):
        peek_pos = self.pos + 1 +add
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token([NUM], int(result))

    def general(self, given):
        ret = []
        if given in MONTHS:
            ret += [MONTH]
        if given in HOURS:
            ret += [HOUR]
        if given in TIMES_OF_DAY:
            ret += [TIME_OF_DAY]
        if given in DETS:
            ret += [DET]
        if given in INTER:
            ret += [INT]
        if given in PREPS:
            ret += [PREP]
        if given in TIME_NOUNS:
            ret += [TIME_NOUN]
        if given in POS_LINKS:
            ret += [POS_LINK]
        if given in TIME_NOUNS_A:
            ret += [TIME_NOUN_A]
        if given in TIMES:
            ret += [TIME]
        if given in PRON_DEMS:
            ret += [PRON_DEM]
        if given in ADV_SPECS:
            ret += [ADV_SPE]
        if given in PLURAL_DETS:
            ret += [DET_PLURAL]
        if given in PRON_PER_SINGS:
            ret += [PRON_PER]
        if given in PRON_PER_PLURALS:
            ret += [PRON_PER_PLURAL]
        if given in PRON_POS_SINGS:
            ret += [PRON_POS]
        if given in PRON_POS_PLURALS:
            ret += [PRON_POS_PLURAL]
        if given in PRON_POS_N_SINGS:
            ret += [PRON_POS_N]
        if given in PRON_POS_N_PLURALS:
            ret += [PRON_POS_PLURAL_N]
        if given in PRON_POS_SINGS_NG:
            ret += [PRON_POS_NG]
        if given in PRON_POS_PLURALS_NG:
            ret += [PRON_POS_PLURAL_NG]
        picked = stemmer.stem_word(given, as_object=True).root
        types = dictionary.search(picked)
        if types == None:
            types = [NOUN]
        ret += types
        return Token(ret, given)

    def word(self):
        """Handle words, reserved or not"""
        result = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == "-"):
            result += self.current_char
            self.advance()
        return RESERVED_WORDS.get(result.upper(), self.general(result))

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self.word()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ",":
                self.advance()
                return Token([COMMA], ",")

            if self.current_char == "'" and self.peek() == 'y':
                self.advance()
                self.advance()
                return Token([CLIT_Y], "'y")

            if self.current_char == "'" and self.peek() == 'n' and self.peek(1) == 'g':
                self.advance()
                self.advance()
                self.advance()
                return Token([CLIT_NG], "'ng")

            self.error()

        return Token([EOF], None)