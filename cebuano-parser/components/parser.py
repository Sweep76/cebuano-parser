###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################
class AST(object):
    pass

class SentencePart(AST):
    def __init__(self, left, conj=None, right=None):
        self.left = left
        self.conj = conj
        self.right = right

class NounPhrasePart(AST):
    def __init__(self, left, conj=None, right=None):
        self.left = left
        self.conj = conj
        self.right = right

class Sentence(AST):
    def __init__(self, pred, nounp=None):
        self.pred_phrase = pred
        self.noun_phrase = nounp

class PredPhrase(AST):
    def __init__(self, verbph, endadv, pred=None, midadv=None):
        self.pred = pred
        self.verb_phr = verbph
        self.adv = endadv
        self.mid_adv = midadv

class Date(AST):
    def __init__(self, kind, month, day, com=None, year=None, extra=None, sa=None):
        self.type = kind
        self.month = month
        self.day = day
        self.comma = com
        self.year = year
        self.extra = extra
        self.sa = sa

class Predicate(AST):
    def __init__(self, element):
        self.content = element

class Descriptive(AST):
    def __init__(self, element):
        self.content = element

class Adverb(AST):
    def __init__(self, element, add=None):
        self.content = element
        self.addition = add

class Time(AST):
    def __init__(self, time, num=None, day=None):
        self.noun = time
        self.number = num
        self.day = day

class NounPhrase(AST):
    def __init__(self, noun, prep, nga=None, other=None):
        self.complex_noun = noun
        self.prep_phrase = prep
        self.nga = nga
        self.clause = other

class VerbPhrase(AST):
    def __init__(self, verb, opt):
        self.complex_verb = verb
        self.opt = opt

class PrepPhrase(AST):
    def __init__(self, prep, second, noun, adv=None, extra=None):
        self.prep = prep
        self.second_prep = second
        self.noun_phrase = noun
        self.adv = adv
        self.extra = extra

class Adjective(AST):
    def __init__(self, adj, nga, ng=None):
        self.adjectives = adj
        self.nga = nga
        self.clit_ng = ng

class Word(AST):
    def __init__(self, content, type):
        self.content = content
        self.type = type

class Possess(AST):
    def __init__(self, type, pos, noun=None):
        self.type = type
        self.link = pos
        self.noun = noun

class AdjOrd(AST):
    def __init__(self, mark, dash, num, nga):
        self.marker = mark
        self.dash = dash
        self.number = num
        self.nga = nga

class AdjNum(AST):
    def __init__(self, num, ka, conj=None):
        self.number = num
        self.ka = ka
        self.conj = conj

class Noun(AST):
    def __init__(self, type, adj, noun, poss, mga=None):
        self.type = type
        self.adjective = adj
        self.nouns = noun
        self.possess = poss
        self.mga = mga

class CompoundNoun(AST):
    def __init__(self, kind, noun, other=None, extra=None):
        self.type = kind
        self.other_phrase = other
        self.noun_phrase = noun
        self.extra = extra
        
class NounPhraseSingularPlural(AST):
    def __init__(self, type, noun, begin=None, ordinal=None, num=None, mga=None, pos=None, extra=None):
        self.type = type
        self.noun_sp = noun
        self.start = begin
        self.pos = pos
        self.ordinal = ordinal
        self.number = num
        self.mga = mga
        self.extra = extra

class DemPronoun(AST):
    def __init__(self, type, dem, clit=None, ordinal=None, num=None, mga=None):
        self.type = type
        self.pronoun = dem
        self.clit = clit
        self.ordinal = ordinal
        self.number = num
        self.mga = mga
        
