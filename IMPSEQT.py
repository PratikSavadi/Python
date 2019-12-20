import pandas as pd
import re
import datetime
import os
import zipfile
# df = pd.read_excel('/home/pratik/Documents/BRD equitas/IMPS_UPI/IMPSNTSLEQT010919_1C.xlsx', skiprows=4)


# reqDate = datetime.datetime.strptime(query['statementDate'], '%m-%d-%y')
# reqDate = reqDate.strftime('%d%m%Y')
path = '/home/pratik/Documents/BRD equitas/IMPS_UPI/UPInew/IMPS_191019.zip'
dest = '/home/pratik/Documents/BRD equitas/IMPS_UPI/IMPS/'
with zipfile.ZipFile(path, 'r') as zf:
    listOfFileNames = zf.namelist()
    for fileName in listOfFileNames:
        if fileName.endswith('.xlsx'):
            zf.extract(fileName, dest)
reqDate = listOfFileNames[0].split('_')[0][-6:].strip()
if os.path.exists(dest):
    files = os.listdir(dest)
    file = [i for i in files if re.match('[A-Z]{11}[0-9]{6}_[0-9]{1}C', i)]
else:
            print("no execution found")
# df2=pd.DataFrame()
# files = ['IMPSNTSLEQT010919_1C.xlsx']

