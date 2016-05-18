def check_parens(string1):
    # paren=0
    # brack=0
    # brace=0
    # for x, i in enumerate(string):
    #     if x == 0:
    #         if i == ")" or i == "]" or i == "}":
    #             return False
    #     if i == "(":
    #         paren+=1
    #     elif i == ")":
    #         paren-=1
    #     elif i =="[":
    #         brack+=1
    #     elif i =="]":
    #         brack-=1
    #     elif i =="{":
    #         brace+=1
    #     elif i =="}":
    #         brace-=1
    #     else:
    #         pass
    #
    # if paren == brack == brace == 0:
    #     return True
    # return False


    import string
    s = ''.join([c for c in string1 if c in ['(){}[]']])
    s0 = ''
    print s, s0
    while s!=s0:
        print s, s0
        s0 = string.replace(s, '()', '')
        s0 = string.replace(s, '{}', '')
        s0 = string.replace(s, '[]', '')
    return not s
