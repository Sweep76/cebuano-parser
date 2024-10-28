###############################################################################
#                                                                             #
#  AST visitors (walkers)                                                     #
#                                                                             #
###############################################################################
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Node(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = "    "*level+("|-->" if level>0 else "")+repr(self.value)+"\n"
        for child in self.children:
            if type(child) == list:
                for v in child:
                    ret += v.__str__(level+1)
            else:
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_branch = None
        
    def visit_SentencePart(self, node):
        sentence = self.visit(node.left)
        if node.conj is not None:
            conj = self.visit(node.conj)
            sentence_part = self.visit(node.right)
            return Node("Sentence Part", [sentence, conj, sentence_part])
        else:
            return Node("Sentence Part", [sentence])

    def visit_NounPhrasePart(self, node):
        noun = self.visit(node.left)
        if node.conj is not None:
            conj = self.visit(node.conj)
            noun_part = self.visit(node.right)
            return Node("Noun Phrase Part", [noun, conj, noun_part])
        else:
            return Node("Noun Phrase Part", [noun])

    def visit_Sentence(self, node):
        predph = self.visit(node.pred_phrase)
        nounph = self.visit(node.noun_phrase)
        return Node("Sentence", [predph, nounph])

    def visit_PredPhrase(self, node):
        pred = self.visit(node.pred)
        verb_ph  = self.visit(node.verb_phr)
        endadv = self.visit(node.adv)
        midadv = self.visit(node.mid_adv)
        return Node("Predicate Phrase", [pred, midadv, verb_ph, endadv])

    def visit_Predicate(self, node):
        return Node("Predicate", [self.visit(node.content)])

    def visit_Descriptive(self, node):
        return Node("Descriptive", [self.visit(node.content)])

    def visit_Adverb(self, node):
        if self is not None:
            element = self.visit(node.content)
            add = self.visit(node.addition)
            return Node("Adverb", [element, add])
        else:
            return Node("Adverb", ["empty"])

    def visit_Time(self, node):
        num = self.visit(node.number)
        day = self.visit(node.day)
        if type(node.noun) == list:
            return Node("Time", [[self.visit(v) for v in node.noun], num, day])
        else:
            return Node("Time", [self.visit(node.noun), num, day])

    def visit_NounPhrase(self, node):
        noun = self.visit(node.complex_noun)
        prep = self.visit(node.prep_phrase)
        nga = self.visit(node.nga)
        clause = self.visit(node.clause)
        return Node("Noun Phrase", [noun, prep, nga, clause])
        
    def visit_VerbPhrase(self, node):
        verb = self.visit(node.complex_verb)
        opt = self.visit(node.opt)
        return Node("Verb Phrase", [verb, opt])

    def visit_PrepPhrase(self, node):
        prep = self.visit(node.prep)
        second = self.visit(node.second_prep)
        noun = self.visit(node.noun_phrase)
        adv = self.visit(node.adv)
        extra = self.visit(node.extra)
        return Node("Prepositional Phrase", [prep, second, noun, adv, extra])

    def visit_Adjective(self, node):
        ng = self.visit(node.clit_ng)
        return Node("Adjective", [[self.visit(adj) for adj in node.adjectives], [self.visit(nga) for nga in node.nga], ng])

    def visit_AdjOrd(self, node):
        mark = self.visit(node.marker)
        dash = self.visit(node.dash)
        num = self.visit(node.number)
        nga = self.visit(node.nga)
        return Node("Ordinal Adjective", [mark, dash, num, nga])

    def visit_Date(self, node):
        month = self.visit(node.month)
        day = self.visit(node.day)
        com = self.visit(node.comma)
        year = self.visit(node.year)
        if node.type == "Spanish":
            sa = self.visit(node.sa)
            if type(node.extra) == list:
                return Node(node.type+" Date", [[self.visit(v) for v in node.extra], day, sa, month, com, year])
            else:
                return Node(node.type+" Date", [self.visit(node.extra), day, sa, month, com, year])
        elif node.type == "English":
            return Node(node.type+" Date", [month, day, com, year])

    def visit_AdjNum(self, node):
        num = self.visit(node.number)
        ka = self.visit(node.ka)
        conj = self.visit(node.conj)
        return Node("Numerical Adjective", [num, conj, ka])

    def visit_Noun(self, node):
        adj = self.visit(node.adjective)
        mga = self.visit(node.mga)
        poss = self.visit(node.possess)
        return Node(node.type+" Noun", [mga, adj, [self.visit(n) for n in node.nouns], poss])

    def visit_Possess(self, node):
        noun = self.visit(node.noun)
        link = self.visit(node.link)
        return Node(node.type+" Possessive Phrase", [link, noun])

    def visit_CompoundNoun(self, node):
        other = self.visit(node.other_phrase)
        noun = self.visit(node.noun_phrase)
        extra = self.visit(node.extra)
        return Node(node.type+"Compound Noun", [noun, extra, other])
            
    def visit_NounPhraseSingularPlural(self, node):
        noun = self.visit(node.noun_sp)
        begin = self.visit(node.start)
        extra = self.visit(node.extra)
        ordinal = self.visit(node.ordinal)
        num = self.visit(node.number)
        mga = self.visit(node.mga)
        pos = self.visit(node.pos)
        return Node(node.type+" Noun Phrase", [begin, pos, ordinal, num, mga, noun, extra])

    def visit_DemPronoun(self, node):
        dem = self.visit(node.pronoun)
        clit = self.visit(node.clit)
        ordinal = self.visit(node.ordinal)
        num = self.visit(node.number)
        mga = self.visit(node.mga)
        return Node(node.type+" Demonstrative Phrase", [dem, clit, ordinal, num, mga])
                    
    def visit_VerbComplex(self, node):
        prefix = self.visit(node.prefix)
        root = self.visit(node.root)
        suffix = self.visit(node.suffix)
        extra = self.visit(node.extra)
        return Node("Complex Verb", [prefix, root, suffix, extra])

    def visit_Word(self, node):
        if node.content is None:
            return Node("___")
        else:
            if type(node.content) == str:
                return Node(node.type+"->"+node.content)
            else:
                return Node(node.type+"->"+str(node.content.value))

    def visit_NoneType (self, node):
        return Node("___")
       
    
def main():
    text = open("cebuano.txt", 'r').read().lower()

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    
    long = len(errors)
    print(text)
    if long == 0:
        print("No errors")
    for x in range(long):
        print("Error #"+str(x+1))
        print(errors[x].error)
        if errors[x].wrong_value is not None:
            print("Error value: "+str(errors[x].wrong_value))
        print("Solution #"+str(x+1))
        print(errors[x].correct)
        if errors[x].right_value is not None:
            print("Right values: "+", ".join(errors[x].right_value))

    semantic_analyzer = SemanticAnalyzer()
    try:
        one = semantic_analyzer.visit(tree)
    except Exception as e:
        print(e)
        raise
    print(one)

if __name__ == '__main__':
    main()