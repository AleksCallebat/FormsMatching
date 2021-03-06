import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify,render_template, redirect, url_for

def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
<<<<<<< HEAD
def read_excel(path="Maching.xlsx"):
=======
def read_excel(path):
>>>>>>> 46a78eb107670e2be530f000d240622a5b763970
    xl = pd.ExcelFile(path)
    df = xl.parse("Sheet1")
    print(df.keys())
    return df

def match_ratio(df,df2,i,j):
    ratio=[]
    score=0
    count=0
    if df["Nom"][i]==df2["Nom"][j] :
        return -1
    else :
        for key in df.keys() :
<<<<<<< HEAD
            if key not in df2.keys() and key not in ['Heure de debut', 'Heure de fin', 'Adresse de messagerie', 'Nom','Pour finir, peux-tu nous laisser ton prenom / nom ?']:
                print("WARNING : NOT SAME KEYS",key)
            if key not in ['Heure de debut', 'Heure de fin', 'Adresse de messagerie', 'Nom','Pour finir, peux-tu nous laisser ton prenom / nom ?']:
                count+=1
=======
            if key not in df2.keys():
                print("WARNING : NOT SAME KEYS")
            if key not in ['Heure de début', 'Heure de fin', 'Adresse de messagerie', 'Nom','Pour finir, peux-tu nous laisser ton prénom / nom ?']:
>>>>>>> 46a78eb107670e2be530f000d240622a5b763970
                answer_similarity=[]
                score+=int(df[key][i]==df2[key][j]) 
                try:
                    for answer in df[key][i]:
                        if answer in df2[key][j]:
                            answer_similarity.append(1)
                        else :
                            pass
                            answer_similarity.append(0)
                    for answer in df2[key][j]:
                        if answer in df[key][i]:
                            answer_similarity.append(1)
                        else :
                            pass
                            answer_similarity.append(0)
                    ratio.append(np.mean(answer_similarity))
                except:
                    print("big exception",df[key])
        if score==count:
            print("full match",df["Nom"][i],df2["Nom"][j])
        return float(score)/count
#        return(np.mean(ratio)) 

def seuil(df1,df2,Names,seuil):
    result=[]
    for k in range(len(Names)) : 
        for j in range(len(Names)) :
            matchRatio=match_ratio(df1,df2,k,j)
            if (matchRatio>seuil):
                result.append((Names[k],Names[j],matchRatio))                
                print(Names[k],Names[j],match_ratio(df1,df2,k,j))
    return pd.DataFrame(result)

def get_all_matches(df1,df2):
    if ("Nom" not in df1.columns) or ("Nom" not in df2.columns):
        return(pd.DataFrame({"ERROR : you must use 'Nom' as matching key between dataframes":[]}))
    result_df=pd.DataFrame(columns=["nom1","nom2","score"])
    match_df=pd.DataFrame(columns=["Nom"]+df2["Nom"].tolist())
    #première colonne nom, puis que des colonnes vides
    for i in range(len(df1["Nom"])):
        match_df.loc[i]=[df1["Nom"][i]]+[match_ratio(df1,df2,i,j) for j in range(len(df2["Nom"]))]      

    result_df=match_df

    return result_df

def get_top_matches(df):
    try :
        ## We take into input the dataframe with all the matches and output a very good way of allocating df2 names to df1
        
        #Initialize the three outputs array as empty
        nom1,nom2,score=[],[],[]

<<<<<<< HEAD
    #Create a list with the full arrays that we will empty 
    try:
        nom1_original=df["Nom"].values
    except:
        print("empty array error",df)
    nom2_original=(df.keys().values[1:])

    print("debug 83",df)
    score_original=[df[name].values for name in nom2_original]
    print("debug 84",score_original)
    for j in range(len(df)):        
        if len(nom1_original)<1 or len(nom2_original)<1:
            #STOP whenever all df2 names are allocated
            break
        else :
            score_original=[]
            for name in nom2_original :
                column=[]
                for j in range(len(df)):
                    if df["Nom"].values[j] in nom1_original:
                        column.append(df[name].values[j])
                score_original.append(column)
            #print("new score",len(score_original))
            nom1_temp,nom2_temp,score_temp=[],[],[]

            # first look to take all the argmaxes
            for k in range(len(nom1_original)):    
                i=np.argmax([score[k] for score in score_original])
                print("checksum",len([score[k] for score in score_original]),len(nom2_original))
                
                nom1_temp.append(nom1_original[k])
                nom=nom2_original[i]
                nom2_temp.append(nom)
                score_temp.append(score_original[i][k])
                    
            ### Uncomment if you allow double matches (yes in that case the code should be simple)
            #nom1,nom2,score=nom1_temp,nom2_temp,score_temp            
            #break
            
            #The idea is to keep all the maximum for a df2 max. It won't always give the optimal solution,
            # but close enough ("algorithme glouton")

            nom2_temp_unique=[]
            for k in nom2_temp:
                if k not in nom2_temp_unique:
                    nom2_temp_unique.append(k)

            #Here, we associate values and match for each of the maximums (in nom2_temp(_unique))
            value=dict([(k,0) for k in nom2_temp_unique])
            match=dict([(k,"") for k in nom2_temp_unique])

            for k in range(len(nom2_temp)):
                matcher=nom2_temp[k]
                matched=nom1_temp[k]
                ratio=score_temp[k]
                if ratio>value[matcher] :
                                   
                    value[matcher]=ratio
                    match[matcher]=matched
                else :
                    pass
          
            #Here we count the columns and line that have not found an optimal match, and keep them inside score_original
 

            # Add the validated names to the definitive lists to output

            nom1=np.concatenate((nom1,[match[j] for j in nom2_temp_unique]))
            nom2=np.concatenate((nom2,[k for k in nom2_temp_unique]))
            score=np.concatenate((score,[value[k] for k in nom2_temp_unique]))

            buffer=[]
            for k in nom1_original :
                if k not in nom1:
                    buffer.append(k)
            nom1_original=buffer
            buffer=[]
            for k in nom2_original:
                if k not in nom2:
                    buffer.append(k)
            nom2_original=buffer


    df_top=pd.DataFrame({"nom1":nom1,"nom2":nom2,"score":score})
    return df_top
