import os
import re

global gcnt
gcnt = 0

global autcheck
autcheck = []

global textcheck
textcheck = []

sketch = 'C:\\Users\\Artem\\Desktop\\pr\\tx'
textreg = re.compile('<TEXT>(.*?)</TEXT>', re.DOTALL)
autreg = re.compile('<AUTHOR>(.*?)</AUTHOR>')
datereg = re.compile('<DATE>(.*?)</DATE>')
genrereg = re.compile('<GENRE>(.*?)</GENRE>')    
wcntreg  = re.compile('<WORDCOUNT>(.*?)</WORDCOUNT>')


def sent(text, meta, path): #path for the original xml; meta[1] - file name. operating with the whole text
    global gcnt
    gcnt += 1

    excl = '.!? '
    miscexcl = ',:;--"().!?&[]'
    
    def wd(word, sn, wn, l): #l - this word's sentence length. operating with a word
        print('word', word)
        
        def morph(word): #get morphology
            mpath = path.replace('\\tx\\', '\\outpt\\MORPH\\')
            mpath = mpath.replace(meta[1]+'.xml', 'M_' + meta[1] + '.txt')
            mtab = open(mpath, 'r').readlines()
            #print(word.strip(miscexcl), word)
            for ln in mtab:
                if word.strip(miscexcl) == ln.split(':')[0]:
                    if len(ln.split(':')) > 2:
                        return '?'
                    else:
                        return ln.split(':')[1]
                elif '\n' in word:
                    return '?'
            return '?'
        
        
        if word.istitle() == True:
            graph = 'cap'
        else:
            graph = ''

        punctr = ''
        for symb in word[-2:]:
            if symb in miscexcl:
                punctr += symb

        sent_pos = ''
        if wn == 1:
            sent_pos = 'bos'
        elif wn == l:
            sent_pos = 'eos'

                    
        inf = morph(word)

        if inf != '?' and word.strip(miscexcl) != '': #writting morphology in prs
            lemcnt = 0
            morph = inf.split()
            nvars = len(morph)
            for lemind in morph:
                if '&lt' in lemind:
                    lemcnt += 1
            if lemcnt == 0:
                lemcnt = 1
            for z in range(nvars): #itering given word's full gram set
                #print(morph[z])                    
                nvar = z+1
                if '&lt' in morph[z].split('+')[0]:
                    #print(morph[z].split('+'))
                    lemf = re.search('&lt;(.*?)&gt;((.*?)})?', morph[z].split('+')[0])
                    if str(lemf) != 'None':
                        lem = lemf.group(1)
                        if str(lem) == 'None':
                                lem = word.strip(miscexcl).lower()
                        flex = lemf.group(3)
                        if str(flex) == 'None':
                            flex = ''
                        flex = flex.strip('}')
                    else: #fix for bad parsing
                        lem = word.strip(miscexcl).lower()
                        flex = ''
                        
                else:
                    lem = word.strip(miscexcl).lower()
                    flex = ''
    
                lex = ''.join(morph[z].split('+')[1]).strip()
                #print(lex)
                gram = ' '.join(morph[z].split('+')[1:]).replace('open', '').replace(lex, '').strip()
                res = str(sn) + '\t' + str(wn) + '\t' + '' + '\t' + graph + '\t' + word.strip(miscexcl) + '\t' + '' + '\t' + str(nvars) + '\t' + str(lemcnt) + '\t' + str(nvar) + '\t' + lem + '\t' + '' + '\t' + '' + '\t' + lex + '\t' + gram + '\t' + flex + '\t' + '' + '\t' + punctr + '\t' + sent_pos   
                prs.write(res + '\n')
    
        else:
            lemcnt = 1
            nvars = '?'
            nvar = '?'
            lex = '?'
            gram = '?'
            res = str(sn) + '\t' + str(wn) + '\t' + '' + '\t' + graph + '\t' + word.strip(miscexcl) + '\t' + '' + '\t' + str(nvars) + '\t' + str(lemcnt) + '\t' + str(nvar) + '\t' + word.strip(miscexcl).lower() + '\t' + '' + '\t' + '' + '\t' + lex + '\t' + gram + '\t' + '' + '\t' + '' + '\t' + punctr + '\t' + sent_pos
            prs.write(res + '\n')                   

        return 0

        

                
    
    def meta_data(): #writting prs meta-info  
        ln = '#meta.docid\t' + str(gcnt) + '\n' + '#meta.author\t%s\n#meta.title\t%s\n#meta.date\t%s\n#meta.genre\t%s\n#meta.words\t%s\n#meta.sentences\t%s\n#meta.date_displayed\t%s\n'
        prs.write(ln % tuple(meta))

    #MAYBE ADD IF - ELSE HERE FOR DISTINGUISH BETWEEN XML AND TXT BRANCHES. IF SO, ADD ANOTHER 1 OR 0 ARG FOR THE EXTENSION AS IN GET_DATA() FUNC TO THE SENT() FUNC
        
    ppath = path.split('\\')
    ppath.pop()
    ppath.append(meta[1] + '.prs')
    prs = open('\\'.join(ppath), 'w', encoding='UTF-8') #creating and openning current text's prs
    prs.write('#sentno\t#wordno\t#lang\t#graph\t#word\t#indexword\t#nvars\t#nlems\t#nvar\t#lem\t#trans\t#trans_ru\t#lex\t#gram\t#flex\t#punctl\t#punctr\t#sent_pos\n')
    
    sentlist = re.split('(\.|\!|\?)', text)
    if sentlist[-1] not in excl:
        sentlist.pop()
    #print(sentlist)
    scnt = len(sentlist)//2
    meta.insert(-1, scnt)
    meta_data() #getting current text's meta

    sentind = 0 #sentence index for prs
    for i in range(len(sentlist)): #iterating each sentence of the text
        if sentlist[i] not in excl:
            sentind += 1
            rawcursent = re.sub('([\w])(,|:|;|--)([\w])', '\\1\\2 \\3', sentlist[i])
            rawcursent = re.sub('([\w])([A-Z])', '\\1 \\2', rawcursent)
            rawcursent = re.sub('<REMARQUE>(.*?)</REMARQUE>', '', rawcursent)
            cursent = rawcursent.lstrip(' ').split()
            try:
                cursent[-1] = cursent[-1] + sentlist[i+1] #getting #punctr
            except:
                continue
            #print(cursent)
            l = len(cursent)
            for t in range(l): #iterating each word of the sentence
                wd(cursent[t], sentind, t+1, l)
                print('\n')
                
        
        
    

