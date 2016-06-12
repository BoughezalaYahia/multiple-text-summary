import tkinter as Tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as ScrollTxt
from tkinter import END,E,W,filedialog,messagebox
from nltk.tokenize import sent_tokenize, RegexpTokenizer, word_tokenize
import math
import fileinput
from textblob import TextBlob as tb
from nltk.tag import pos_tag, map_tag
from nltk.corpus import stopwords
import re
 
class Test(object):
    i = 1 
    column = 1
    width = 10
    tem = 1

class popupWindow(object):
    def __init__(self,master):
        self.master = master
        self.l=Tk.Label(master,text="Input number of documents to be summarize [1-3]: ")
        self.l.pack()
        self.e=Tk.Entry(master)
        self.e.pack()
        self.b=Tk.Button(master,text='Submit',command=self.validation)
        self.b.pack()
       
    def validation(self):
        try:
            if 1<= int(self.e.get()) <= 3:
                Test.i = int(self.e.get())
                self.master.destroy()
            else:
                messagebox.showwarning("Error","Number of documents must be between 1-3 only")
        except:
           messagebox.showerror("Error","Input not valid")
 
class popupWindow2(object):
    def __init__(self,master):
        self.master = master
        self.l=Tk.Label(master,text="Choose Document Number [1-"+str(Test.i)+"] ")
        self.l.pack()
        self.e=Tk.Entry(master)
        self.e.pack()
        self.b=Tk.Button(master,text='Submit',command=self.validation)
        self.b.pack()
       
    def validation(self):
        try:
            if 1 <= int(self.e.get()) <= Test.i:
                Test.tem = int(self.e.get())
                self.master.destroy()
            else:
                messagebox.showwarning("Error","Number of documents must be between 1-"+str(Test.i)+" only")
        except:
           messagebox.showerror("Error","Input not valid")
 

#Menu bar frame
class MenuBarFrame(Tk.Frame):
 
    def __init__(self, master=None):
        Tk.Frame.__init__(self,master)
        self.grid(row=0,column=0,sticky=W+E)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1,weight=1)
        self.CreateWidgets()
         
    def CreateWidgets(self):
        menubar = Tk.Menu(self)
        filemenu = Tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open text",command=self.OpenFile)
        filemenu.add_command(label="Save text",command=self.SaveText)
        filemenu.add_command(label="Save summary",command=self.SaveSummary)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=MainWindow.destroy)
        menubar.add_cascade(label="File",menu=filemenu)
        self.master.config(menu=menubar)
        if Test.i == 2:
            Test.column = 2
            Test.width = 25
        elif Test.i == 3:
            Test.column = 3
            Test.width = 20 
        self.txtInptLbl = Tk.Label(self, text="Text for summarization:",anchor=W,width=10)
        self.txtInptLbl.grid(row=0,column=0,sticky=W+E)
        self.summaryLbl = Tk.Label(self, text="Summary: ",anchor=W,width=Test.width)
        self.summaryLbl.grid(row=0,column=Test.column,sticky=W+E)
 
    def OpenFile(self):
        textBoxFrame.inputTxtBox.delete('1.0',END)
        openFile=filedialog.askopenfilename(parent=self,filetypes=[('text document (*.txt)','*.txt')])
        for l in fileinput.input(openFile):
            textBoxFrame.inputTxtBox.insert(END,l)

    def SaveText(self):
        saveText=filedialog.asksaveasfilename(parent=self,filetypes=[('text document (*.txt)','*.txt')],defaultextension='.txt')
        text=textBoxFrame.inputTxtBox.get('1.0',END)
        file=open(saveText,"w")
        file.write(text)
        file.close
 
    def SaveSummary(self):
        saveText=filedialog.asksaveasfilename(parent=self,filetypes=[('text document (*.txt)','*.txt')],defaultextension='.txt')
        text=textBoxFrame.outputTxtBox.get('1.0',END)
        file=open(saveText,"w")
        file.write(text)
        file.close
 
