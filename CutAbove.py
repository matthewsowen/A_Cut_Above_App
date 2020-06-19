import pandas as pd
from pyzipcode import ZipCodeDatabase
import streamlit as st


'''
# A Cut Above
### Finding the Sharpest Surgeon

#### Please enter your information to find lung surgeons near you.
'''


L_Docs = pd.read_csv('Lung_Surgeons.csv', index_col = 0)

L_Hosp = pd.read_csv('L_hosps.csv', index_col = 0)



ZIP = st.text_input('ZIP code', 
                    max_chars = 5)

radius = st.number_input(label = 'Radius (in miles)',
                         min_value = 1,
                         max_value = 1000,
                         value = 25,
                         step = None)

zipdb = ZipCodeDatabase()

if len(ZIP) == 5:

    try:
        in_radius = [z.zip for z in zipdb.get_zipcodes_around_radius(ZIP, radius)]
    
    except:
        
        st.write('That doesn\'t appear to be a valid ZIP code!')
    
    else:
        
        HinZ = []
            
        for i in range(len(L_Hosp['ZIP Code'])):
                
            if L_Hosp['ZIP Code'][i][0:5] in in_radius:
                    
                HinZ.append(str(L_Hosp.iloc[i, 0]))
                    
            else:
                    
                pass
            
        
        Local_Docs = pd.DataFrame(columns = ['Surgeons', 'Hospitals', 'Avg Review',
                                                 '% Negative Outcome', 'Class',
                                                 'Predicted Class', 'Rating'])
            
        for d in range(len(L_Docs['Surgeons'])):
                
            sp = L_Docs.iloc[d, 1].split(';')
                
            for h in sp:
                        
                if h in HinZ:
                            
                    df = L_Docs.iloc[d, :]
                    df['Hospital'] = h
                    Local_Docs = Local_Docs.append(df, ignore_index = True) 
                    break
                            
                else:
                            
                    pass
        
        Local_Docs['Average Patient Review'] = list(round(Local_Docs['Avg Review'],1))
            
        Local_Docs.sort_values(by = ['Predicted Class'],
                               inplace = True)
            
            
        
            
        Local_Docs.set_index('Surgeons', 
                             drop = True, inplace = True)
        
        
        
        
        
        #Local_Docs2 = Local_Docs.replace(to_replace = 
                                         #{';[A-Za-z0-9-; ]+':''},
                                         #regex = True)
            
        #Local_Docs3 = Local_Docs2.replace(to_replace = 
                                          #{';':''},
                                          #regex = True)
    
        if Local_Docs.shape[0] != 0:
            
            '''
            #### Here are top the surgeons in your area!
            '''
    
            Local_Docs2 = Local_Docs[['Hospital', 'Rating',
                                  'Average Patient Review']][0:30]
        
            st.table(Local_Docs2.style)
            
        else:
            
            '''
            #### We couldn\'t find any surgeons. Please try a larger radius.
            '''

