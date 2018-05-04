
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


text=open('comment_list.txt', 'r',encoding='utf-8')
mytext=text.read()
cut = jieba.cut(mytext,cut_all=True)
split_cut ='/'.join(cut)
wc = WordCloud(background_color = "white", #设置背景颜色  
               max_words = 2000, #设置最大显示的字数  
               margin=5,
               font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",#不加这一句显示口字形乱码
               max_font_size = 80,  #设置字体最大值  
               random_state = 40, #设置有多少种随机生成状态，即有多少种配色方案  
    )  
mword =wc.generate(split_cut)
plt.imshow(mword)
plt.axis("off")
plt.show()