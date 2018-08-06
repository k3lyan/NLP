from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBox, LTChar, LTTextLine
from wrapper_pdf import PdfMinerWrapper
import sys
import os
import re
import langid
from langid.langid import LanguageIdentifier, model
import random
from random import uniform


def language_detect(text,identifier):
    identifier.set_languages(['fr','en'])
    return identifier.classify(text)

def extract_full_pdf():
    # Declaration of the regular expressions used later
    regexp_ann={'annexe_fr_maj': r"(ANNEX+)", 'annexe_fr': r"(Annex+)",'APPENDIX':r"(APPENDIX+)", 'annexe_en': r"(Appendix+)", 'annexe_A': r"(ANNEXE A.+)",\
     'appendices': r"(Appendices+)"}
    regexp_non_ann={'cf_annexe': r"(cf annexe+)",'cf._annexe': r"(cf. annexe+)", 'ement_annexe': r"(ement annexe+)", 'annexe_six': r"(annexe 6+)",\
    'annexe_l': r"(sur l’annexe+)", 'annexe_o': r"(annexe au+)",'ann_5': r"(le tableau de l’annexe 5+)",'annexe_pages2': r"(annexe 2 pages 4+)",  \
    'parties_annexe': r"(parties annexe+)",'annexe_8': r"(annexe 8+)", 'annexe_cf3': r"(cf annexe 3+)", 'annexe_g': r"(appendix g+)",\
    'expose_annexe': r"(exposée en annexe+)",'para_annexe': r"( annexes+)", 'en2_annexe': r"(en  annexe+)", 'annexe3': r"(annexe 3+)", 'annexe_couts': r"(Annexes : Co+)", \
    'appendix_2': r"(appendix 2: oc+)", 'appendix_3': r"(appendix 3: list+)",'ann_3': r"(cf. annexe 3+)", 'annexe_pages': r"(annexe 2 pages 7+)", \
    'pmp_annexe': r"(cf. pmp appendix+)",'app_annexe': r"(voir appendix 2+)", 'd_annexe': r"(d'annexe de+)", 'annexe_f': r"(annexe f+)", \
    'appendix_1': r"(appendix 1: project+)", 'vannexe_2': r"(voir annexe 2 +)", 'annexe_de_securite': r"(d’annexe de sécurité+)",\
    'annexes_couts': r"(annexes: coû+)", 'annexe_presente': r"(annexe 4 présente+)", 'appendix_c': r"(appendix c+)", 'dans_annexe': r"(dans l’annexe+)",\
    'vannexeb' : r"(voir annexe b+)",\
    'annexes_e': r"(annexe e+)", 'annexe_6': r"(voir annexe 6+)", 'annexe_fmc': r"(new fmc annex+)", 'annexe_fmc': r"(voir appendix 1+)", \
    'annc' : r"(annexe c+)",'anne_b': r"(cf annexe b+)",\
    'annexes_b': r"(voir annexe b+)", 'annexe_b2': r"(il est joint en annexe b+)", 'annexe_4': r"(annexe 4+)", 'annexe_4': r"(annexe \[2\]+)", \
    'annexe_comm': r"(pour  tous  les  sujets  communs+)",\
    'annexes_une': r"(une annexe+)", 'annexe_5': r"(annexe 5.+)", 'annexe_de': r"(annexes de+)", 'ann_b': r"(cf. Annexe B+)", 'cfann3' : r"(cf. annexe 3+)",\
    'annex_g' : r"(annexe g+)",'annexe_monde': r"(dans le monde. l’annexe+)",'annexes_9': r"(annexe 9 présente+)",'annex_7': r"(annexe 7+)",\
    'annexes_une': r"(l’annexe 1b+)", 'annexes_3': r"(cf annexe 3+)", 'annexes_b': r"(cf. annexe b+)", 'annexe_12': r"(annexe 12+)",\
    'annexes_quatre': r"(annexe iv donne+)", 'annexes_avion': r"(concerne la fourniture à dassault d'une suite avionique civile+)",\
    'voir_annexe': r"(voir annexe+)", 'en_annexe': r"(en annexe+)", 'l_annexe': r"(l'annexe+)", 'sur_l_annexe': r"(sur l'annexe+)", \
    'anne_exe':r"(cf anne exe a+)",'pmp_app':r"(pmp appendix g+)", 'ann_7' : r"(annexe 7+)", 'une_ann_sec': r"(l’annexe I présente+)",\
    'une_ann': r"(une annexe+)", 'une_ann_secur': r"(une annexe de sécurité+)", 'une_ann_g': r"(annexe g.+)", 'une_ann_cc': r"(annexé au cctp+)"}
    regexp = {'retour_ligne': r"[\n]",\
     'bold':r"(Bold+)", 'figure': r"(figure+)", 'dot': r"(\.\.\.\.\.\.\.\.)", 'toc_en': r"^(table of content)+",\
     'toc_fr': r"^(table des mati)+", 'sommaire': r"^(sommaire)+",'TDI':r"^(table des illustration)+",'TDA':r"^(tables des ab)+",\
      'liste_annexe':r"^(liste des annexe+)", 'liste_doc':r"^(documents de référence+)", 'glossaire':r"^(glossaire+)"}
    
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    proba_language={'en':0,'fr':0}
    nb_language={'en':0,'fr':0}
    sommaire_trouve=0
    annexe_trouve=0
    bas_de_page_trouve=0
    nb_sommaire=0

    with PdfMinerWrapper(sys.argv[1]) as doc:
        sentences = []
        avant_annexe = True
        print('---------{}---------'.format(sys.argv[1]))
        for p, page in enumerate(doc):
            if (p > 0 and avant_annexe == True and page.pageid < 37):
                print('---PAGE no.{} of pdf {}---'.format(page.pageid,sys.argv[1]))
                y_sommaire = 0
                for tbox in page:
                    if not isinstance(tbox, LTTextBox):
                        continue
                    for obj in tbox:
                        # 51 IS THE LIMIT (Puzenat)
                        if(obj.y0 < 50):
                            bas_de_page_trouve=1
                        if(obj.y0 > 50 and obj.y0 > y_sommaire):
                            bold = False
                            size = False
                            no_figure = True
                            avant_annexe = True
                            somme = 0
                            no_sommaire = True
                            if ((len(re.findall(regexp['dot'], obj.get_text().lower()))+\
                                len(re.findall(regexp['toc_fr'], obj.get_text().lower()))+\
                                len(re.findall(regexp['TDA'], obj.get_text().lower()))+\
                                len(re.findall(regexp['TDI'], obj.get_text().lower()))+\
                                len(re.findall(regexp['liste_doc'], obj.get_text().lower()))+\
                                len(re.findall(regexp['glossaire'], obj.get_text().lower()))+\
                                len(re.findall(regexp['liste_annexe'], obj.get_text().lower()))+\
                                len(re.findall(regexp['sommaire'], obj.get_text().lower()))+\
                                len(re.findall(regexp['toc_en'], obj.get_text().lower())))> 0 and page.pageid<8):
                                no_sommaire = False
                                nb_sommaire+=1
                                y_sommaire = obj.y0
                                sommaire_trouve = 1
                            for i, c in enumerate(obj):
                                if not isinstance(c, LTChar):
                                    continue
                                if (len(re.findall(regexp['bold'], c.fontname)) == 0):
                                    somme += 1
                                    # The all sentence has the same size, if the last character is huger, all the sentence is
                                if c.size > 12:
                                    size = True
                            # If all the characters of the sentence are bold, the sentence is bold
                            if somme == 0:
                                bold = True
                            # If the object is a figure, we don't take it into account
                            if len(re.findall(regexp['figure'], obj.get_text().lower())) > 0:
                                no_figure = False
                            # A title must have a huger font size, be bold and shouldn't be a figure
                            if(no_figure and page.pageid > 34):
                                indic_ann=0
                                indic_non_ann=0
                                for j in regexp_ann.keys():
                                    if (len(re.findall(regexp_ann[j], obj.get_text()))>0):
                                        indic_ann=1
                                for j in regexp_non_ann.keys():
                                    if (len(re.findall(regexp_non_ann[j], obj.get_text().lower()))>0):
                                        indic_non_ann=1
                                if(indic_ann==1 and indic_non_ann==0):
                                    avant_annexe = False
                                    print('ANNEXES REACHED')
                                    annexe_trouve=1

                            val = uniform(0,1)
                            if(val<=0.2 and no_sommaire):
                                l=language_detect(obj.get_text(),identifier)
                                if(l[1]>0.7):
                                    proba_language[l[0]]+=l[1]
                                    nb_language[l[0]]+=1
                            sentences.append({'sentence': re.sub(regexp['retour_ligne'], r"", obj.get_text()),\
                                    'avant_annexe': avant_annexe, 'no_sommaire': no_sommaire})

    # BUILDING PDF FILES
    titre_rapport = sys.argv[1].replace(" ", "_")
    titre_rapport = titre_rapport.replace(".pdf", ".txt")

    # SELECTION TEXTE
    contenu = ""
    avant = True
    for line in range(0, len(sentences)):
        if(not sentences[line]['avant_annexe']):
            avant = False
        if(avant and sentences[line]['no_sommaire']):
            contenu += " " + sentences[line]['sentence']

    print('TEXT TRANSFERED.')

    repertoire=""
    for i in proba_language.keys():
            if(nb_language[i]!=0 and sum(nb_language.values())!=0):
                proba_language[i]=proba_language[i]/nb_language[i]
                nb_language[i]=nb_language[i]/sum(nb_language.values())

    if(nb_language['en']>0.7):
        print("english text with english/french ratio = ")
        print(nb_language['en'])
        print("with average recognition = ")
        print(proba_language['en'])
        print("THIS IS AN ENGLISH TEXT")
        repertoire="english"
        file = open('./{}/{}'.format(repertoire, titre_rapport), "w")
        file.write(contenu)
        file.close()

    # INFOS
    if (sommaire_trouve + annexe_trouve + bas_de_page_trouve == 3):
        print ('sommaie + annexe + bas de page trouvée')
        repertoire="good"
        file = open('./{}/{}'.format(repertoire, titre_rapport), "w")
        file.write(contenu)
        file.close()
    else:
        if (sommaire_trouve ==0):
            print( 'SOMMAIRE NOT FOUND: {}'.format(sys.argv[1]))
            repertoire="sommaire"
            file = open('./{}/{}'.format(repertoire, titre_rapport), "w")
            file.write(contenu)
            file.close()
        if(annexe_trouve ==0):
            print('ANNEXE NOT FOUND: {}'.format(sys.argv[1]))
            repertoire="annexe"
            file = open('./{}/{}'.format(repertoire, titre_rapport), "w")
            file.write(contenu)
            file.close()
        if(bas_de_page_trouve==0):
            print( 'BAS DE PAGE NOT FOUND: {}'.format(sys.argv[1]))
            repertoire="bas"
            file = open('./{}/{}'.format(repertoire, titre_rapport), "w")
            file.write(contenu)
            file.close()
    print("nb de pages sommaire = {}".format(nb_sommaire))

extract_full_pdf()
