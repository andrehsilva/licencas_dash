from typing import Text
import streamlit as st
import pandas as pd
import io

buffer = io.BytesIO()
base = "teste"
df = pd.read_csv(base, sep=';')
df = df.drop(columns=['TenantName','TenantId','SchoolId','ComboId','OrderDate','ComboCode','ComboName','LicenceId', 'LicenseStatus', 'Brand'])
df = df.loc[(df['OrderStatus'] == '1') &(df['OrderStatus'] == '1')&(df['Profile']=='Aluno')]
df = df.drop(columns=['Profile','OrderStatus'])
df = df.rename(columns={'SchoolName':'Escola','OrderNumber':'Nº Pedido','LicenceName':'Nome da Licença','TagName':'Segmento',
                        'OrderNumberOfLicenses':'Licenças','LicenceStartDate':'Data de início','LicenceEndDate':'Data de expiração'})




# sidebar
st.sidebar.image('https://static.tildacdn.com/tild6262-3035-4431-b436-326632643236/03_logo_conexia_educ.png', width=300)
st.sidebar.title('Licenças Ativas - LEX')
#st.sidebar.subheader('Licenças Ativas')
escolas = df['Escola'].unique()
options = st.sidebar.multiselect('Selecione as escolas',escolas)


if not options:
    st.info('A base de dados é atualizada semanalmente, todas as segundas')
    st.subheader('Licenças de todas as escolas')
    st.write(df)
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name="Licenças Ativas", index=False)
            writer.save()
            
            st.download_button(
                label="📥 Download",
                data=buffer,
                file_name="Licencas_escolas.xlsx",
                mime="application/vnd.ms-excel"
            )
else:
    for escola in escolas:
        if escola in options:
            #df_escola = df.loc[(df['Escola'] == escola) & (df['Segmento'] == segmentos)]
            df_escola = df.loc[(df['Escola'] == escola)]
            st.subheader(escola)
           
            buffer2 = io.BytesIO()
            with pd.ExcelWriter(buffer2, engine='xlsxwriter') as writer:
                df_escola.to_excel(writer, sheet_name="Licenças Ativas", index=False)
                writer.save()
            
                st.download_button(
                    label="📥 Download",
                    data=buffer2,
                    file_name=escola+".xlsx",
                    mime="application/vnd.ms-excel"
                )

            st.write(df_escola)
