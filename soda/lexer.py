from rply import LexerGenerator

lg = LexerGenerator()
lg.ignore(r"\s+")
lg.ignore(r"#.*")
lg.add("PRINTLN", r"Println")
lg.add("NUMBER", r"(((0|-?[1-9][0-9]*)(\.[0-9]*)?)|(\.[0-9]*))([eE][\+\-]?[0-9]*)?")
lg.add("STRING", r"\"([^\"\\]|\\.)*\"")
lg.add("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*")
lg.add("+", r"\+")
lg.add("-", r"-")
lg.add("*", r"\*")
lg.add("/", r"/")
lg.add("%", r"%")
lg.add("^", r"\^")
lg.add("(", r"\(")
lg.add(")", r"\)")
lexer = lg.build()