class VerbComplex(AST):
    def __init__(self, prefix, root, suffix, extra=None):
        self.prefix = prefix
        self.root = root
        self.suffix = suffix
        self.extra = extra

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        #print (self.current_token.type+" "+token_type)
        #print ("eee")
        if token_type in self.current_token.type:
            self.current_token = self.lexer.get_next_token()
        else:
            errors.append(Error("Wrong syntax: "+", ".join(self.current_token.type), token_type, self.current_token.value))

    def contain(self, words):
        result = False
        for x in self.current_token.type:
            if x in words:
                result = True
                break
        return result

    def sentence_part(self):
        """sentence_part : sentence
                         | sentence (CONJ|COMMA) sentence_part
        """
        left = self.sentence()

        if CONJ in self.current_token.type:
            conjunct = self.current_token
            self.eat(CONJ)
            return self.sentence_part_extra(left, conj)
        elif COMMA in self.current_token.type:
            conjunct = self.current_token
            self.eat(COMMA)
            return self.sentence_part_extra(left, conj)
        else:
            return SentencePart(left)

    def sentence_part_extra(self, left, conj):
        right=self.sentence_part()
        return SentencePart(left, Word(conj, CONJ), right)

    def sentence(self):
        """sentence : pred_phrase (noun_phrase_part)?"""
        pred_phrase = self.pred_phrase()
        noun_phrase = self.noun_phrase_part()
        if pred_phrase.verb_phr is not None:
            pref = pred_phrase.verb_phr.complex_verb.prefix.content
            noun = pred_phrase.verb_phr.opt if pred_phrase.verb_phr.opt is not None else noun_phrase
            if pref is not None and pref in ['nang', 'mang'] and noun.left is not None and noun.left.complex_noun.type == "Singular" and noun.conj is None:
                errors.append(Error("Using a plural prefix for a singular noun", "Use a singular prefix", pref+"-", ['nag-', 'naga-', 'mag-', 'maga-']))
            elif pref is not None and pref in ['nag', 'naga', 'mag', 'maga'] and noun.left is not None and (noun.left.complex_noun.type == "Plural" or noun.conj is not None):
                errors.append(Error("Using a singular prefix for a plural noun", "Use a plural prefix", pref+"-", ['nang-', 'mang-']))
        return Sentence(pred_phrase, noun_phrase)

    def conditions(self, conds):
        return True in conds

    def pred_phrase(self):
        """pred_phrase : verb_phrase (adverb)?
                       | predicate (adverb)? verb_phrase (adverb)?
        """
        if VERB in self.current_token.type:
            verb_phrase = self.verb_phrase()
            end_adv = self.adverb()
            self.tenses(verb_phrase, end_adv)
            return PredPhrase(verb_phrase, end_adv)
        else:
            predicate = self.predicate()
            mid_adv = self.adverb()
            verb_phrase = self.verb_phrase() if VERB in self.current_token.type else None
            end_adv = self.adverb()
            self.tenses(verb_phrase, end_adv, mid_adv)
            return PredPhrase(verb_phrase, end_adv, predicate, mid_adv)


    def tenses_condition(self, given, one, two, root):
        words_p = words_s = correct = None
        if given in [NIAGING.lower(), 'kaganina', 'kagahapon']:
            words_p = PAST_PREFIX
            words_s = PAST_SUFFIX
            correct = "PAST"
        elif given in [KARONG.lower(), 'karon']:
            words_p = PRESENT_PREFIX
            words_s = PRESENT_SUFFIX
            correct = "PRESENT"
        elif given in [SUNOD.lower(), 'ugma']:
            words_p = FUTURE_PREFIX
            words_s = FUTURE_SUFFIX
            correct = "FUTURE"
        if (one.content is not None and one.content not in words_p) and two.content is None:
            errors.append(Error(one.type+" from root "+root, correct+"_PREFIX", one.content, words_p))
        elif one.content is None and (two.content is not None and words_s in suff):
            errors.append(Error(two.type+" from root "+root, correct+"_SUFFIX", two.content, words_s))
        elif one.content is not None and two.content is not None:
            if one.content not in words_p:
                errors.append(Error(one.type+" from root "+root, correct+"_PREFIX", one.content, words_p))
            if two.content not in words_s:
                errors.append(Error(two.type+" from root "+root, correct+"_SUFFIX", two.content, words_s))
                        
    def tenses(self, verb, end, mid=None):
        if verb is not None:
            prefix = verb.complex_verb.prefix
            suffix = verb.complex_verb.suffix
            if end is not None and type(end.content) == Time:
                noun = end.content.noun.content if type(end.content.noun) != list else end.content.noun[0].content
                if HOUR not in noun.type:
                    self.tenses_condition(noun.value, prefix, suffix, verb.complex_verb.root.content.value)
            elif end is not None and type(end.addition) == Time:
                noun = end.addition.noun.content if type(end.addition.noun) != list else end.addition.noun[0].content
                if HOUR not in noun.type:
                    self.tenses_condition(noun.value, prefix, suffix,  verb.complex_verb.root.content.value)

    def verb_phrase(self):
        """verb_phrase : verb_complex 
                       | verb_complex noun_phrase_part
                       | verb_complex prep_phrase
        """
        verb = self.verb_complex()
        end = None
        if self.contain([DET, PRON_POS, PRON_POS_NG, PRON_POS_PLURAL_NG, PRON_PER, DET_PLURAL, PRON_POS_PLURAL, PRON_PER_PLURAL, PRON_DEM, IKA, NUM, NOUN, MONTH]) or self.current_token.value == 'ka':
            end = self.noun_phrase_part()
        elif PREP in self.current_token.type:
            end = self.prep_phrase()
        return VerbPhrase(verb, end)

    def verb_complex(self):
        """verb_complex : (verb_prefix)? VERB (verb_suffix)?
        """
        verb = self.current_token
        self.eat(VERB)
        word = stemmer.stem_word(verb.value, as_object=True)
        verb.value = word.root
        pref_tense = []
        suff_tense = []
        if word.prefix in PAST_PREFIX:
            pref_tense.append("PAST_PREFIX")
        if word.prefix in FUTURE_PREFIX:
            pref_tense.append("FUTURE_PREFIX")
        if word.prefix == 'pag':
            pref_tense.append(IMPERATIVE)
        if word.prefix in PRESENT_PREFIX:
            pref_tense.append("PRESENT_PREFIX")
        if word.suffix in PAST_SUFFIX:
            suff_tense.append("PAST_SUFFIX")
        if word.suffix in FUTURE_SUFFIX:
            suff_tense.append("FUTURE_SUFFIX")
        if word.suffix in PRESENT_SUFFIX:
            suff_tense.append("PRESENT_SUFFIX")
        suff = ", ".join(suff_tense) if len(suff_tense)>0 else "SUFFIX"
        pre = ", ".join(pref_tense) if len(pref_tense)>0 else "PREFIX"
        if CLIT_Y in self.current_token.type:
            clit = self.current_token
            self.eat(CLIT_Y)
            return VerbComplex(Word(word.prefix, pre), Word(verb, VERB), Word(word.suffix, suff), Word(clit, CLIT_Y))
        else:
            return VerbComplex(Word(word.prefix, pre), Word(verb, VERB), Word(word.suffix, suff))

    def predicate(self):
        """ predicate : descriptive
                      | noun_phrase
                      | prep_phrase
                      | INT
                      | empty
        """
        if self.contain([DET, PRON_DEM, PRON_POS, PRON_POS_NG, PRON_POS_PLURAL_NG, PRON_PER, DET_PLURAL, PRON_POS_PLURAL, PRON_PER_PLURAL, IKA, NUM, ADJ, KA, NOUN, MONTH]):
            thing = element = self.noun_phrase_part()
        elif self.contain([PLACE, ADJ, ADV, ADV_SPE]):
            thing = element = self.descriptive()
        elif PREP in self.current_token.type:
            thing = element = self.prep_phrase()
        elif INT in self.current_token.type:
            element = self.current_token
            self.eat(INT)
            thing = Word(element, INT)
        else:
            thing = None
        return Predicate(thing)

    def descriptive(self):
        """ descriptive : ADJ
                        | adverb
        """
        if ADJ in self.current_token.type:
            element = self.current_token
            self.eat(ADJ)
            thing = Word(element, ADJ)
        elif self.contain ([PLACE, ADV, ADV_SPE]):
            thing = element = self.adverb()
        return Descriptive(thing)

    def adverb(self):
        """ adverb : PLACE (time)?
                   | time (ADV_SPE)?
                   | ADV_SPE
                   | ADV
                   | alas time
                   | DILI (ADV_SPE)?
                   | empty
        """
        if PLACE in self.current_token.type:
            place = self.current_token
            self.eat(PLACE)
            if self.contain([TIME, NIAGING, SUNOD, KARONG]):
                time = self.time()
                return Adverb(Word(place, PLACE), time)
            else:
                return Adverb(Word(place, PLACE))
        elif ADV_SPE in self.current_token.type:
            element = self.current_token
            self.eat(ADV_SPE)
            return Adverb(Word(element, ADV_SPE))
        elif self.contain([TIME, NIAGING, SUNOD, KARONG, HOUR]):
            element = self.time()
            if ADV_SPE in self.current_token.type:
                opt = self.current_token
                eat(ADV_SPE)
                return Adverb(element, Word(opt, ADV_SPE))
            else:
                return Adverb(element)
        elif ADV in self.current_token.type and self.current_token.value == 'alas':
            element = self.current_token
            self.eat(ADV)
            time = self.time()
            return Adverb(Word(element, ADV), time)
        elif ADV in self.current_token.type:
            element = self.current_token
            self.eat(ADV)
            return Adverb(Word(element, ADV))
        elif ADV in self.current_token.type and self.current_token.value == 'dili':
            element = self.current_token
            self.eat(ADV)
            if ADV_SPE in self.current_token.type:
                opt = self.current_token
                eat(ADV_SPE)
                return Adverb(Word(element, ADV), Word(opt, ADV_SPE))
            else:
                return Adverb(Word(element, ADV))
        else:
            return None

    def time(self):
        """ time : TIME
                 | NIAGING (adj_num)? TIME_NOUN
                 | SUNOD NGA (adj_num)? TIME_NOUN
                 | KARONG TIME_NOUN_A
                 | HOUR sa TIME_OF_DAY
        """
        if TIME in self.current_token.type:
            time = self.current_token
            self.eat(TIME)
            return Time(Word(time, TIME))
        elif NIAGING in self.current_token.type:
            time = self.current_token
            self.eat(NIAGING)
            num = self.adj_num()
            noun = self.current_token
            self.eat(TIME_NOUN)
            return Time(Word(time, NIAGING), num, Word(noun, TIME_NOUN))
        elif SUNOD in self.current_token.type:
            times = []
            times.append(Word(self.current_token, SUNOD))
            self.eat(SUNOD)
            times.append(Word(self.current_token, NGA))
            self.eat(NGA)
            num = self.adj_num()
            noun = self.current_token
            self.eat(TIME_NOUN)
            return Time(times, num, Word(noun, TIME_NOUN))
        elif KARONG in self.current_token.type:
            time = self.current_token
            self.eat(KARONG)
            noun = self.current_token
            self.eat(TIME_NOUN_A)
            return Time(Word(time, KARONG), day=Word(noun, TIME_NOUN_A))
        elif HOUR in self.current_token.type:
            time = self.current_token
            self.eat(HOUR)
            if self.current_token.value != 'sa':
                errors.append(Error('Preposition is not sa', "Preposition should be sa", self.current_token.value, ['sa']))
                sa = None
            else:
                sa = Word(self.current_token, PREP)
                self.eat(PREP)
            day = self.current_token
            self.eat(TIME_OF_DAY)
            if time.value in ["uno", "dos", "tres", "kwatro", "singko"] and day.value not in ["ka-adlawon", "hapon"] :
                corr = ["ka-adlawon", "hapon"]
                errors.append(Error('Wrong part of day for a particular hour', "Should be "+", or ".join(corr), day.value))
            if time.value in ["sais", "siete", "otso", "nuwebe", "diyes", "onse"] and day.value not in ["gabi-i", "buntag"]:
                corr = ["gabi-i", "buntag"]
                errors.append(Error('Wrong part of day for a particular hour', "Should be "+", or ".join(corr), day.value))
            if time.value == "dose" and day.value != "udto":
                errors.append(Error('Wrong part of day for a particular hour', "Should be udto", day.value, ['udto']))
            return Time([Word(time, HOUR), sa], day=Word(day, TIME_OF_DAY))

    def prep_phrase(self):
        """ prep_phrase : PREP (PREP)? noun_phrase_part (ADV_SPE)? (prep_phrase)?
                        | empty
        """
        if PREP in self.current_token.type:
            prep = self.current_token
            self.eat(PREP)
            return self.prep_phrase_add(prep)
        else:
            return None

    def prep_phrase_add(self, prep):
        if PREP in self.current_token.type:
            second = self.current_token
            self.eat(PREP)
        else:
            second = None
        noun_phrase = self.noun_phrase_part()
        if noun_phrase is None:
            errors.append(Error("No noun phrase after preposition; type of speech found: "+' '.join(self.current_token.type),
                                "Must be a noun phrase after preposition", self.current_token.value))
        if ADV_SPE in self.current_token.type:
            adv = self.current_token
            self.eat(ADV_SPE)
        else:
            adv = None
        if PREP in self.current_token.type:
            extra = self.prep_phrase()
            return PrepPhrase(Word(prep, PREP), Word(second, PREP), noun_phrase, Word(adv, ADV_SPE), extra)
        else:
            return PrepPhrase(Word(prep, PREP), Word(second, PREP), noun_phrase, adv)

    def date(self):
        """date : MONTH DAY (COMMA YEAR)?
                | IKA DASH DAY sa MONTH (COMMA YEAR)?
        """
        if MONTH in self.current_token.type:
            month = self.current_token
            self.eat(MONTH)
            day = self.current_token
            self.eat(NUM)
            if COMMA in self.current_token.type:
                com = self.current_token
                self.eat(COMMA)
                year = self.current_token
                self.eat(NUM)
                self.date_condition(month.value, day.value, year.value)
                return Date("English", Word(month, MONTH), Word(day, DAY), Word(com, COMMA), Word(year, YEAR))
            else:
                self.date_condition(month.value, day.value)
                return Date("English", Word(month, MONTH), Word(day, DAY))

    def date_spanish(self, one, two, day):
        one.content.value = one.content.value[:-1]
        if PREP in self.current_token.type and self.current_token.value == 'sa':
            sa = self.current_token
            self.eat(PREP)
        else:
            sa = None
            errors.append(Error("Misuse of preposition", "Use preposition sa", self.current_token.value))
        ex = [one, two]
        month = self.current_token
        self.eat(MONTH)
        if COMMA in self.current_token.type:
            com = self.current_token
            self.eat(COMMA)
            year = self.current_token
            self.eat(NUM)
            self.date_condition(month.value, day.value, year.value)
            return Date("Spanish", Word(month, MONTH), Word(day, DAY), Word(com, COMMA), Word(year, YEAR), ex, Word(sa, PREP))
        else:
            self.date_condition(month.value, day.value)
            return Date("Spanish", Word(month, MONTH), Word(day, DAY), extra=ex, sa=Word(sa, PREP))

    def leap_year(self, year):
        if (year % 4) == 0:
           if (year % 100) == 0:
               if (year % 400) == 0:
                   return True
               else:
                   return False
           else:
               return True
        else:
           return False
        
    def date_condition(self, month, day, year=None):
        if month in ['enero', 'marso', 'mayo', 'hulyo', 'agosto', "oktubre", "disyembre"] and day not in range(1, 32):
            errors.append(Error("Way beyond the number of dates for "+month, "Should be between 1 and 31", day))
        elif month in ["abril", "hunyo", "septiyembre", "nubiyembre"] and day not in range(1, 31):
            errors.append(Error("Way beyond the number of dates for "+month, "Should be between 1 and 30", day))
        elif month == "pebrero" and day not in range(1, 30) and year is not None and self.leap_year(year) == True:
            errors.append(Error("Way beyond the number of dates for "+month, "Should be between 1 and 29 in a leap year", day))
        elif month == "pebrero" and day not in range(1, 29) and year is not None and self.leap_year(year) == False:
            errors.append(Error("Way beyond the number of dates for "+month, "Should be between 1 and 28", day))

    def noun_phrase_part(self):
        """noun_phrase_part : noun_phrase
                            | noun_phrase COMMA noun_phrase_part
                            | noun_phrase CONJ noun_phrase
        """
        left = self.noun_phrase()
        if COMMA in self.current_token.type:
            conjunct = self.current_token
            self.eat(COMMA)
            right=self.noun_phrase_part()
            return NounPhrasePart(left, Word(conjunct, COMMA), right)
        elif CONJ in self.current_token.type:
            conjunct = self.current_token
            self.eat(CONJ)
            right=self.noun_phrase()
            return NounPhrasePart(left, Word(conjunct, CONJ), right)
        else:
            return NounPhrasePart(left)

    def noun_phrase_extras(self, ordinal=None):
        number = self.adj_num()
        if MGA in self.current_token.type:
            noun = self.noun_plural()
            return NounPhraseSingularPlural("Plural", noun, None, ordinal, number)
        else:
            noun = self.noun_singular()
            return NounPhraseSingularPlural("Singular", noun, None, ordinal, number)
        
    def noun_phrase(self):
        """noun_phrase : (noun_phrase_singular | noun_phrase_plural | dem_pron | noun_phrase_ang) (NGA sentence)? (prep_phrase)?
                       | date
                       | number
                       | empty
        """
        if IKA in self.current_token.type:
            ika=Word(self.current_token, IKA)
            self.eat(IKA)
            dash=Word(Token([DASH], "-"), DASH)
            number = self.current_token
            self.eat(NUM)
            if NGA in self.current_token.type:
                nga = self.current_token
                self.eat(NGA)
                adj = AdjOrd(ika, dash, Word(number, NUM), Word(nga, NGA))
                if self.contain([KA, NUM, ADJ]):
                    return self.noun_phrase_extras(adj)
            else:
                return self.date_spanish(ika, dash, number)
        elif MONTH in self.current_token.type:
            return self.date()
        elif DET in self.current_token.type and self.current_token.value == 'ang':
            noun = self.noun_phrase_ang()
            return self.noun_prep_phrase_nga(noun)
        elif self.contain([KA, NUM, ADJ]):
            return self.noun_phrase_extras()
        elif self.contain([DET, PRON_POS, PRON_PER, NOUN, PRON_POS_NG]):
            noun = self.noun_phrase_singular()
            return self.noun_prep_phrase_nga(noun)
        elif self.contain([DET_PLURAL, PRON_POS_PLURAL, PRON_POS_PLURAL_NG, PRON_PER_PLURAL, MGA]):
            noun = self.noun_phrase_plural()
            return self.noun_prep_phrase_nga(noun)
        elif PRON_DEM in self.current_token.type:
            noun = self.dem_pron()
            return self.noun_prep_phrase_nga(noun)
        else:
            return None

    def noun_prep_phrase_nga(self, noun):
        if NGA in self.current_token.type:
            nga = Word(self.current_token, NGA)
            self.eat(NGA)
            other = self.sentence()
        else:
            nga = other = None
        prep_phrase = self.prep_phrase() if PREP in self.current_token.type else None
        return NounPhrase(noun, prep_phrase, nga, other)

    def noun_phrase_singular(self):
        """noun_phrase_singular : (DET)? (adj_ord)? (adj_num)? noun_singular
                                | PRON_PER (CLIT_Y)?
                                | PRON_POS_NG (noun_singular|noun_plural)
        """
        if PRON_PER in self.current_token.type:
            personal = self.current_token
            self.eat(PRON_PER)
            if CLIT_Y in self.current_token.type:
                clit = Word(self.current_token, CLIT_Y)
                self.eat(CLIT_Y)
            else:
                clit = None
            return NounPhraseSingularPlural("Singular", Word(personal, PRON_PER), extra=clit)
        elif PRON_POS_NG in self.current_token.type:
            pos = self.current_token
            self.eat(PRON_POS_NG)
            noun = self.noun_plural() if MGA in self.current_token.type else self.noun_singular()
            return NounPhraseSingularPlural("Singular", noun, Word(pos, PRON_POS_NG))
        else:
            if DET in self.current_token.type:
                det = self.current_token
                self.eat(DET)
            else:
                det = None
            ordinal = self.adj_ord() if IKA in self.current_token.type else None
            number = self.adj_num()
            noun = self.noun_singular()
            return NounPhraseSingularPlural("Singular", noun, Word(det, DET), ordinal, number)

    def noun_phrase_plural(self):
        """noun_phrase_plural : (DET_PLURAL)? (adj_ord)? (adj_num)? noun_plural
                              | PRON_PER_PLURAL (CLIT_Y)?
                              | PRON_POS_PLURAL_NG (noun_singular|noun_plural)
        """
        if PRON_PER_PLURAL in self.current_token.type:
            personal = self.current_token
            self.eat(PRON_PER_PLURAL)
            if CLIT_Y in self.current_token.type:
                clit = Word(self.current_token, CLIT_Y)
                self.eat(CLIT_Y)
            else:
                clit = None
            return NounPhraseSingularPlural("Plural", Word(personal, PRON_PER_PLURAL), extra=clit)
        elif PRON_POS_PLURAL_NG in self.current_token.type:
            pos = self.current_token
            self.eat(PRON_POS_PLURAL_NG)
            noun = self.noun_plural() if MGA in self.current_token.type else self.noun_singular()
            return NounPhraseSingularPlural("Plural", noun, Word(pos, PRON_POS_PLURAL_NG))
        else:
            if DET_PLURAL in self.current_token.type:
                det = self.current_token
                self.eat(DET_PLURAL)
            else:
                det = None
            ordinal = self.adj_ord() if IKA in self.current_token.type else None
            number = self.adj_num()
            noun = self.noun_plural(det)
            return NounPhraseSingularPlural("Plural", noun, Word(det, DET_PLURAL), ordinal, number)

    def dem_pron(self):
        """dem_pron : PRON_DEM (CLIT_NG (adj_ord)? (adj_num)? (noun_singular | noun_plural))?
        """
        dem = self.current_token
        self.eat(PRON_DEM)
        if CLIT_NG in self.current_token.type:
            clit = self.current_token
            self.eat(CLIT_NG)
            ordinal = self.adj_ord() if IKA in self.current_token.type else None
            number = self.adj_num()
            if MGA in self.current_token.type:
                noun = self.noun_plural()
                return DemPronoun("Plural", Word(dem, PRON_DEM), Word(clit, CLIT_NG), ordinal, number, noun)
            else:
                noun = self.noun_singular()
                return DemPronoun("Singular", Word(dem, PRON_DEM), Word(clit, CLIT_NG), ordinal, number, noun)
        else:
            return DemPronoun("", Word(dem, PRON_DEM))

    def noun_phrase_ang(self):
        """noun_phrase_ang : ANG (PRON_POS_NG)? (adj_ord)? (adj_num)? (noun_singular|noun_plural) 
                           | ANG (PRON_POS_PLURAL_NG)? (adj_ord)? (adj_num)? (noun_singular|noun_plural) 
        """
        ang = self.current_token
        self.eat(DET)
        poss = None
        if PRON_POS_NG in self.current_token.type:
            poss = self.current_token
            self.eat(PRON_POS_NG)
        elif PRON_POS_PLURAL_NG in self.current_token.type:
            poss = self.current_token
            self.eat(PRON_POS_PLURAL_NG)
        ordinal = self.adj_ord() if IKA in self.current_token.type else None
        number = self.adj_num() if NUM in self.current_token.type or self.current_token.value == 'ka' else None
        if MGA in self.current_token.type:
            noun = self.noun_plural()
            return NounPhraseSingularPlural("Plural", noun, Word(ang, DET), ordinal, number, pos=Word(poss, PRON_POS_PLURAL_NG))
        else:
            noun = self.noun_singular()
            return NounPhraseSingularPlural("Singular", noun, Word(ang, DET), ordinal, number, pos=Word(poss, PRON_POS_NG))

    def noun_singular(self):
        """noun_singular : (adjective)? (NOUN)+ (possess_singular|possess_plural|possess_general)?
        """
        adj = self.adjective() if ADJ in self.current_token.type else None
        nouns = []
        while NOUN in self.current_token.type:
            nouns.append(Word(self.current_token, NOUN))
            self.eat(NOUN)
        if PRON_POS_N in self.current_token.type:
            poss = self.possess_singular()
        elif PRON_POS_PLURAL_N in self.current_token.type:
            poss = self.possess_plural()
        else:
            poss = self.possess_general()
        return Noun("Singular", adj, nouns, poss)

    def noun_plural(self, determine=None):
        """noun_plural : MGA (adjective)? (NOUN)+ (possess_singular|possess_plural|possess_general)?
        """
        if determine is None:
            mga = self.current_token
            self.eat(MGA)
        else:
            mga = None
        adj = self.adjective() if ADJ in self.current_token.type else None
        nouns = []
        while NOUN in self.current_token.type:
            nouns.append(Word(self.current_token, NOUN))
            self.eat(NOUN)
        if PRON_POS_N in self.current_token.type:
            poss = self.possess_singular()
        elif PRON_POS_PLURAL_N in self.current_token.type:
            poss = self.possess_plural()
        else:
            poss = self.possess_general()
        return Noun("Plural", adj, nouns, poss, Word(mga, MGA))

    def possess_general(self):
        """possess_general : POS_LINK compound_nouns
        """
        if POS_LINK in self.current_token.type:
            pos_link = self.current_token
            self.eat(POS_LINK)
            if pos_link.value == 'sa' and self.contain([DET, PRON_DEM, PRON_POS, PRON_POS_NG, PRON_POS_PLURAL_NG, PRON_PER, DET_PLURAL, PRON_POS_PLURAL, PRON_PER_PLURAL, IKA, NUM, ADJ, KA, NOUN, MONTH, PREP]):
                return self.prep_phrase_add(pos_link)
            else:
                nouns = self.compound_nouns(pos_link)
                return Possess("General", Word(pos_link, POS_LINK), nouns)
        else:
            return None

    def possess_singular(self):
        """possess_singular: PRON_POS_N
        """
        pos = self.current_token
        self.eat(PRON_POS_N)
        return Possess("Singular", Word(pos, PRON_POS_N))

    def possess_plural(self):
        """possess_plural: PRON_POS_PLURAL_N
        """
        pos = self.current_token
        self.eat(PRON_POS_PLURAL_N)
        return Possess("Plural", Word(pos, PRON_POS_PLURAL_N))

    def compound_nouns(self, kind):
        """compound_nouns: (noun_singular|noun_plural)
                            | (noun_singular|noun_plural) COMMA compound_noun()
                            | (noun_singular|noun_plural) UG (noun_singular|noun_plural)
        """
        if kind.value == 'ni' and MGA in self.current_token.type:
            errors.append(Error("Misappropriate use of possessive linker", "Should use sa", kind.value))
        noun = self.noun_plural() if MGA in self.current_token.type else self.noun_singular()
        if COMMA in self.current_token.type:
            extra = self.current_token
            self.eat(COMMA)
            other = self.compound_nouns('')
            return CompoundNoun('', noun, other, Word(extra, COMMA))
        elif self.current_token.value == 'ug':
            extra = self.current_token
            self.eat(CONJ)
            other = self.noun_plural() if MGA in self.current_token.type else self.noun_singular()
            return CompoundNoun('', noun, other, Word(extra, CONJ))
        else:
            return CompoundNoun('', noun)

    def adj_ord(self):
        """adj_ord : IKA DASH NUM NGA
        """
        ika=Word(self.current_token, IKA)
        self.eat(IKA)
        dash=Word(Token([DASH], "-"), DASH)
        number = self.current_token
        self.eat(NUM)
        nga = self.current_token
        self.eat(NGA)
        return AdjOrd(ika, dash, Word(number, NUM), Word(nga, NGA))

    def adj_num(self):
        """adj_num : NUM KA
                   | KA NUM AN (UG NUM)? KA
        """
        if NUM in self.current_token.type:
            number = self.current_token
            self.eat(NUM)
            if PRON_PER in self.current_token.type:
                ka = self.current_token
                self.eat(PRON_PER)
                return AdjNum(Word(number, NUM), Word(ka, KA))
            else:
                return Word(number, NUM)
        elif self.current_token.value == 'ka':
            give = []
            give.append(Word(self.current_token, KA))
            self.eat(PRON_PER)
            give.append(Word(self.current_token, NUM))
            self.eat(NUM)
            give.append(Word(self.current_token, AN))
            self.eat(AN)
            if CONJ in self.current_token and self.current_token.value == UG:
                conj = self.current_token
                self.eat(UG)
                give.append(Word(self.current_token, NUM))
                self.eat(NUM)
            else:
                conj = None
            ka = self.current_token
            self.eat(KA)
            return AdjNum(give, Word(ka, KA), Word(conj, CONJ))
        else:
            return None

    def adjective(self):
        """adjective : ADJ ((NGA|NG) ADJ)* (NG|NGA)?
        """
        adjectives = []
        nga = []
        current = self.current_token
        adjectives.append(Word(current, ADJ))
        self.eat(ADJ)
        extra = stemmer.stem_word(current.value, as_object=True).prefix
        while NGA in self.current_token.type or extra == 'ng':
            if NGA in self.current_token.type:
                nga.append(Word(self.current_token, NGA))
                self.eat(NGA)
            else:
                nga.append(Word(Token(['NG_PREFIX'], extta), 'NG_PREFIX'))
            if ADJ in self.current_token.type:
                current = self.current_token
                extra = stemmer.stem_word(current.value, as_object=True).prefix
                adjectives.append(Word(current, ADJ))
                self.eat(ADJ)
        return Adjective(adjectives, nga)
        
    def parse(self):
        """
        sentence_part : sentence
                      | sentence (CONJ|COMMA) sentence_part
        sentence : pred_phrase (noun_phrase_part)?
        pred_phrase : verb_phrase (adverb)?
                    | predicate (adverb)? verb_phrase (adverb)?
        verb_phrase : verb_complex (noun_phrase_part)?
                    | verb_complex (prep_phrase)?
        predicate : descriptive
                  | noun_phrase_part
                  | prep_phrase
                  | INT
        descriptive : ADJ
                    | adverb
        adverb : PLACE (time)?
                | time (ADV_SPE)?
                | ADV_SPE
                | ADV
                | alas time
                | DILI (ADV_SPE)?
                | empty
        time : TIME
                 | NIAGING (adj_num)? TIME_NOUN
                 | SUNOD NGA (adj_num)? TIME_NOUN
                 | KARONG TIME_NOUN_A
                 | HOUR sa TIME_OF_DAY
        date : MONTH DAY (COMMA YEAR)?
                | IKA DASH DAY sa MONTH (COMMA YEAR)?
        prep_phrase : PREP (PREP)? noun_phrase_part (ADV_SPE)? (prep_phrase)?
                    | empty
        noun_phrase_part : noun_phrase
                            | noun_phrase COMMA noun_phrase_part
                            | noun_phrase CONJ noun_phrase
        noun_phrase : (noun_phrase_singular | noun_phrase_plural | dem_pron | noun_phrase_ang) (NGA sentence)? (prep_phrase)?
                       | date
                       | number
                       | empty
        noun_phrase_singular : (DET) (adj_ord)? (adj_num)? noun_singular 
                             | PRON_PER
                             | PRON_POS_NG (noun_singular|noun_plural)
        noun_phrase_plural : (DET_PLURAL) (adj_ord)? (adj_num)? noun_plural
                           | PRON_PER_PLURAL
                           | PRON_POS_PLURAL_NG (noun_singular|noun_plural)
        noun_phrase_ang : ANG (PRON_POS_NG)? (adj_ord)? (adj_num)? (noun_singular|noun_plural) 
                           | ANG (PRON_POS_PLURAL_NG)? (adj_ord)? (adj_num)? (noun_singular|noun_plural)         
        dem_pron : dem_pron : PRON_DEM (CLIT_NG (adj_ord)? (adj_num)? (noun_singular | noun_plural))?
        noun_singular : (adjective)? (NOUN)+ (possess_singular|possess_plural|possess_general)?
        noun_plural : MGA (adjective)? (NOUN)+ (possess_singular|possess_plural|possess_general)?
        possess_singular: PRON_POS_N
        possess_plural: PRON_POS_PLURAL_N
        possess_general : POS_LINK compound_nouns
        compound_nouns: (noun_singular|noun_plural)
                            | (noun_singular|noun_plural) COMMA compound_noun()
                            | (noun_singular|noun_plural) UG (noun_singular|noun_plural)
        adj_ord : IKA DASH NUM (NGA | NG) 
        adj_num : NUM KA
                | KA NUM AN (UG NUM)? KA
        verb_complex : (verb_prefix)? VERB (verb_suffix)? ((PRON_PER)CLIT_Y)?
        verb_prefix : VERB_PREF_PRES
                    | VERB_PREF_PAST
                    | VERB_PREF_FUT
        verb_suffix : A
                    | HA
                    | HI
                    | VERB_SUFF_PRES
                    | VERB_SUFF_PAST
                    | VERB_SUFF_FUT
        adjective : ADJ (NGA ADJ)* (CLIT_NG|NGA)?
        """
        node = self.sentence_part()
        #if self.current_token.type != EOF:
        #    self.error()

        return node