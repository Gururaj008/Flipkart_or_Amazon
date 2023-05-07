import streamlit as st
import plotly.express as px
import math
import bs4
from bs4 import BeautifulSoup
from collections import OrderedDict
import urllib.request as url
import pandas as pd
import re


flip_list = list()
link = list()
global title_flip,o_f, s_f, dis_f, path_1

def flipkart(product):
    try:
        path_1 = f'https://www.flipkart.com/search?q={product}'
        print(path_1)
        link.append(path_1)
        response = url.urlopen(path_1)
        source = bs4.BeautifulSoup(response)
        # print('From flipkart')
        # print(source)
        title_flip = source.find('div', class_='_4rR01T')
        s_price = source.find('div', class_='_30jeq3 _1_WHN1')
        print(f'From Flipkart {s_price}')
        if s_price == None:
            s_price = source.find('div', class_='_30jeq3')
            print(f'From Flipkart {s_price}')
        o_price = source.find('div', class_='_3I9_wc _27UcVY')
        if o_price == None:
            o_price = source.find('div', class_='_3I9_wc')

        s_1 = s_price.text
        o_1 = o_price.text
        # print(f'from FLIPKART - {s_1}')
        # print(f'from FLIPKART - {o_1}')
        s_f = re.sub('[^0-9]',"",s_1)
        o_f = re.sub('[^0-9]',"",o_1)
        print(f'from FLIPKART selling price- {s_f}')
        print(f'from FLIPKART original price- {o_f}')
        s_f = int(s_f)
        o_f = int(o_f)
        dis_f = ((o_f-s_f)/o_f)*100
        dis_f = math.floor(dis_f) 
        if s_f == None or o_f == None:
            print(':red[** NO SUCH PRODUCT**]') 
        else:
            flip_list.append(int(o_f))
            flip_list.append(int(s_f))
            flip_list.append(int(dis_f))
    except:
        st.markdown(':red[**NO SUCH PRODUCT IN FLIPKART**]')

amaz_list = list()
global title_amz, o_a, s_a, dis_a, path_2
def amazon(product):
    try:
        path_2 = f'https://www.amazon.in/s?k={product}'
        link.append(path_2)
        response = url.urlopen(path_2)
        source = bs4.BeautifulSoup(response)
        title_amz = source.find('span', class_='a-size-medium a-color-base a-text-normal')
        s_price = source.find('span', class_='a-price-whole')
        o_price = source.find('span', class_='a-offscreen')
        #o_1 = o_1.find('span')
        s_1 = s_price.text
        o_1 = o_price.text
        print(f'From Amazon selling price - {s_1}')
        print(f'From Amazon original price - {o_1}')
        s_1 = re.sub('[^0-9]',"",s_1)
        o_a = re.sub('[^0-9]',"",o_1)
        print(f'From Amazon - {o_a}')
        s_a = int(s_1)
        o_a = int(o_a)
        dis_a = ((o_a-s_a)/o_a)*100
        dis_a = math.floor(dis_a)
        if s_a == None or o_a == None:
            print(':red[** NO SUCH PRODUCT]')
        else:
            amaz_list.append(int(o_a))
            amaz_list.append(int(s_a))
            amaz_list.append(int(dis_a))
    except:
        st.markdown(':red[**NO SUCH PRODUCT IN AMAZON**]')

def make_df():
    print('-'* 80)
    print(flip_list)
    print(amaz_list)
    display=[]
    display.append(flip_list)
    display.append(amaz_list)
    import pandas as pd
    df = pd.DataFrame(display)
    df = df.rename(columns ={0:'Original price',1:'Selling price',2:'% Discount offered'}, index={0:'FLIPKART',1:'AMAZON'})
    #df1 = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    #df1.set_properties(**{'text-align': 'center'})
    return df

