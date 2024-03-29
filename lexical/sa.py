import subprocess
import sys

global token 
global lexeme 
global i  
global display
global z # var to just handle formatting to output file

## this is the file, the file to pass into the lexer()
filename = sys.argv[1]

argument = filename 

subprocess.run(["python3", "la.py", argument])

##grab the current lexer and token 
## after passing it in the lexer()
with open("result.txt", "r") as file1:
    lexervals = []
    for x in file1:
        lexervals.append(x.strip().split())

## update the token and lexeme values 
## this will do the incremementing too 
def lexer():
    global token 
    global lexeme
    global i 
    
    token = lexervals[i][0]
    lexeme = lexervals[i][1]
    i += 1

def printOut(file):
    global z # var to just handle formatting to output file
    
    if z == 0:
        file.write("Token: " + token + "\tLexeme: " + lexeme + "\n")
        z += 1
    else: 
        file.write("\n")
        file.write("Token: " + token + "\tLexeme: " + lexeme + "\n")

def Rat24s(file):    
    if (lexeme == '$'):
       
        if (display):
            print("<Rat24S> -> $ <Opt Function Definition> $ <Opt Declaration List> " +
                  "$ <Statement List> $")
        
        printOut(file)
        file.write("<Rat24S> -> $ <Opt Function Definition> $ <Opt Declaration List> " +
                  "$ <Statement List> $\n")
        
        lexer()  
        OptFunctionDefinition(file)
        if lexeme == '$':
            printOut(file)
            lexer()
            OptDeclarationList(file)
            if lexeme == '$':
                printOut(file)
                lexer()
                StatementList(file)
                if lexeme == '$':
                    printOut(file)
                else:
                    print("RAT24S Syntax Error: wrong syntax found, expected '$' as ending character" 
                      + " instead got " + lexeme)
                    exit(1) 
            else:
                print("RAT24S Syntax Error: wrong syntax found, expected '$' after <Opt Declaration List>" 
                      + " instead got " + lexeme)
                exit(1)                
        else:
            print("RAT24S Syntax Error: wrong syntax found, expected '$' after <Opt Function Definition>"  
                 + " instead got " + lexeme)
            exit(1)
    else:
        print("RAT24S Syntax Error: wrong syntax found, expected '$', instead got " + lexeme)
        exit(1)

def OptFunctionDefinition(file):
    if lexeme == "function":
        if (display):
            print("<Opt Function Definitons> -> <Function Definitions>")
        
        printOut(file)
        file.write("<Opt Function Definitons> -> <Function Definitions>\n")
        
        FunctionDefinitions(file)
    else:
        if (display):
            print("<Opt Function Definitons> -> Epsilon")
        file.write("<Opt Function Definitons> -> Epsilon")
        Empty()        

def FunctionDefinitions(file):
    if (display):
        print("<Function Definitions> -> <Function> <Function Definitons Prime>")
    
    file.write("<Function Definitions> -> <Function> <Function Definitons Prime>\n")
    
    Function(file)
    FunctionDefinitionsPrime(file)

def FunctionDefinitionsPrime(file):
    if lexeme == 'function':
        if (display):
            print("<Function Definitions> -> <Function Definitons Prime>")
        file.write("<Function Definitions> -> <Function Definitons Prime>\n")
        FunctionDefinitions(file)
    else:
        if (display):
            print("<Function Definitions> -> Epsilon")
        file.write("<Function Definitions> -> Epsilon\n")
        Empty()

def Function(file):
    if lexeme == 'function':
        if (display):
            print("<Function> -> function <Identifier> " +
                  "(<Opt Parameter List>) <Opt Declaration List> <Body>")
        
        file.write("<Function> -> function <Identifier> " +
                  "(<Opt Parameter List>) <Opt Declaration List> <Body>\n")
        lexer()
        if token == 'Identifier':
            printOut(file)
            lexer()
            
            if lexeme == '(':
                printOut(file)
                lexer()
                OptParameterList(file)
                
                if lexeme == ')':
                    printOut(file)
                    lexer()
                    OptDeclarationList(file)
                    Body(file)
                        
                else:
                    print("Function Syntax Error: wrong syntax found, expected ')'," 
                    + "instead got " + token + ' ' + lexeme)
                    exit(1)     
            else:
                print("Function Syntax Error: wrong syntax found, expected '(' before Opt Param List" + 
                      ", instead got " + lexeme)
        else:
            print("Function Syntax Error: wrong syntax found, expected 'Identifier' after 'function'," 
                  + "instead got " + token + ' ' + lexeme)
            exit(1)

