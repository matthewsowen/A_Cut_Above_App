import pandas as pd
import numpy as np
from pyzipcode import ZipCodeDatabase
import streamlit as st


'''
# A Cut Above
### Finding the Sharpest Surgeon

'''


MA_Docs = pd.read_csv('MassDocs.csv')

MA_Hosp = pd.read_csv('MassHosp.csv')


st.selectbox('What kind of surgery do you need?',
             ('GI Surgery', 'Lung Surgery'))

ZIP = st.text_input('Please enter your ZIP Code', 
                    max_chars = 5)

radius = st.number_input('Radius (in miles)')

zipdb = ZipCodeDatabase()

in_radius = [z.zip for z in zipdb.get_zipcodes_around_radius(
        ZIP, radius)]

HinZ = []

for i in range(len(MA_Hosp['ZIP Code'])):
    
    if MA_Hosp['ZIP Code'][i][0:5] in in_radius:
        
        HinZ.append(str(MA_Hosp.iloc[i, 2]))
        
    else:
        
        pass


Local_Docs = pd.DataFrame(columns = ['Surgeons', 'Gender', 'Hospitals', 'Problem Rate'])

for d in range(len(MA_Docs['Surgeons'])):
    
    sp = MA_Docs.iloc[d, 3].split(';')
    
    for h in sp:
            
        if h in HinZ:
                
            df = MA_Docs.iloc[d, :]
            Local_Docs = Local_Docs.append(df, ignore_index = True) 
            break
                
        else:
                
            pass
        
Local_Docs.sort_values(by = ['Problem Rate'],
                       inplace = True)



'''
#### Here are the top surgeons in your area!
'''

Local_Docs.set_index('Surgeons', 
                     drop = True, inplace = True)

Local_Docs2 = Local_Docs.replace(to_replace = 
                                 {';[A-Za-z0-9-; ]+':''},
                                 regex = True)

Local_Docs3 = Local_Docs2.replace(to_replace = 
                                 {';':''},
                                 regex = True)

st.table(Local_Docs3.iloc[0:10,0:2])