for a in file:
        newPath = '/usr/share/nginx/smartrecon/mft/'
        df = pd.read_excel(dest + a, skiprows=4)
        df["cycle"] = a.split('.')[0].split('_')[-1]
        cycle=df["cycle"].unique()
        df2=df[df['Description'].isin(['Remitter P2A Approved Fee', 'Remitter P2A Approved NPCI Switching Fee'])]
        if len(df2) :
            df_feeRem = df2.copy()
            df_feeRem['Remarks'] = 'Fee'
            df_feeRem = df_feeRem.groupby(['Remarks'], as_index=False)['Debit'].sum()
            df_feeRem.rename(columns={'Debit':'Dr'},inplace=True)
            df_feeRem = df_feeRem.assign(
                **{'Narration': 'IMPS REM P2A APP Fee-'+df["cycle"]+'-DT' + reqDate, 'Cr': 0, 'Ac Name': 'IMPS EXPENSES',
                   'GL AC': '404210010'})
        else:
            df_feeRem=pd.DataFrame()

        df2 = df[df['Description'].isin(['Remitter P2A Approved Fee GST','Remitter P2A Approved NPCI Switching Fee GST'])]
        if len(df2):
            df_feegstRem=df2.copy()
            df_feegstRem['Remarks']= 'Fee'
            df_feegstRem=df_feegstRem.groupby(['Remarks'],as_index=False)['Debit'].sum()
            df_feegstRem.rename(columns={'Debit':'Dr'},inplace=True)
            df_feegstRem = df_feegstRem.assign(
                **{'Narration': 'IMPS REM P2A APP Fee IGST-'+df["cycle"]+'-DT'+ reqDate, 'Cr': 0, 'Ac Name': 'IGST RECOVERY -  Flex',
                   'GL AC': '114070217'})
        else:
            df_feegstRem=pd.DataFrame()

        df2 = df[df['Description'].isin(['Remitter P2A Approved Transaction Amount'])]
        if len(df2):
            df_sumRem=df2.copy()
            df_sumRem = df_sumRem.assign(
                **{'Narration': 'IMPS REM P2A APP Txn Amt-'+df["cycle"]+'-DT'+ reqDate, 'Cr': 0, 'Ac Name': 'IMPS Outward Settlement A/c',
                   'GL AC': '200000508888'})
            df_sumRem.rename(columns={'Debit':'Dr'},inplace=True)
            df_sumRem.drop(['Description','No of Txns','Credit'],inplace=True,axis=1)
        else:
            df_sumRem = pd.DataFrame()


        df2 = df[df['Description'].isin(['Remitter P2A-08 Approved Fee', 'Remitter P2A-08 Approved NPCI Switching Fee'])]
        if len(df2):
            df_feeP208Rem=df2.copy()
            df_feeP208Rem['Remarks'] = 'Fee'
            df_feeP208Rem = df_feeP208Rem.groupby(['Remarks'], as_index=False)['Debit'].sum()
            df_feeP208Rem.rename(columns={'Debit':'Dr'},inplace=True)
            df_feeP208Rem = df_feeP208Rem.assign(
                **{'Narration': 'IMPS REM P208 APP Fee-'+df["cycle"]+'-DT'+ reqDate, 'Cr': 0, 'Ac Name': 'IMPS EXPENSES',
                   'GL AC': '404210010'})
        else:
            df_feeP208Rem = pd.DataFrame()

        df2 = df[df['Description'].isin(['Remitter P2A-08 Approved Fee GST','Remitter P2A-08 Approved NPCI Switching Fee GST'])]
        if len(df2):
            df_feegstP208Rem=df2.copy()
            df_feegstP208Rem['Remarks']= 'Fee'
            df_feegstP208Rem=df_feegstP208Rem.groupby(['Remarks'],as_index=False)['Debit'].sum()
            df_feegstP208Rem.rename(columns={'Debit':'Dr'},inplace=True)
            df_feegstP208Rem = df_feegstP208Rem.assign(
                **{'Narration': 'IMPS Remitter P2A-08 APP Fee IGST-'+df["cycle"]+'-DT'+ reqDate, 'Cr': 0, 'Ac Name': 'IGST RECOVERY -  Flex',
                   'GL AC': '114070217'})
        else:
            df_feegstP208Rem = pd.DataFrame()

        df2 = df[df['Description'].isin(['Remitter P2A-08 Approved Transaction Amount'])]
        if len(df2):
            df_sumP208Rem=df2.copy()
            df_sumP208Rem = df_sumP208Rem.assign(
                **{'Narration': 'IMPS REM P2A APP Txn Amt-'+df["cycle"]+'-DT'+ reqDate, 'Cr': 0, 'Ac Name': 'IMPS Outward Settlement A/c',
                   'GL AC': '200000508888'})
            df_sumP208Rem.rename(columns={'Debit':'Dr'},inplace=True)
            df_sumP208Rem.drop(['Description','No of Txns','Credit'],inplace=True,axis=1)
        else:
            df_sumP208Rem = pd.DataFrame()

        df2 = df[df['Description'].isin(['Beneficiary MRT Approved Fee'])]
        if len(df2):
            df_feeBenf = df2.copy()
            df_feeBenf = df_feeBenf.assign(
                **{'Narration': 'IMPS BEN MRT APP Fee-'+df["cycle"]+'-DT'+ reqDate, 'Dr': 0, 'Ac Name': 'IMPS INCOME',
                   'GL AC': '302210201'})
            df_feeBenf.rename(columns={'Credit':'Cr'},inplace=True)
            df_feeBenf.drop(['Description','No of Txns','Debit'],inplace=True,axis=1)
        else:
            df_feeBenf = pd.DataFrame()

        df2 = df[df['Description'].isin(['Beneficiary MRT Approved Fee GST'])]
        if len(df2):
            df_feegstBenf = df2.copy()
            df_feegstBenf = df_feegstBenf.assign(
                **{'Narration': 'IMPS BEN MRT APP Fee GST-'+df["cycle"]+'-DT'+ reqDate, 'Dr': 0, 'Ac Name': 'GST LIABILITY- Flex',
                   'GL AC': '208080261'})
            df_feegstBenf.rename(columns={'Credit':'Cr'},inplace=True)
            df_feegstBenf.drop(['Description','No of Txns','Debit'],inplace=True,axis=1)
        else:
            df_feegstBenf = pd.DataFrame()

        df2 = df[df['Description'].isin(['Beneficiary MRT Approved Transaction Amount'])]
        if len(df2):
            df_sumBenf= df2.copy()
            df_sumBenf = df_sumBenf.assign(
                **{'Narration': 'IMPS BEN MRT APP Txn Amt-'+df["cycle"]+'-DT'+ reqDate, 'Dr': 0, 'Ac Name': 'IMPS Inward Settlement A/c',
                   'GL AC': '200000508890'})
            df_sumBenf.rename(columns={'Credit':'Cr'},inplace=True)
            df_sumBenf.drop(['Description','No of Txns','Debit'],inplace=True,axis=1)
        else:
            df_sumBenf = pd.DataFrame()

        df2 = df[df['Description'].isin(['Beneficiary P2A Approved Fee'])]
        if len(df2):
            df_feeP208Benf = df2.copy()
            df_feeP208Benf = df_feeP208Benf.assign(
                **{'Narration': 'IMPS BEN P2A APP Fee-'+df["cycle"]+'-DT'+reqDate, 'Dr': 0, 'Ac Name': 'IMPS INCOME',
                   'GL AC': '302210201'})
            df_feeP208Benf.rename(columns={'Credit':'Cr'},inplace=True)
            df_feeP208Benf.drop(['Description','No of Txns','Debit'],inplace=True,axis=1)
        else:
            df_feeP208Benf = pd.DataFrame()

        df2 = df[df['Description'].isin(['Beneficiary P2A Approved Fee GST'])]
        if len(df2):
            df_feegstP208Benf = df2.copy()
            df_feegstP208Benf = df_feegstP208Benf.assign(
                **{'Narration': 'IMPS BEN P2A APP Fee GST-'+df["cycle"]+'-DT'+ reqDate, 'Dr': 0, 'Ac Name': 'GST LIABILITY- Flex',
                   'GL AC': '208080261'})
            df_feegstP208Benf.rename(columns={'Credit':'Cr'},inplace=True)
            df_feegstP208Benf.drop(['Description','No of Txns','Debit'],inplace=True,axis=1)
        else:
            df_feegstP208Benf = pd.DataFrame()

        df2 = df[df['Description'].isin(['Beneficiary P2A Approved Transaction Amount'])]
        if len(df2):
            df_sumP208Benf= df2.copy()
            df_sumP208Benf = df_sumP208Benf.assign(
                **{'Narration': 'IMPS BEN P2A APP Txn Amt-'+df["cycle"]+'-DT'+ reqDate, 'Dr': 0, 'Ac Name': 'IMPS Inward Settlement A/c',
                   'GL AC': '200000508890'})
            df_sumP208Benf.rename(columns={'Credit':'Cr'},inplace=True)
            df_sumP208Benf.drop(['Description','No of Txns','Debit'],inplace=True,axis=1)
        else:
            df_sumP208Benf = pd.DataFrame()

        df2 = df[df['Description']=='Beneficiary/Remitter Sub Totals']
        if len(df2):
            df_settlAmt=  df2.copy()
            df_settlAmt.loc[len(df_settlAmt),'Description']='Settlement Amount'


        #  Assuming Settlement Amount is havung one row in description.So we have taken value of 0th index of debit and credit,
        #  if cr > dr then dr-cr and result will be under cr column
            df_settlAmt.loc[df_settlAmt['Description'] == 'Settlement Amount','Cr'] = df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] -df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] if df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] >df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] else '0'
            df_settlAmt.loc[df_settlAmt['Description'] == 'Settlement Amount','Dr'] = df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] -df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] if df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] >df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] else '0'
            df_settlAmt = df_settlAmt.assign(
                **{'Narration': 'IMPS Final settlement-'+df["cycle"]+'-DT'+'reqDate', 'Ac Name': 'RTGS SETTLEMENT ACCOUNT WITH RBI',
                   'GL AC': '110040003'})
            df_settlAmt.drop(df_settlAmt.index[[0]],inplace=True)
            df_settlAmt.drop(['Description','No of Txns','Debit','Credit'],inplace=True,axis=1)
        else:
            df_settlAmt = pd.DataFrame()

        dfnew=df_feeRem.append([df_feegstRem,df_sumRem,df_feeP208Rem,df_feegstP208Rem,df_sumP208Rem,df_feeBenf,df_feegstBenf,df_sumBenf,df_feeP208Benf,
                                  df_feegstP208Benf,df_sumP208Benf,df_settlAmt]).reset_index(drop=True)
        del [df_feeRem,df_feegstRem,df_sumRem,df_feeP208Rem,df_feegstP208Rem,df_sumP208Rem,df_feeBenf,df_feegstBenf,df_sumBenf,df_feeP208Benf,
                                  df_feegstP208Benf,df_sumP208Benf,df_settlAmt]
        if cycle == '1C':
            df1C= dfnew.copy()
            df1C.drop(['Remarks'],inplace=True,axis=1)
            df1C=df1C[['GL AC','Ac Name','Dr','Cr','Narration']]
            # print df1C


        elif cycle == '2C':
            df2C = dfnew.copy()
            df2C.drop(['Remarks'], inplace=True, axis=1)
            df2C = df2C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
            # print df2C

        elif cycle == '3C':
            df3C = dfnew.copy()
            df3C.drop(['Remarks'], inplace=True, axis=1)
            df3C = df3C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
            # print df3C

        elif cycle == '4C':
            df4C = dfnew.copy()
            df4C.drop(['Remarks'], inplace=True, axis=1)
            df4C = df4C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
            # print df4C

        dfs = {}
        if len(df1C):
            dfs['IMPSNTSLEQT_1C'] = df1C
            for a in dfs:
                dfs[a].to_csv('/tmp/' + i + '.csv', index=False)
                print dfs[a]

        if len(df2C):
            dfs['IMPSNTSLEQT_2C'] = df2C
            for b in dfs:
                dfs[b].to_csv('/tmp/' + i + '.csv', index=False)
                print dfs[b]
        if len(df3C):
            dfs['IMPSNTSLEQT_3C'] = df3C
            for c in dfs:
                dfs[c].to_csv('/tmp/' + i + '.csv', index=False)
        if len(df4C):
            dfs['IMPSNTSLEQT_4C'] = df4C

            for d in dfs:
                dfs[d].to_csv('/tmp/' + i + '.csv', index=False)