def OptParameterList(file):
    if token == 'Identifier':
        # printOut(file)
        if (display):
            print("<Opt Parameter List> -> <Parameter List>")
        
        file.write("<Opt Parameter List> -> <Parameter List>\n")
        ParameterList(file)
    else:
        if (display):
            print("<Opt Parameter List> -> Epsilon")
        
        file.write("<Opt Parameter List> -> Epsilon\n")

def ParameterList(file):
    if (display):
        print("<Parameter List> -> <Parameter> <Parameter List Prime>")
    file.write("<Parameter List> -> <Parameter> <Parameter List Prime>\n")
    
    Parameter(file)
    ParameterListPrime(file)

def ParameterListPrime(file):
    if lexeme == ',':
        if (display):
            print("<Parameter List Prime> -> , <Parameter List>")
        printOut(file)
        lexer()
        ParameterList(file)
    else:
       if (display):
            print("<Parameter List Prime> -> Epsilon")
        
    file.write("<Parameter List Prime> -> Epsilon\n")  
    Empty()

def Parameter(file):
    if (token == 'Identifier'):
        if (display):
            print("<Parameter> -> <IDs> <Qualifier>")
        file.write("<Parameter> -> <IDs> <Qualifier>\n")
        
        IDs(file)
        Qualifier(file)
    else:
        print("Parameter Syntax Error: wrong syntax found, expected 'Identifier'," 
              + "instead got " + token + ' ' + lexeme)
        exit(1)

def IDs(file):
    if token == 'Identifier':
        printOut(file)
        if (display):
                print("<IDs> -> <Identifier> <IDs Prime>")
        file.write("<IDs> -> <Identifier> <IDs Prime>\n")
        lexer()
        IDsPrime(file)
    else:
        print("IDs Syntax Error: wrong syntax found, expected 'Identifier'," 
              + "instead got " + token + ' ' + lexeme)
        exit(1)          

def IDsPrime(file):
    if (lexeme == ','):
        printOut(file)
        if (display):
                print("<IDs Prime> -> ,<IDs>")
        file.write("<IDs Prime> -> ,<IDs>\n")
        
        # printOut(file)
        lexer()
        IDs(file)
    else:
        if (display):
                print("<IDs Prime> -> Epsilon")
        file.write("<IDs Prime> -> Epsilon\n")
        Empty()

