import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text="MS Dhoni probably ranks as the third-most popular Indian cricketer ever, behind only Sachin Tendulkar and Virat Kohli. He emerged from a cricketing backwater, the eastern Indian state of Jharkhand, and made it to the top with a home-made batting and wicketkeeping technique, and a style of captaincy that scaled the highs and hit the lows of both conservatism and unorthodoxy. Under Dhoni's leadership, India won the top prize in all formats: leading the Test rankings for 18 months starting December 2009, winning the 50-over World Cup in 2011, and the T20 world title on his captaincy debut in 2007.He seemingly emerged fully formed at 23, when he blasted two centuries in a triangular 50-over tournament for India A in Nairobi. Long-haired and fearless, he soon swaggered into international cricket, and became an instant darling of the crowds with ODI innings of 148 and 183 not out within a year of his debut.Dhoni improvised abd learned, but he didn't apologise for his batting style, which was not the most elegant."

def summariser(rawdocs):
        stopwords=list(STOP_WORDS)
        # print(stopwords)
        nlp=spacy.load("en_core_web_sm")
        #smallest module of spacy

        doc=nlp(rawdocs)
        # print(doc)
        #now we create tokens
        tokens=[token.text for token in doc]
        # print(tokens)
        word_freq={}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text]=1
                else :
                    word_freq[word.text]+=1
        # print(word_freq)
        # prints the map freq of concerned words
        max_freq=max(word_freq.values())
        # print(max_freq)
        # max freq of word
        for word in word_freq.keys():
            word_freq[word]=word_freq[word]/max_freq
        # normalized frequnecy
        # print(word_freq)

        sent_tokens=[sent for sent in doc.sents]
        # print(sent_tokens) we create sentence tokens here sentence becomes list elementts

        sent_scores={}
        for sent in sent_tokens:
            for word in sent:
                if word.text in word_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent]=word_freq[word.text]
                    else :
                        sent_scores[sent]+=word_freq[word.text]
        # print(sent_scores)
                        
        select_len=int(len(sent_tokens)* 0.3)
        # print(select_len)
        # 30% of total sentences 
        summary=nlargest(select_len,sent_scores,key=sent_scores.get)
        print(summary)
        final_summary=[word.text for word in summary]
        summary=' '.join(final_summary)
        return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))