if __name__=='__main__':
    st.title(':blue[Suggesting customer where to buy a ]')
    st.title(':blue[specific product(Flipkart or Amazon)]')
    col1,col2 = st.columns(2, gap='medium')
    with col1:
        st.subheader(':orange[About the project]')
        st.markdown('<div style="text-align: justify">The Indian e-commerce industry has been driven by increasing mobile phone adoption and is estimated to be $75 billion in 2022 and has the potential to expand up to $111 billion by 2024 and $200 billion by 2026. Amazon and Flipkart account for more than 60 percent of the Indian e-commerce market. The offers and discounts offered by each of them vary based on the festive season and special sale on specific date and time.</div>', unsafe_allow_html=True)
        st.write('')
        st.markdown('<div style="text-align: justify">The primary aim of this project is to help customer buy a specific product from the e-commerce market places like Flipkart and Amazon. The suggestion made is based on the selling price of the product and the amount of discount offered so that the customer ends up spending less on buying the product.  </div>', unsafe_allow_html=True)
        st.write('')
        st.subheader(':orange[About the developer]')
        st.write('')
        st.markdown('<div style="text-align: justify">Gururaj H C is passionate about Machine Learning and fascinated by its myriad real world applications. Possesses work experience with both IT industry and academia. Currently pursuing “IIT-Madras Certified Advanced Programmer with Data Science Mastery Program” course as a part of his learning journey.  </div>', unsafe_allow_html=True)
    with col2:
        st.subheader(':orange[Get the suggestion]')
        st.write()
        prod = st.text_input('**Enter a product of your choice**','')
        #product = prod
        product = prod.replace(" ","%20")
        st.markdown(':red[:** PLEASE TYPE ONLY RELEVANT PRODUCT NAMES**]')
        st.markdown('<div style="text-align: justify">As FLIPKART and AMAZON populate their page with some product regardless of the search text you typed above matching the exact product. The results displayed here are totally dependent on what shows up on the respective webpages.  </div>', unsafe_allow_html=True)
        st.write('')
        st.write('')
        if st.button('Fetch the details'):
                st.write('Hang on......')
                flipkart(product)
                amazon(product)
                dataframe = make_df()
                if dataframe.isnull().sum().sum() > 0:
                    st.markdown(":red[**Sorry! No such product....**]")
                
                else:
                    try:
                        st.table(dataframe)
                        st.markdown(':red[*Prices mentioned are in INR]')
                        y_axis = [x for x in dataframe.index]
                        fig=px.bar(dataframe,x='Selling price',y=y_axis, orientation='h',width=425, height = 250,color='% Discount offered').update_layout(xaxis_title="Selling price of the product", yaxis_title="e- commerce store")
                        st.write(fig)
                        if (dataframe['Selling price']['FLIPKART'])<(dataframe['Selling price']['AMAZON']):
                            diff = abs((dataframe['Selling price']['FLIPKART']) - (dataframe['Selling price']['AMAZON']))
                            st.markdown(f"Buy {prod} from :green[**FLIPKART**] as you will save Rs.:green[**{diff}**] on your purchase")
                            st.markdown(':you can use the following link for your purchase:')
                            st.markdown(f'{link[0]}')
                            
                            
                        elif (dataframe['Selling price']['AMAZON'])<(dataframe['Selling price']['FLIPKART']):
                            diff = abs((dataframe['Selling price']['FLIPKART']) - (dataframe['Selling price']['AMAZON']))
                            st.markdown(f"Buy {prod} from :green[**AMAZON**] as you will save Rs.:green[**{diff}**] on your purchase")
                            st.markdown('You can use the following link for your purchase:')
                            st.markdown(f'{link[1]}') 
                            
                        else:
                            st.markdown(':green[The selling price on **FLIPKART** and **AMAZON** is same]')
                            st.markdown('Use any of the following link for your purchase')
                            st.markdown(f'{link[0]}')
                            st.markdown(f'{link[1]}')
                    except:
                        st.write('')
    st.divider()
    col3, col4, col5 = st.columns(3)
    with col4:
        st.markdown('_An effort by_ :blue[**MAVERICK_GR**]')
    st.markdown(':green[**DEVELOPER CONTACT DETAILS**]')
    st.markdown(":orange[email id:] gururaj008@gmail.com")
    st.markdown(":orange[Personal webpage hosting other Datascience projects :] http://gururaj008.pythonanywhere.com/")
    st.markdown(":orange[LinkedIn profile :] https://www.linkedin.com/in/gururaj-hc-machine-learning-enthusiast/")
    st.markdown(":orange[Github link:] https://github.com/Gururaj008 ")
    
     
                        