#Textbox frame
class TextBoxFrame(Tk.Frame):    
 
    def __init__(self, master=None):
        Tk.Frame.__init__(self,master)
        self.grid(row=1,column=0,sticky='w,e,s,n')
        self.CreateWidgets()
        self.ContextMenu()
 
    def CreateWidgets(self):
        self.inputTxtBox = ScrollTxt.ScrolledText(self,height=10,width=10,wrap=Tk.WORD)
        self.inputTxtBox2 = ScrollTxt.ScrolledText(self,height=10,width=10,wrap=Tk.WORD)
        self.inputTxtBox3 = ScrollTxt.ScrolledText(self,height=10,width=10,wrap=Tk.WORD)
        if Test.i == 1:
             self.inputTxtBox.pack(side='left',fill=Tk.BOTH,expand=1)
        elif Test.i == 2:
            self.inputTxtBox.pack(side='left',fill=Tk.BOTH,expand=1)
            self.inputTxtBox2.pack(side='left',fill=Tk.BOTH,expand=1)
        elif Test.i == 3:
            self.inputTxtBox.pack(side='left',fill=Tk.BOTH,expand=1)
            self.inputTxtBox2.pack(side='left',fill=Tk.BOTH,expand=1)
            self.inputTxtBox3.pack(side='left',fill=Tk.BOTH,expand=1)
       
        self.outputTxtBox = ScrollTxt.ScrolledText(self,height=10,width=10,wrap=Tk.WORD)
        self.outputTxtBox.pack(side='left',fill=Tk.BOTH,expand=1)
 
    def ContextMenu(self):
        self.contextMenu=Tk.Menu(self,tearoff=0)
        self.contextMenu.add_command(label="Cut",accelerator="CTRL+X",command=self.Cut)
        self.contextMenu.add_command(label="Copy",accelerator="CTRL+C",command=self.Copy)
        self.contextMenu.add_command(label="Paste",accelerator="CTRL+V",command=self.Paste)
        self.bind_class("Text","<Button-3>", self.Callback)
 
    def Callback(self,event):
        self.contextMenu.post(event.x_root, event.y_root)
        self.currentTextWidget=event.widget
 
    def Cut(self):
        self.currentTextWidget.event_generate("<<Cut>>")
         
    def Copy(self):
        self.currentTextWidget.event_generate("<<Copy>>")
 
    def Paste(self):
        self.currentTextWidget.event_generate("<<Paste>>")
         
class BottomButtonsFrame(Tk.Frame):
 
    def __init__(self, master=None):
        Tk.Frame.__init__(self,master,)
        self.grid(row=2,column=0,sticky=W+E)
        self.CompressRate=50
        self.CreateWidgets() 
         
    def CreateWidgets(self):        
        self.Summarize = Tk.Button(self, text="Summarize",width=10,command=ComputeSummary)
        self.Summarize.grid(row=0)
        self.RatioLabel = Tk.Label(self, text="Compress percent:")
        self.RatioLabel.grid(row=0,column=1)
        self.CmbBxRt = ttk.Combobox(self,values=list(range(10,100,10)),state='readonly')
        self.CmbBxRt.set(self.CompressRate)
        self.CmbBxRt.bind("<<ComboboxSelected>>",self.CmbBxRtValue)
        self.CmbBxRt.grid(row=0,column=2) 
        self.Exit = Tk.Button(self, text="Exit",width=10,command=MainWindow.destroy)
        self.Exit.grid(row=1)
 
    def CmbBxRtValue(self,event):
        self.CompressRate=(self.CmbBxRt.get())                  
          
#tf-idf
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)
  
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)
  
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
  
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
 
def totalSent(sentence):
    temSent = list()
    temSent = sent_tokenize(sentence)
    return len(temSent)
 