def get_data(f, t): #t = 0 - xml, t = 1 - txt. getting plain text and meta info
    global textcheck
    inptext = open(f, 'r', encoding='UTF-8').read()
    meta = []
    if t == 0:
        rawtext = textreg.findall(inptext)
        text = re.sub('(\n|\r)', '', ''.join(rawtext))
        text = re.sub('<REMARQUE>(.*?)</REMARQUE>', '', text)
        author = autreg.findall(inptext)
        meta.append(''.join(author))
        meta.append(f.split('\\')[7][:-4])
        textcheck.append(f.split('\\')[7][:-4])
        date = datereg.findall(inptext)
        meta.append(''.join(date))
        genre = genrereg.findall(inptext)
        meta.append(''.join(genre))
        wcnt = wcntreg.findall(inptext)
        meta.append(''.join(wcnt))
        meta.append(''.join(date)) #display date
        
        return text.rstrip('\t'), meta, f
    

def get_dirs(): #getting authors list
    out = []
    for root, dirs, fl in os.walk(sketch):
        for d in dirs:
            out.append(d)
    return out

def get_f(au):
    global autcheck
    global textcheck
    for d in au:
        #if d not in autcheck: #indend here for author-walk method
        if 'Phillip Massinger' in d: #PUT NAME OF THE AUTHOR NEEDED HERE. SELECTIVE AUTHOR METHOD HERE
            for root, dirs, fl in os.walk(sketch + '\\' + d):
                for f in fl:
                    print('\n\n\n', f.upper())
                    if '.xml' in f:
                        if f[:-4] not in textcheck:
                            #print(f[:-4])
                            text = get_data(sketch + '\\' + d + '\\' + f, 0)
                            sent(text[0], text[1], text[2])
                            textcheck.append(f[:-4])
                        else:
                            continue
                    elif '.txt' in f: #TXT BRANCH
                        continue
                        #text = get_data(sketch + '\\' + d + '\\' + f, 1)
                        #sent(text)
                    
            autcheck.append(d)   
        

aut = get_dirs() #full set of authors
get_f(aut)

##p = sketch + "\\George Chapman\\Monsieur D'Olive.xml"
##data = get_data(p, 0)
##sent(data[0], data[1], data[2])
