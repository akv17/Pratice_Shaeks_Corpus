# Pratice_Shaeks_Corpus
ссылка на архив с выходными данными морфолог. парсера, копиями сделанных мной prs и исходными текстами:
https://yadi.sk/d/Lg8vJi-dwyhew

в папке MORPH - все данные морфолог. парсинга. есть аутпуты парсеры для всех (почти всех) xml текстов. 

в папке XML+PRS - все исходные тексты + prs-файлы (моего производства, без данных о синтакс. разметке) для некоторых авторов, которых успел обработать.

prsparse1.py - для создания prs-файла. на данный момент работает только с xml. к сожалению, времени хватило только на отладку xml, потому что очень часто новый текст приносил новый вылет, вызванный помарками в оформлении исходных файлов или еще чем-нибудь новым. в общем, пришлось потратить очень много времени на отладку механизма только для xml. каждого автора я обрабатывал отдельно (ввиду бессмыслия прохода по всем из-за большого количества вылетов), но оставил в коде примерную схему того, как проходить сразу по всем авторам, правда не проверял ее работоспособность.

morph_parse.py - приведение аутпута морфолог. парсера в нужный вид. обязательная процедура для каждого автора. опять же работал для каждого автора отдельно, но можно быстро поправить на проход по всем. можно запускать из корня в папке MORPH (там этот .py продублирован).
 
в папке MORPH - все данные морфолог. парсинга. есть аутпуты парсеры для всех (почти всех) xml текстов. 

СХЕМА РАБОТЫ: МЕТОД ОБРАБОТКИ ОДНОГО ОПРЕДЕЛЕННОГО АВТОРА
- с помощью morph_parse.py привести к нужному виду всю морфологию текущего автора (нужно лишь вставить его имя в переменную aut и запустить скрипт)
- далее запустить prsparse1.py и вставить имя этого же автора в ветвление в ф-ии get_f(au). там будут маркеры, куда вставлять. далее можно запускать скрипт

Автоматизировать весь процесс с помощью os.walk даже не пытался, потому что, опять же, возникало слишком много вылетов, которые нужно было исправлять и тестировать.