def ComputeSummary():
   
    textBoxFrame.outputTxtBox.delete('1.0', END)
    inputFrame = textBoxFrame.inputTxtBox.get("1.0",END).encode('utf-8').decode('utf-8')
    if Test.i == 2:
        inputFrame2 = textBoxFrame.inputTxtBox2.get("1.0",END)
    elif Test.i == 3:
        inputFrame2 = textBoxFrame.inputTxtBox2.get("1.0",END)
        inputFrame3 = textBoxFrame.inputTxtBox3.get("1.0",END)
    compressRate = 1 - float(int(bottomButtonsFrame.CompressRate)/100)
    try:
        sentences = list()
        processWord = list()
        bloblist = list()
        sentences.append(inputFrame.lower())
        if Test.i == 2:
            sentences.append(inputFrame2.lower())
            compressRate = int(compressRate*(totalSent(sentences[0])+totalSent(sentences[1])))
        elif Test.i == 3:
            sentences.append(inputFrame2.lower())
            sentences.append(inputFrame3.lower())
            compressRate = int(compressRate*(totalSent(sentences[0])+totalSent(sentences[1])+totalSent(sentences[2])))
        else:
            compressRate = int(compressRate*(totalSent(sentences[0])))

        if(compressRate == 0):
            compressRate+=1
        elif(compressRate == totalSent(sentences[0])):
            compressRate-=1

        for i in range(len(sentences)):
            processWord.append(word_tokenize(sentences[i]))
        
        #Enclitics
        for i in range(len(processWord)):
            j = 0
            for word, tag in pos_tag(processWord[i]):
                if map_tag("en-ptb","universal",tag) == "VERB":
                    if word == "\'ll":
                        processWord[i][j] = "will"
                    elif word == "\'ve":
                        processWord[i][j] = "have"
                    elif word == "\'m":
                        processWord[i][j] = "am"
                    elif word == "\'re":
                        processWord[i][j] = "are"
                j+=1
        ##Take only verb and noun
        for i in range(len(processWord)):
            for word, tag in pos_tag(processWord[i]):
                if map_tag("en-ptb","universal",tag) != "NOUN" and map_tag("en-ptb","universal",tag) != "VERB":
                    processWord[i].remove(word)
                elif word == "\'s":
                        processWord[i].remove(word)
 
        #Remove stopwords
        for i in range(len(processWord)):
            for word in  processWord[i]:
                if word in stopwords.words("english"):
                    processWord[i].remove(word)
 
        #convert word list into sentence list
        for i in range(len(processWord)):
            processWord[i] = ' '.join(processWord[i])
  
        #Use blob list
        for i in range(len(processWord)):
            bloblist.append(tb(processWord[i]))
  
        #print top 5 words in each document
        for i, blob in enumerate(bloblist):
            print("")
            print("Top words in document {}".format(i + 1))
            scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key = lambda x: x[1], reverse=False)
            count_word = 1
            for word, score in sorted_words[:5]:
                print("Word",count_word,": ",word, " TF-IDF: ",abs(round(score,10)))
                count_word += 1
  
        ##============================================================================##
        ## variable to keep values and words
        total_value = list()
        #initialize total value dynamic
        for i in range(len(processWord)):
            total_value.append(0) 
        save_words = list()
  
        ## Function to calculate sentence value
        def sent_value(word_value, doc_value):
            #return (1-word_value)/(1-doc_value)
            try:
                return word_value/doc_value
            except:
                return word_value/(doc_value + 1)
        def dict_pair(sent, value):
            list_set = [sent, value]
            return list_set
  
        #variable sentence
        sentences_list = list()
        sentence_word_value = 0
        #======TEST TRY BASED ON TEXT=======
        overall_text = ""
        for i in range(len(sentences)):
            overall_text+=sentences[i] 
        sentences_list = sent_tokenize(overall_text) 
        list_toBeSorted = list()
  
        ## Calculate total value in document
        for i, blob in enumerate(bloblist):
            scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key = lambda x: x[1], reverse=False)
            save_words.append(blob.words)
            ## calculate total value of document
            for word, score in sorted_words:
                total_value[i] += score
  
            ## calculate value of each sentence
            for sent in sentences_list:
                sentence_word_value = 0
                for word in word_tokenize(sent):
                    if word in blob.words:
                        sentence_word_value += tfidf(word,blob,bloblist)
                list_toBeSorted.append(dict_pair(sent, sent_value(sentence_word_value, total_value[i])))
                sorted_sent = sorted(list_toBeSorted, key = lambda x:x[1], reverse=False)
  
        ## Print Total tf/idf value for each documents
        counter = 0
        for i in enumerate(bloblist):
            print("Total value of document " ,str(counter+1) ," = ", str(abs(total_value[counter])))
            counter += 1
  
        count = 1
        sentList = list()
        for sent,value in sorted_sent:
            if count == compressRate+1:
                break
            else:
                if sent not in sentList:
                    sentList.append(sent)
                    print("\nSentence ",count,": \n",sent,"\nValue: ",abs(value), sep='')
                    count += 1
        
        sentCounter = 0
        wordCounter = 0
        print("\nSummary:")
        for sent_List in sentences_list:
            for sent in sentList:
                if sent_List in sent:
                    print(sent_List[0][0].upper()+sent_List[1:],end = ' ')
                    textBoxFrame.outputTxtBox.insert(END,sent_List[0][0].upper()+sent_List[1:]+' ')
                    sentCounter+=1
                    wordCounter += len(re.findall(r'\w+',sent_List))
        
        
        print("\nStatistic:")
        for i in range(len(sentences)):
            sentCounter2 = 0
            wordCounter2 = 0
            for j in range(len(sent_tokenize(sentences[i]))):
                if len(sentences[i]) != 1:
                    sentCounter2+=1
            wordCounter2 = len(re.findall(r'\w+',sentences[i]))
            print("Number of sentences in document ",i+1,": ",sentCounter2)
            print("Number of words in document ",i+1,"    : ",wordCounter2)
            print()
        print("Number of sentences in summary     : ",sentCounter)
        print("Number of words in summary         : ",wordCounter)

    except ZeroDivisionError:
         messagebox.showinfo("Error", "Please input sentences inside the frame!")
    except UnicodeEncodeError:
         messagebox.showinfo("Error", "Please make sure only english words and no clitics inside the frame!")
 
root = Tk.Tk()
m=popupWindow(root)
root.mainloop()
MainWindow = Tk.Tk()
MainWindow.title("TF-IDF Text Summarization")
if Test.i == 1:
    MainWindow.minsize(800,500)
elif Test.i == 2:
    MainWindow.minsize(1000,600)
elif Test.i == 3:
    MainWindow.minsize(1200,650)
MainWindow.columnconfigure(0,weight=1)
MainWindow.rowconfigure(0, weight=0)
MainWindow.rowconfigure(1, weight=1)
MainWindow.rowconfigure(2, weight=0)
menuBarFrame = MenuBarFrame(master=MainWindow)
textBoxFrame=TextBoxFrame(master=MainWindow)
bottomButtonsFrame=BottomButtonsFrame(master=MainWindow)
MainWindow.mainloop()
