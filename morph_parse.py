import os

aut = 'Phillip Massinger' #PUT NAME OF AUTHOR NEEDED HERE
nm = []

for root, dr, fl in os.walk('C:\\Users\\Artem\\Desktop\\pr\\outpt\\MORPH\\'): #or ('.') if in root
    if aut in root:
        for el in fl:
            if 'M_' not in el:            
                nm.append(el)



print(nm)    

for ln in nm:
    f = open('C://Users//Artem//Desktop//pr//outpt//MORPH//' + aut + '//' + ln, 'r').read().split()
    f_out = open('C://Users//Artem//Desktop//pr//outpt//MORPH//' + aut + '//M_' + ln, 'w')
    d = {}
    symb = '&/{'
    check = []
    for i in range(len(f)):
        #print(i)
        if f[i][0] not in symb and f[i] not in check:
            check.append(f[i])
            trig = False #dictionary += trigger
            #print('main el=', f[i])
            #print(check)
            for z in range(i+1, len(f)):
                #print('sub el', f[z])
                if f[z][0] == '+':
                    #print('addin')
                    if trig == False:
                       d[f[i]] = f[z] + ' '
                       trig = True
                    elif trig == True:
                        #print('trigerrin')
                        d[f[i]] += f[z] + ' '
                        
                elif f[z][0] == '&':
                    #print('addin')
                    if trig == False:
                       d[f[i]] = f[z] #+ ' '
                       trig = True
                    elif trig == True:
                        #print('trigerrin')
                        d[f[i]] += f[z] #+ ' '
                        
                elif f[z] == f[i]:
                    #print('equal')
                    continue
                elif f[z][0] not in symb:
                    #print('escape', 'escapin el=', f[z])
                    #d[f[i]] = d[f[i]].rstrip(' ')
                    break

    for el in d:              
        #print(el + ':' , d[el], '\n')
        f_out.write(el.replace('\n', '') + ':' + d[el].rstrip(' ') + '\n')
    f_out.close()    
    print('done')    
              
print('final done')    
    
        