UPLOAD_FOLDER = 'uploads'
=======
        #Create a list with the full arrays that we will empty 
        nom1_original=df["Nom"].values
        nom2_original=(df.keys().values[1:])
        score_original=[df[name].values for name in nom1_original]


        for j in range(len(df)):
            
            if len(nom1_original)<1 or len(nom2_original)<1:
                #STOP whenever all df2 names are allocated
                break
            else :
                score_original=[]
                for name in nom1_original :
                    column=[]
                    for j in range(len(df)):
                        if df["Nom"].values[j] in nom2_original:
                            column.append(df[name].values[j])
                    score_original.append(column)
                #print("new score",len(score_original))
                nom1_temp,nom2_temp,score_temp=[],[],[]

                # first look to take all the argmaxes
                for k in range(len(nom1_original)):    
                    i=np.argmax(score_original[:][k])
                    
                    nom1_temp.append(nom1_original[k])
                    nom=nom2_original[i]
                    nom2_temp.append(nom)
                    score_temp.append(score_original[k][i])
                        
                ### Uncomment if you allow double matches (yes in that case the code should be simple)
    #            nom1,nom2,score=nom1_temp,nom2_temp,score_temp            
    #           break
                
                #The idea is to keep all the maximum for a df2 max. It won't always give the optimal solution,
                # but close enough ("algorithme glouton")

                nom2_temp_unique=[]
                for k in nom2_temp:
                    if k not in nom2_temp_unique:
                        nom2_temp_unique.append(k)

                #Her    e, we associate values and match for each of the maximums (in nom2_temp(_unique))
                value=dict([(k,0) for k in nom2_temp_unique])
                match=dict([(k,"") for k in nom2_temp_unique])

                for k in range(len(nom2_temp)):
                    matcher=nom2_temp[k]
                    matched=nom1_temp[k]
                    ratio=score_temp[k]
                    if ratio>value[matcher] :
                                    
                        value[matcher]=ratio
                        match[matcher]=matched
                    else :
                        pass
    #          
                #Here we count the columns and line that have not found an optimal match, and keep them inside score_original
    

                # Add the validated names to the definitive lists to output

                nom1=np.concatenate((nom1,[match[j] for j in nom2_temp_unique]))
                nom2=np.concatenate((nom2,[k for k in nom2_temp_unique]))
                score=np.concatenate((score,[value[k] for k in nom2_temp_unique]))

                buffer=[]
                for k in nom1_original :
                    if k not in nom1:
                        buffer.append(k)
                nom1_original=buffer
                buffer=[]
                for k in nom2_original:
                    if k not in nom2:
                        buffer.append(k)
                nom2_original=buffer

        df_top=pd.DataFrame({"nom1":nom1,"nom2":nom2,"score":score})
        return df_top
    except:
        print(df)
        return df

UPLOAD_FOLDER = './uploads'
>>>>>>> 46a78eb107670e2be530f000d240622a5b763970
ALLOWED_EXTENSIONS = set(["csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("uploading file",request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        file2=request.files['file2']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("uploading file for real")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "liste1.xlsx"))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], "liste2.xlsx"))
            df=(read_excel(os.path.join(app.config['UPLOAD_FOLDER'], "liste1.xlsx")))
            df2=(read_excel(os.path.join(app.config['UPLOAD_FOLDER'], "liste2.xlsx")))
<<<<<<< HEAD
            df=(read_excel("uploads/liste1.xlsx"))
            df2=(read_excel("uploads/liste2.xlsx"))
            
            #print("debug1",df.keys()==df2.keys(),len(df["Nom"]))
=======
            #print("check formating",df["Nom"], df2["Nom"])
>>>>>>> 46a78eb107670e2be530f000d240622a5b763970
            if len(df)<len(df2):
                print("case 1")
                df=get_all_matches(df,df2)
            else:
                print("case 2")
                df=get_all_matches(df2,df)
<<<<<<< HEAD
            print("debug",df)
=======
                print(df)
>>>>>>> 46a78eb107670e2be530f000d240622a5b763970
            df_top=get_top_matches(df)
            return render_template('view.html',tables=[df_top.to_html(classes="df"),df.to_html(classes="df")],
    titles = ['na',"Meilleure configuration", 'TOUS les resultats'])
    return render_template("uploaded.html")
    