def Qualifier(file):
    if (token == 'Keyword' and lexeme == 'integer'):
        if (display):
                print("<Qualifier> -> integer")
        printOut(file)
        file.write("<Qualifier> -> integer\n") 
        
        lexer()   
    
    elif (token == 'Keyword' and lexeme == 'boolean'):
        if (display):
                print("<Qualifier> -> boolean")
        printOut(file)
        file.write("<Qualifier> -> boolean\n")
        lexer()  
    
    elif (token == 'Keyword' and lexeme == 'real'):
        if (display):
                print("<Qualifier> -> real")
        printOut(file)
        file.write("<Qualifier> -> real\n")
        lexer()  
    else:
        print("Qualifier Syntax Error: wrong syntax found, expected 'integer or " 
              + "real or boolean' after <Identifier>," 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def Body(file):
    if lexeme == '{':
        printOut(file)
        
        if (display):
            print("<Body> -> { <Statement List> }")
        file.write("<Body> -> { <Statement List> }\n") 
        
        # printOut(file)
        lexer()
        StatementList(file)
        
        if lexeme == '}':
            printOut(file)
            lexer()
        else:
            print("Body Syntax Error: wrong syntax found, expected '}', after <Statement List>" 
              + " instead got " + token + ' ' + lexeme)
            exit(1) 
    else:
        print("Body Syntax Error: wrong syntax found, expected '{'," 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def StatementList(file):
    if (display):
            print("<Statement List> -> <Statement> <Statement List Prime>")
    file.write("<Statement List> -> <Statement> <Statement List Prime>\n")
    
    Statement(file)
    StatementListPrime(file)

def StatementListPrime(file):
    if (lexeme == '{' or token == 'Identifier' or lexeme == 'if'or 
    lexeme == 'return' or lexeme == 'print' or lexeme == 'scan'
    or lexeme == 'while'):
        if (display):
            print("<Statement List Prime> -> <Statement List>")
        file.write("<Statement List Prime> -> <Statement List>\n")
        StatementList(file)
    
    else:
        if (display):
            print("<Statement List Prime> -> Epsilon")
        
        file.write("<Statement List Prime> -> Epsilon\n")  
        Empty()

def Statement(file):
    if lexeme == '{':
        if (display):
            print("<Statement> -> <Compound>")
        printOut(file)
        file.write("<Statement> -> <Compound>\n")
        Compound(file)
        
    elif token == 'Identifier':
        if (display):
            print("<Statement> -> <Assign>")
        printOut(file)
        file.write("<Statement> -> <Assign>\n")
        Assign(file)
        
    elif lexeme == 'if':
        if (display):
            print("<Statement> -> <If>")
        printOut(file)
        file.write("<Statement> -> <If>\n")
        If(file)
        
    elif lexeme == 'return':
        if (display):
            print("<Statement> -> <Return>")
        printOut(file)
        file.write("<Statement> -> <Return>\n")
        Return(file)
        
    elif lexeme == 'print':
        if (display):
            print("<Statement> -> <Print>")
        printOut(file)
        file.write("<Statement> -> <Print>\n")
        Print(file)
        
    elif lexeme == 'scan':
        if (display):
            print("<Statement> -> <Scan>")
        printOut(file)
        file.write("<Statement> -> <Scan>\n")
        Scan(file)
        
    elif lexeme == 'while':
        if (display):
            print("<Statement> -> <While>")
        printOut(file)
        file.write("<Statement> -> <While>\n")
        While(file)
        
    else:
        print("Statement Syntax Error: wrong syntax found, expected '{' or " + 
              "<Identifier> or 'if' or 'return' or 'print' or 'scan' or 'while' after '{'," 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def Compound(file):
    if lexeme == '{':
        if (display):
            print("<Compound> -> { <Statement List> }")
        file.write("<Compound> -> { <Statement List> }\n")
        
        lexer()
        StatementList(file)
        
        if lexeme == '}':
            printOut(file)
            lexer()
        else:
            print("Compound Syntax Error: wrong syntax found, expected '}'"
              + " instead got " + token + ' ' + lexeme)
            exit(1) 
        
    else:
        print("Compound Syntax Error: wrong syntax found, expected '{'"
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def Assign(file):
    if token == 'Identifier':
        if (display):
            print("<Assign> -> <Identifier> = <Expression>;")
        file.write("<Assign> -> <Identifier> = <Expression>;\n")
        
        lexer()
        
        if lexeme == '=':
            printOut(file)
            lexer()
            Expression(file)
            
            if lexeme == ';':
                printOut(file)
                lexer()
            else:
                print("Assign Syntax Error: wrong syntax found, expected ';' after expression"
                + " instead got " + token + ' ' + lexeme)
                exit(1)
        else:
            print("Assign Syntax Error: wrong syntax found, expected '=' after <Identifier>"
              + " instead got " + token + ' ' + lexeme)
            exit(1) 
    else:
        print("Assign Syntax Error: wrong syntax found, expected 'Identifier'"
              + " instead got " + token + ' ' + lexeme)
        exit(1)

def Expression(file):
    if (display):
            print("<Expression> -> <Term> <Expression Prime>")
    file.write("<Expression> -> <Term> <Expression Prime>\n")
    Term(file)
    ExpressionPrime(file)

def ExpressionPrime(file):
    if lexeme == '+':
        printOut(file)
        
        if (display):
            print("<Expression Prime> -> + <Term> <Expression Prime>")
        file.write("<Expression Prime> -> + <Term> <Expression Prime>\n")
        
        lexer()
        Term(file)
        ExpressionPrime(file)
        
    elif lexeme == '-':
        printOut(file)
        
        if (display):
            print("<Expression Prime> -> - <Term> <Expression Prime>")
        file.write("<Expression Prime> -> - <Term> <Expression Prime>\n")
        
        lexer()
        Term(file)
        ExpressionPrime(file)
        
    else:
        if (display):
            print("<Expression Prime> -> Epsilon")
        file.write("<Expression Prime> -> Epsilon\n")  
        Empty()
    
def Term(file):
    if (display):
            print("<Term> -> <Factor> <Term Prime>")
    file.write("<Term> -> <Factor> <Term Prime>\n")
    
    Factor(file)
    TermPrime(file)

def TermPrime(file):
    if lexeme == '*':
        printOut(file)
        
        if (display):
                print("<Term Prime> -> * <Factor> <Term Prime>")
        file.write("<Term> -> * <Factor> <Term Prime>\n")
        
        lexer()
        Factor(file)
        TermPrime(file)
    
    elif lexeme == '/':
        printOut(file)
        
        if (display):
                print("<Term Prime> -> / <Factor> <Term Prime>")
        file.write("<Term> -> / <Factor> <Term Prime>\n")
        
        lexer()
        Factor(file)
        TermPrime(file)
        
    else:
        if (display):
            print("<Term Prime> -> Epsilon")
        file.write("<Term Prime> -> Epsilon\n")  
        Empty()

def Factor(file):
    if lexer == '-':
        printOut(file)
        if (display):
            print("<Factor> -> -<Primary>")
        file.write("<Factor> -> -<Primary>\n") 
        
        lexer()
        Primary(file)
    else:
        if (display):
            print("<Factor> -> <Primary>")
        file.write("<Factor> -> <Primary>\n") 
        Primary(file)

def Primary(file):
    if token == 'Identifier':
        printOut(file)
        if (display):
            print("<Primary> -> <Identifier>")
        file.write("<Primary> -> <Identifier>\n") 
        lexer()
        PrimaryPrime(file)
        
    elif token == 'Integer':
        printOut(file)
        if (display):
            print("<Primary> -> <Integer>")
        file.write("<Primary> -> <Integer>\n") 
        lexer()  
        
    elif lexeme == '(':
        printOut(file)
        if (display):
            print("<Primary> -> ( <Expression> )")
        file.write("<Primary> -> ( <Expression> )\n") 
        lexer()
        Expression(file)
        if lexeme == ')':
            printOut(file)
            lexer()
        else:
            print("Primary Syntax Error: wrong syntax found, expected ')' after <Expression>" + 
             " instead got " + token + ' ' + lexeme)
            exit(1)
        
    elif lexeme == 'real':
        printOut(file)
        if (display):
            print("<Primary> -> <Real>")
        file.write("<Primary> -> <Real>\n") 
        lexer()
        
    elif lexeme == 'true':
        printOut(file)
        if (display):
            print("<Primary> -> true")
        file.write("<Primary> -> true\n") 
        lexer()
        
    elif lexeme == 'false':  
        printOut(file)
        if (display):
            print("<Primary> -> false")
        file.write("<Primary> -> false\n") 
        lexer()
        
    else:
        print("Primary Syntax Error: wrong syntax found, expected " +
              "<Identifier> or <Integer> or '(' or 'real' or 'true' or 'false'" 
              + " instead got " + token + ' ' + lexeme)
        exit(1)

def PrimaryPrime(file):
    if lexeme == '(':
        printOut(file)
        if (display):
            print("<Primary Prime> -> ( <IDs> )")
        file.write("<Primary Prime> -> ( <IDs> )\n") 
        
        lexer()
        IDs(file)
        
        if lexeme == ')':
            printOut(file)
            lexer()
        else:
            print("Primary Prime Syntax Error: wrong syntax found, expected ')' after <Expression>" 
              + " instead got " + token + ' ' + lexeme)
            exit(1)    
    else:
        if (display):
            print("<Primary Prime> -> Epsilon")
        file.write("<Primary Prime> -> Epsilon\n")  
        Empty()

def If(file):
    if lexeme == 'if':
        printOut(file)
        
        if (display):
            print("<If> -> ( <Condition> ) <Statement> <If Prime>")
        file.write("<If> -> ( <Condition> ) <Statement> <If Prime>\n") 
        
        lexer()
        if lexeme == '(':
            printOut(file)
            lexer()
            Condition(file)
            if lexeme == ')':
                printOut(file)
                lexer()
                Statement(file)
                IfPrime(file)
            else:
                print("If Syntax Error: wrong syntax found, expected ')'" 
                + " instead got " + token + ' ' + lexeme)
                exit(1)
        else:
            print("If Syntax Error: wrong syntax found, expected '('" 
              + " instead got " + token + ' ' + lexeme)
            exit(1)    
    else:
        print("If Syntax Error: wrong syntax found, expected 'if'" 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 
        
def IfPrime(file):
    if lexeme == 'endif':
        printOut(file)
        
        if (display):
            print("<If Prime> -> endif")
        file.write("<If Prime> -> endif\n") 
        lexer()
        
    elif lexeme == 'else':
        printOut(file)
        
        if (display):
            print("<If Prime> -> else <Statement> endif")
        file.write("<If Prime> -> else <Statement> endif\n") 
        
        lexer()
        Statement(file)
        if lexeme == 'endif':
            printOut(file)
            lexer()
        else:
            print("If Prime Syntax Error: wrong syntax found, expected 'endif'" 
              + " instead got " + token + ' ' + lexeme)
            exit(1)
            
    else:
        print("If Prime Syntax Error: wrong syntax found, expected 'endif' or 'else'" 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def Condition(file):
    if (display):
        print("<Condition> -> <Expression> <Relop> <Expression>")
    file.write("<Condition> -> <Expression> <Relop> <Expression>\n")
    
    Expression(file)
    Relop(file)
    Expression(file)

def Relop(file):
    if lexeme == '==':
        printOut(file)
        if (display):
            print("<Relop> -> ==")
        file.write("<Relop> -> ==\n")
        lexer()
        
    elif lexeme == '!=':
        printOut(file)
        if (display):
            print("<Relop> -> !=")
        file.write("<Relop> -> !=\n")
        lexer()
        
    elif lexeme == '<=':
        printOut(file)
        if (display):
            print("<Relop> -> <=")
        file.write("<Relop> -> <=\n")
        lexer()
        
    elif lexeme == '=>':
        printOut(file)
        if (display):
            print("<Relop> -> =>")
        file.write("<Relop> -> =>\n")
        lexer()
        
    elif lexeme == '>':
        printOut(file)
        if (display):
            print("<Relop> -> >")
        file.write("<Relop> -> >\n")
        lexer()
        
    elif lexeme == '<':
        printOut(file)
        if (display):
            print("<Relop> -> <")
        file.write("<Relop> -> <\n")
        lexer()
        
    else:
        print("Relop Syntax Error: wrong syntax found, expected '==' or '!='" +
              "or '<=' or '=>' or '>' or ''<" 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def Return(file):
    if lexeme == 'return':
        if (display):
            print("<Return> -> return <Return Prime>")
        file.write("<Return> -> return <Return Prime>\n")
        lexer()
        ReturnPrime(file)
    else:
        print("Return Syntax Error: wrong syntax found, expected 'return'"
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def ReturnPrime(file):
    if lexeme == ';':
        if (display):
            print("<Return Prime> -> ;")
        file.write("<Return Prime> -> ;\n")
    else:
        if (display):
            print("<Return Prime> -> <Expression>;")
        file.write("<Return Prime> -> <Expression>;\n")
        Expression(file)
        if lexeme == ';':
            printOut(file)
            lexer()
        else:
            print("Return Prime Syntax Error: wrong syntax found, expected ';' after <Expression>"
              + " instead got " + token + ' ' + lexeme)
            exit(1)

def Print(file):
    if lexeme == 'print':
        if (display):
            print("<Print> -> print ( <Expression> );")
        file.write("<Print> -> print ( <Expression> );\n")
        lexer()
        
        if lexeme == '(':
            printOut(file)
            lexer()
            Expression(file)
            if lexeme == ')':
                printOut(file)
                lexer()
                if lexeme == ';':
                    printOut(file)
                    lexer()
                else:
                    print("Print Syntax Error: wrong syntax found, expected ';' after <Expression>"
                    + " instead got " + token + ' ' + lexeme)
                    exit(1) 
            else:
                print("Print Syntax Error: wrong syntax found, expected ')' after <Expression>"
                + " instead got " + token + ' ' + lexeme)
                exit(1) 
        else:
            print("Print Syntax Error: wrong syntax found, expected '(' after 'print'"
              + " instead got " + token + ' ' + lexeme)
            exit(1)     
    else:
        print("Print Syntax Error: wrong syntax found, expected 'print'"
              + " instead got " + token + ' ' + lexeme)
        exit(1)            

def Scan(file):
    if lexeme == 'scan':
        # printOut(file)
        if (display):
            print("<Scan> -> scan ( <IDs> );")
        file.write("<Scan> -> scan ( <IDs> );\n")
        lexer()
        if lexeme == '(':
            printOut(file)
            lexer()
            IDs(file)
            if lexeme == ')':
                printOut(file)
                lexer()
                if lexeme == ';':
                    printOut(file)
                    lexer()
                else:
                    print("Scan Syntax Error: wrong syntax found, expected ';'"
                    + " instead got " + token + ' ' + lexeme)
                    exit(1)
            else:
                print("Scan Syntax Error: wrong syntax found, expected ')'"
                + " instead got " + token + ' ' + lexeme)
                exit(1)                
        else:
            print("Scan Syntax Error: wrong syntax found, expected '('"
              + " instead got " + token + ' ' + lexeme)
            exit(1)    
        
    else:
        print("Scan Syntax Error: wrong syntax found, expected 'scan'"
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def While(file):
    if lexeme == 'while':
        # printOut(file)
        
        if (display):
            print("<While> -> while ( <Condition> ) <Statement> endwhile")
        file.write("<While> -> while ( <Condition> ) <Statement> endwhile\n")
        lexer()
        
        if lexeme == '(':
            printOut(file)
            lexer()
            Condition(file)
            if lexeme == ')':
                printOut(file)
                lexer()
                Statement(file)
                if lexeme == 'endwhile':
                    printOut(file)
                    lexer()
                else:
                    print("While Syntax Error: wrong syntax found, expected 'endwhile' after <Statement>"
                    + " instead got " + token + ' ' + lexeme)
                    exit(1)
            else:
                print("While Syntax Error: wrong syntax found, expected ')' after <Condition>"
                + " instead got " + token + ' ' + lexeme)
                exit(1)
        else:
            print("While Syntax Error: wrong syntax found, expected '(' after 'while'"
              + " instead got " + token + ' ' + lexeme)
            exit(1)     
    else:
        print("While Syntax Error: wrong syntax found, expected 'while'"
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def OptDeclarationList(file):
    if (lexeme == 'integer' or lexeme == 'boolean' or lexeme == 'real'):
        if (display):
            print("<Opt Declaration List> -> <Declaration List>")
        file.write("<Opt Declaration List> -> <Declaration List>\n") 
        DeclarationList(file)
    else:
        if (display):
            print("<Opt Declaration List> -> Epsilon")
        
        file.write("<Opt Declaration List> -> Epsilon\n")  
        Empty()

def DeclarationList(file):
    if (display):
        print("<Declaration List> -> <Declaration>; <Declaration List Prime>")
    file.write("<Declaration List> -> <Declaration>; <Declaration List Prime>\n") 
    
    Declaration(file)
    if lexeme == ';':
        printOut(file)
        lexer()
        DeclarationListPrime(file)
    else:
        print("Declaration List Syntax Error: wrong syntax found, expected ';'" + 
              "after <Declaration>," 
              + " instead got " + token + ' ' + lexeme)
        exit(1) 

def DeclarationListPrime(file):
    if lexeme == 'integer' or lexeme == 'boolean' or lexeme == 'real':
        
        if (display):
            print("<Declaration List Prime> -> <Declaration>")
        file.write("<Declaration List Prime> -> <Declaration>\n") 
        DeclarationList(file)
    else:
        if (display):
            print("<Declaration List Prime> -> Epsilon")
        file.write("<Declaration List Prime> -> Epsilon\n")  
        Empty()

def Declaration(file):
    if (display):
        print("<Declaration> -> <Qualifier> <IDs>")
    file.write("<Declaration> -> <Qualifier> <IDs>\n")
    
    Qualifier(file)
    IDs(file)    

def Empty():
    pass

def main():
    global i 
    global display 
    global z
    
    i = 0
    z = 0 
    
    print("\n")
    
    display_input = input("Enter 0 for no printing, 1 for printing: ")
    
    if display_input == '0':
        display = False
    else:
        display = True 
    
    with open("sa_results.txt", "w") as file: 
        lexer()
        Rat24s(file)

main()