#Imports-------------------------------------------
import os
import sys
from fpdf import FPDF
import yaml
import re
import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter
import networkx as nx
import matplotlib.pyplot as plt
from datetime import date

#Variables-----------------------------------------
found = False
cntTitle = 1
cntsubTitle = 1
cntsubsubTitle = 1
global cnt
global index
global indexposition
global indexfile
indexposition=0
last=False
graph = nx.Graph()

indexfile =["" for i in range(50)]

#Code----------------------------------------------
#Aks the current directory where this python file is using os library
#to look for the file name asked by input.
arr=os.listdir()
fileName=input("Enter a name file to process: ")
sourceCont=open("StaticContent.txt","r")
filevariable=open(fileName,"r")
documents = yaml.load(filevariable,Loader=yaml.FullLoader)
#relative_path = os.open("/home/devasc/Desktop/CSO/P/lab1-python-cc-p1", os.O_RDONLY)

#Check if the file name asked in the input already exist in the directory
#if not, the programs ends.
i=0
while i < len(arr):
  if arr[i]==fileName:
    print("File found: " + arr[i])
    found = True
  i+=1
else:
  if found == False:
    print("file not found")
    sys.exit()

title = 'Informació infraestructura de Xarxa TecnoCampus('+fileName+')'


def doindex(ind):
  global indexposition
  global indexfile
  indexfile[indexposition] = ind
  indexposition +=1


class PDF(FPDF):

  def header(self):
    if self.page_no() != 1:
      #Logo
      self.image('logo_tc.jpg',160,8,33)
            # Arial bold 15
      self.set_text_color(0,0,0)
      self.set_font('Arial', 'B', 12)
      # Move to the right
      #self.cell(80)
      w = self.get_string_width(title) + 6
      self.set_x((w / 2) - 10)
      # Title
      self.cell(30, 10, title, 0, 0, 'C')
      # Line break
      self.ln(20)

  
  # Page footer
  def footer(self):
    if self.page_no() != 1:
      if last:
        # Position at 1.5 cm from bottom
        self.set_y(-10)
        self.set_x(3)
        # Arial italic 8
        self.set_text_color(0,0,0)
        self.set_font('Arial', 'I', 11)
        # Page number
        self.cell(0, 10,str(2), 0, 0, 'L')
      else:
        # Position at 1.5 cm from bottom
        self.set_y(-10)
        self.set_x(3)
        # Arial italic 8
        self.set_text_color(0,0,0)
        self.set_font('Arial', 'I', 11)
        # Page number
        self.cell(0, 10,str(self.page_no()+1), 0, 0, 'L')

    # Page footer









dt=date.today()
#Generate the class PDF to work with the librari fpdf an write all to generate the pdf
pdf = PDF()
pdf.set_auto_page_break(True)
pdf.add_page()
pdf.set_font('Arial', '', 35)
pdf.set_text_color(0,0,0)
#Set place where want to start to create the front page of the pdf
#and write the title and information we want
pdf.rect(40,30,5,200,'F')
pdf.set_xy(50,70)
pdf.write(20,"Informació infraestructura\n")
pdf.set_xy(50,90)
pdf.write(20,"de Xarxa TecnoCampus\n")
pdf.set_xy(50,110)
pdf.write(20,"("+fileName+")\n")
pdf.set_xy(50,150)
time=dt.strftime('%B, %Y')
pdf.write(20,time+"\n")

pdf.set_xy(39,235)
pdf.set_font('Arial', '', 8)
pdf.write(5,"La informació continguda en aquest document pot ser de caràcter privilegiat y/o confidencial. Qualsevol disseminació,\n")
pdf.set_xy(39,238)
pdf.write(5,"distribució o copia d'aquest document per qualsevol altre persona diferent als receptors originals queda estrictament\n")
pdf.set_xy(39,241)
pdf.write(5,"prohibida. Si ha rebut aquest document per error, sis plau notifiquí immediatament al emissor i esborri qualsevol copia\n")
pdf.set_xy(39,244)
pdf.write(5,"d'aquest document.\n")

pdf.add_page()


#Class where the methods to fill the pdf gonna be 
class swithcerPDFStaticVariable:

  #Method to find other methods without extra parameter,
  #only the parameter title that have the name of the method in the class to find
  def switchStatic(self,title):
    defautl="lo que sea"
    return getattr(self,title,lambda:defautl)()

  #Method to find other methods with extra parameter for the place of the node in the yaml file,
  #the parameter title to find methods with that name and the parameter varpl for the place of the node
  def switchVariable(self,title,varpl):
    defautl="lo que sea"
    return getattr(self,title,lambda:defautl)(varpl)

  #Write in the pdf a line with a Title format
  def title(self):
    global cntTitle
    global cntsubTitle
    global cntsubsubTitle
    global index
    pdf.set_font('Arial', '', 18)
    pdf.set_text_color(0,0,255)
    pdf.write(15, str(cntTitle) + ".-")
    pdf.write(15,fstr)
    ad = fstr.split('\n')
    index = str(cntTitle) + ".-" +  ad[0]+","+str(pdf.page_no())
    doindex(index)
    cntTitle = cntTitle + 1
    cntsubTitle = 1
    cntsubsubTitle = 1
    
  #Write in the pdf a line with a Subtitle format
  def sub(self):
    global cntTitle
    global cntsubTitle
    global cntsubsubTitle
    global index
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(15,159,230)
    pdf.write(9, str(cntTitle-1) + "." + str(cntsubTitle) +".-")
    pdf.write(9,fstr)
    ad = fstr.split('\n')
    index = "  "+str(cntTitle-1) + "." + str(cntsubTitle) +".-" + ad[0]+","+str(pdf.page_no())
    doindex(index)
    cntsubTitle += 1
    cntsubsubTitle = 1

  #Write in the pdf a line with a Subtitle of the Subtitle  format
  def under(self):
    global cntsubsubTitle
    global index
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(15,159,230)
    pdf.write(9, str(cntTitle-1) + "." + str(cntsubTitle-1) + "."+ str(cntsubsubTitle) + ".-")
    pdf.write(9,fstr)
    ad = fstr.split('\n')
    index= "    "+str(cntTitle-1) + "." + str(cntsubTitle-1) + "."+ str(cntsubsubTitle) +".-" + ad[0]+","+str(pdf.page_no())
    doindex(index)
    cntsubsubTitle += 1

  #Write a line with format of a basic text
  def writeBasicText(self):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    if re.search('[a-zA-Z]',fstr):
      pdf.write(5,fstr)
  
  #Method used to add a concrete line that have the name of the file in it
  def namefile(self):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    pdf.write(5,"El present document descriu la topologia realitzada amb la configuració "+fileName+" a la\n")

  #Write a line with a Subtitle format but the content of the file it's variable 
  #depending on wich line the pdf is writing
  def tlvar(self,nodeplace):
    global cntTitle
    global cntsubTitle
    global cntsubsubTitle
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(15,159,230)
    pdf.write(9, str(cntTitle-1) + "." + str(cntsubTitle) +".-")
    pdf.write(9,documents["nodes"][nodeplace]["label"]+"\n")
    index = "  "+str(cntTitle-1) + "." + str(cntsubTitle) +".-" + documents["nodes"][nodeplace]["label"]+","+str(pdf.page_no())
    doindex(index)
    cntsubTitle += 1
    cntsubsubTitle = 1
  
  #This method is used to know how many nodes and links are and write a line in the pdf with the information
  def lennodes(self):
    nodesnum=0
    linksnum=0

    for k,v in documents.items():
      if k == "nodes":
        nodesnum=len(v)
      if k == "links":
        linksnum=len(v)

    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    pdf.write(5,"En aquesta topologia tenim "+str(nodesnum)+" equips, connectats a través de "+str(linksnum)+" links\n")

  #This method loks for all the conexions made by the links and write the information in the pdf
  def interadd(self):
    found = False
    i = 0
    strvar = ""
    for k in documents["links"]:
      pdf.set_font('Arial', 'B', 11)
      pdf.set_text_color(0,0,0)
      pdf.write(5,"   -Link "+ k["id"]+": ")
      pdf.set_font('Arial', '', 11)
      pdf.set_text_color(0,0,0)
      pdf.write(5, "connecta ")
      found = False
      i=0
      while found is False:
        if documents["nodes"][i]["id"] == k["n1"]:
          pdf.write(5,k["i1"] +"("+documents["nodes"][i]["label"]+ ") amb ")
          found = True
        i+=1
      
      i=0
      found = False
      while found is False:
        if documents["nodes"][i]["id"] == k["n2"]:
          pdf.write(5,k["i1"] +"("+documents["nodes"][i]["label"]+ ")\n")
          found = True
        i+=1


  #Bannerex looks in the configuration of the node especified(the nodeplace) for information about
  #banners, if the method doesn't found any banner writes a line saying that there is no banner
  #configuration
  def bannerex(self,nodesplace):
    start = False
    found =False
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    for k in documents["nodes"][nodesplace]["configuration"].splitlines():
      if start:
        if "^C" in k:
          start = False
          x = k.split("^C")
          pdf.write(5,x[0]+"\n")
        else:
          pdf.write(5, k+"\n")

      if k.startswith("banner"):
        if found == False:
          found=True
          pdf.write(5, "El dispositiu té configurats els següent Banners:\n")
        start = True
        x = k.split()
        pdf.write(5,"-"+x[1]+"\n")
    
    if found == False:
      pdf.write(5, "El dispositiu no té configurats els Banners\n")

  #Little method to find the ip route in the configuration of the node
  def routef(self,nod):
    for n in documents["nodes"][nodeplace]["configuration"].splitlines():
      if n.startswith("ip"): 
        if "route" in n:
          x=n.split()
          return(x[4])

  #Little method to know if a char or a string(w) is in a line(s)
  #only check if this char or string it's alone
  def contwor(self, s, w):
    return(' ' + w + ' ') in (' ' + s + ' ')

  #Find the name of the links and the configuration ips for it 
  def alpput(self,nodeplace):
    start = False
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    for k in documents["nodes"][nodeplace]["interfaces"]:
      pdf.write(5,"   -  Link "+k["id"]+": "+k["label"]+". ")
      for n in documents["nodes"][nodeplace]["configuration"].splitlines():
        if start:
          if n.startswith("ip"):
            if s.contwor(n, "address"):
              x=n.split()
              pdf.write(5,"Configuració IP: " +x[2] + "(DG: ")
              pdf.write(5,routef(nodeplace)+ ")")
              start = False
        else:
          if n.startswith("interface"):
            if s.contwor(n,k["label"]):
              start = True
          elif n.startswith("ip"):
            if not start:
              if s.contwor(n, "addr"):
                x=n.split()
                pdf.write(5,"Configuració IP: " +x[3] + "(DG: ")
              elif s.contwor(n, "route add default"):
                x=n.split()
                pdf.write(5,x[5]+")")
        
      start = False
      pdf.write(5,"\n")

  #Find and write wich was the last day and hour that the configuration of the node whas changed
  def iosadconfiguration(self,nodeplace):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    for k in documents["nodes"][nodeplace]["configuration"].splitlines():
      if s.contwor(k, "Last configuration"):
        x=k.split()
        pdf.write(5,"El darrer canvi de la configuracio va ser el "+x[8]+" "+x[9]+" "+x[10]+" a les "+ x[5]+x[6]+"\n")

  #Find and write the crypto configuration of the node asked in the parameter
  def cryptoconf(self,nodeplace):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    find = False
    mode=""
    for k in documents["nodes"][nodeplace]["configuration"].splitlines():
      if s.contwor(k, "set peer"):
        pdf.write(5,"El dispositiu té la següent configuració de crypto:\n")
        x=k.split()
        pdf.write(5," - Connexió amb "+ x[2]+"\n")
        find = True
        
    

    if find != True:
      pdf.write(5,"El dispositiu no té configuració de crypto\n")
    else:
      for k in documents["nodes"][nodeplace]["configuration"].splitlines():
        if s.contwor(k, "policy"):
          x=k.split()
          pdf.write(5,"   . Política de regles número "+ x[3]+"\n")
        elif s.contwor(k, "encr"):
          x=k.split()
          pdf.write(5,"     . Encriptació "+ x[1]+", "+x[2]+"\n")
        elif s.contwor(k, "authentication"):
          x=k.split()
          pdf.write(5,"     . Autenticació "+ x[1]+"\n")
        elif s.contwor(k, "group"):
          x=k.split()
          pdf.write(5,"     . Diffie-Helmann grup "+ x[1]+"\n")
        elif s.contwor(k, "key"):
          x=k.split()
          pdf.write(5,"   . Contrasenya ISAKMP: "+ x[3]+"\n")
        elif s.contwor(k, "crypto ipsec transform-set"):
          pdf.write(5,"   . Configuració VPN:\n")
          x=k.split()
          pdf.write(5,"     . Conjunt de transformació: "+ x[3]+"\n")
          pdf.write(5,"     . Configuració Encriptació ESP: "+ x[4]+"\n")
          pdf.write(5,"     . Configuració Signatura ESP: "+ x[5]+"\n")
        elif s.contwor(k, "mode"):
          x=k.split()
          pdf.write(5,"     . Mode "+ x[1]+"\n")
        elif s.contwor(k, "match address"):
          x=k.split()
          pdf.write(5,"     . ACL número "+ x[2]+"\n")


  #Look for the interfaces that have the node especified by parameter, when found, check if the node
  #have a configuration for the interfaces, if have, write the configuration for it, if not, only
  #write the interfaces the node have
  def isosinterface(self,nodeplace):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    inter=""
    i=0
    found = False
    fooundsome = False
    if documents["nodes"][nodeplace]["configuration"] == "":
      for k in documents["nodes"][nodeplace]["interfaces"]:
        if found == False:
          fooundsome=True
          pdf.write(5,"Les interfícies i la seva configuració és:\n")
          found = True
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0,0,0)
        pdf.write(5,"\t"+ "   -Link"+documents["nodes"][nodeplace]["interfaces"][i]["id"]+":"+documents["nodes"][nodeplace]["interfaces"][i]["label"]+"\n")
        i+=1
    else:
      for k in documents["nodes"][nodeplace]["interfaces"]:
        inter+=k["id"]+" "+k["label"]
        if len(inter.split(",")) < len(documents["nodes"][nodeplace]["interfaces"]):
          inter+=","

      x=inter.split(",")
      while i < len(x):
        l=x[i].split()
        if s.contwor( l[1],"Loopback0"):
          pdf.write(5,"Les interfícies i la seva configuració és:\n")
          pdf.write(5," - Link "+ l[0]+": "+l[1]+": \n")
        for k in documents["nodes"][nodeplace]["configuration"].splitlines():
          if s.contwor(k, l[1]):
            if s.contwor(k, "eth0"):
              f=k.split()
              pdf.write(5," - Link "+ l[0]+": "+l[1]+": "+f[3]+"\n")
            else:
              pdf.write(5," - Link "+ l[0]+": "+l[1]+": ")

            fooundsome=True
            found = True
          
          if found:
            if s.contwor(k,"ip address"):
              if  s.contwor(k,"no") == False:
                j=k.split()
                pdf.write(5,j[2]+" (" + j[3]+")\n")
                found = False
              else:
                pdf.write(5,"\n")
                found = False
        i+=1
    if fooundsome == False:
      pdf.write(5,"No hi ha configuració de interfícies\n") 
    pdf.write("\n")
  
  #Enroutprotocol looks in the configuration of the node specified if have a routing protocol configurated
  #and write it in the pdf, if not only says that there is no routing protocol
  def enroutprotocol(self,nodeplace):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    trobat = False
    access=-1
    for k in documents["nodes"][nodeplace]["configuration"].splitlines():
      if s.contwor(k, "router"):
        trobat = True
        x=k.split()
        pdf.write(5,"El protocol d'enrutament utilitzat és "+x[1] + " " + x[2] +", amb la següent configuració (xarxes publicades):\n")
      
      if trobat:
        if s.contwor(k, "network"):
          x=k.split()
          if int(x[4])>access:
            pdf.write(5,"   - Àrea "+x[4]+":\n")
            pdf.write(5,"       - Xarxa "+x[1]+" màscara invertida "+x[2]+"\n")
            access = int(x[4])
          else:
            pdf.write(5,"       - Xarxa "+x[1]+" màscara invertida "+x[2]+"\n")
    
    if trobat == False:
      pdf.write(5,"No hi ha protocol d'enrutament\n")
  
  #This method check if the node specified have any control acces configuration and write it in the pdf
  def llistescontrol(self,nodeplace):
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0,0,0)
    trobat = False
    extended = False
    access=-1
    permit=""
    for k in documents["nodes"][nodeplace]["configuration"].splitlines():
      if s.contwor(k, "access-list"):
        trobat = True
        if s.contwor(k, "extended"):
          extended = True

        if extended == False:
          x=k.split()
          if access!=int(x[1]):
            pdf.write(5," - Número "+x[1]+"\n")
            access=int(x[1])
            if permit != x[3]:
              pdf.write(5,"   - PERMIT ("+x[3]+")\n")
              permit = x[3]
              pdf.write(5,"     - ORIGEN:"+x[4]+" màscara invertida "+x[5]+"\n")
              pdf.write(5,"     - DESTÍ:"+x[6]+" màscara invertida "+x[7]+"\n")
            else:
              pdf.write(5,"     - ORIGEN:"+x[4]+" màscara invertida "+x[5]+"\n")
              pdf.write(5,"     - DESTÍ:"+x[6]+" màscara invertida "+x[7]+"\n")
          else:
            if permit != x[3]:
              pdf.write(5,"   - PERMIT ("+x[3]+")\n")
              permit = x[3]
              pdf.write(5,"     - ORIGEN:"+x[4]+" màscara invertida "+x[5]+"\n")
              pdf.write(5,"     - DESTÍ:"+x[6]+" màscara invertida "+x[7]+"\n")
            else:
              pdf.write(5,"     - ORIGEN:"+x[4]+" màscara invertida "+x[5]+"\n")
              pdf.write(5,"     - DESTÍ:"+x[6]+" màscara invertida "+x[7]+"\n")


    if extended:
      for k in documents["nodes"][nodeplace]["configuration"].splitlines():
        if s.contwor(k, "extended"):
          x=k.split()
          permit=x[3]

        x=k.split()
        if s.contwor(k, "permit"):
          pdf.write(5,"   - PERMIT ("+x[1]+")\n")
          if s.contwor(k, "any"):
             pdf.write(5,"     - ORIGEN:"+x[2]+" màscara invertida "+x[3]+"\n")
          else:
            pdf.write(5,"     - ORIGEN:"+x[2]+" màscara invertida "+x[3]+"\n")
            pdf.write(5,"     - DESTÍ:"+x[4]+" màscara invertida "+x[5]+"\n")
        elif  s.contwor(k, "deny"):
          pdf.write(5,"   - DENY ("+x[1]+")\n")
          if s.contwor(k, "any"):
             pdf.write(5,"     - ORIGEN:"+x[2]+" màscara invertida "+x[3]+"\n")
          else:
            pdf.write(5,"     - ORIGEN:"+x[2]+" màscara invertida "+x[3]+"\n")
            pdf.write(5,"     - DESTÍ:"+x[4]+" màscara invertida "+x[5]+"\n")


    if trobat == False:
      pdf.write(5,"El dispositiu no té configurada cap ACL.\n")

  #This method look for the nodes and the links and generates topology in image format to added in the pdf 
  def topologyFill(self):

    counter = 1
    mapping = {}
    for k in documents["nodes"]:
      graph.add_node(counter)
      mapping[counter] = k["node_definition"] + "\n" + k["label"]
      counter += 1
    
    for v in documents["links"]:
      first = int(list(v["n1"])[1])
      second = int(list(v["n2"])[1])
      graph.add_edge(first, second)

    graphFinal = nx.relabel_nodes(graph, mapping)
    nx.draw(graphFinal, with_labels=True, node_size = 1300)
    plt.savefig("path.png")
    pdf.image("path.png", 50, pdf.get_y()+10,120)
    pdf.ln(120)


  #Short method to know the n2 variable of the links that have the n1 specified by parameter
  def findswithcplace(self,find):
    for k in documents["links"]:
      if k["n1"] == find:
        result=k["n2"]+","+k["i2"]
        return result
    return "null"



  #Method to collect the information about the nodes linked and create a table from that data.
  def table(self):
    pdf.add_page()
    pdf.set_font('Times', '', 10.0)
    epw = pdf.w - pdf.l_margin - 35
    col_width = epw/5 - 5 
    found = False
    data1=[]

    for k in documents["links"]:
      found = False
      i=0
      inter1 =""
      
      inter2 =""
      eq1=""
      eq2=""
      interxarxa=""
      for n in documents["nodes"]:
        if n["id"] == k["n1"]:
          for j in n["interfaces"]:
            if j["id"] == k["i1"]:
              if j["label"] == "eth0":
                for l in n["configuration"].splitlines():
                  if swithcerPDFStaticVariable().contwor(l, j["label"]):
                    f=l.split()
                    eq1=n["label"]
                    inter1 = f[3]
                    ix=inter1.split(".")
                    interxarxa=ix[0]+"."+ix[1]+"."+ix[2]+".0"

              else:
                for c in n["configuration"].splitlines():
                  if swithcerPDFStaticVariable().contwor(c, "interface "+j["label"]):
                    found=True
                  
                  if found:
                    if swithcerPDFStaticVariable().contwor(c,"ip address"):
                      if swithcerPDFStaticVariable().contwor(c,"no")==False:
                        x=c.split()
                        found = False
                        eq1=n["label"]
                        inter1 = x[2]
                        ix=inter1.split(".")
                        interxarxa=ix[0]+"."+ix[1]+"."+ix[2]+".0"


        if n["id"] == k["n2"]:
          if n["node_definition"] == "unmanaged_switch":  
            xfi=swithcerPDFStaticVariable().findswithcplace(k["n2"])
            if xfi != "null":
              xf=xfi.split(",")
      
              for d in documents["nodes"]:
                if d["id"] == xf[0]:
                  for j in d["interfaces"]:
                    if j["id"] == xf[1]:
                      if j["label"] == "eth0":
                        for l in d["configuration"].splitlines():
                          if swithcerPDFStaticVariable().contwor(l, j["label"]):
                            f=l.split()
                            eq2=d["label"]
                            inter2 = f[3]
                      else:
                        for c in d["configuration"].splitlines():
                          if swithcerPDFStaticVariable().contwor(c, "interface "+j["label"]):
                            found=True
                          
                          if found:
                            if swithcerPDFStaticVariable().contwor(c,"ip address"):
                              if swithcerPDFStaticVariable().contwor(c,"no")==False:
                                x=c.split()
                                found = False
                                eq2=d["label"]
                                inter2 = x[2]            
          else:
            for j in n["interfaces"]:
              if j["id"] == k["i2"]:
                if j["label"] == "eth0":
                  for l in n["configuration"].splitlines():
                    if swithcerPDFStaticVariable().contwor(l, j["label"]):
                      f=l.split()
                      eq2=n["label"]
                      inter2 = f[3]
                else:
                  for c in n["configuration"].splitlines():
                    if swithcerPDFStaticVariable().contwor(c, "interface "+j["label"]):
                      found=True
                    
                    if found:
                      if swithcerPDFStaticVariable().contwor(c,"ip address"):
                        if swithcerPDFStaticVariable().contwor(c,"no")==False:
                          x=c.split()
                          found = False
                          eq2=n["label"]
                          inter2 = x[2]
        i+=1
      if (interxarxa =="" or eq1=="" or eq2=="" or inter2=="") == False:
        data1.append({'Xarxa': interxarxa, 'Equip1': eq1, 'Interfície1':k["i1"],'IP1':inter1,'Equip2':eq2,'Interfície2':k["i2"],'IP2':inter2})

    df = pd.DataFrame(data1)
    s = df['Xarxa']
    v = df['Equip1']
    c = df['Interfície1']
    d = df['IP1']
    e = df['Equip2']
    f = df['Interfície2']
    g = df['IP2']
    lnedata=len(data1)
    data=[]
    data.append(df)
    for i in range (lnedata):
      data.append([s[i], v[i], c[i], d[i],e[i],f[i],g[i]])
    th = pdf.font_size
    count = 0
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    for row in data:
        count += 1
        for datum in row:
            if count == 1:
                pdf.set_fill_color(70, 130, 180)
                pdf.set_font('Times', '', 10)
                pdf.cell(col_width, 2*th, str(datum), border=1, align='L', fill=1)

            else:
                pdf.set_font('Times', '', 10)
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.multi_cell(col_width, 2*th, str(datum), border=1, align='L', fill=0)
                pdf.set_xy(x+28,y)
        pdf.ln(2 * th)
    pdf.ln(2* th)
    

s = swithcerPDFStaticVariable()

def pdfwrite(cnt):
  if cnt == 1:
    s.switchStatic("title")
  elif cnt == 2:
    s.switchStatic("sub")
  elif cnt == 3:
    s.switchStatic("namefile")
  elif cnt == 6:
    s.switchStatic("sub")
  elif cnt == 19:
    s.switchStatic("sub")
  elif cnt == 21:
    s.switchStatic("topologyFill")
  elif cnt == 22:
    s.switchStatic("lennodes")
  elif cnt == 24:
    s.switchStatic("title")
  elif cnt == 27:
    s.switchVariable("tlvar",0)
  elif cnt == 28:
    s.switchStatic("under")
  elif cnt == 29:
    s.switchVariable("isosinterface",0)
  elif cnt == 39:
    s.switchVariable("tlvar",1)
  elif cnt == 40:
    s.switchVariable("iosadconfiguration",1)
  elif cnt == 41:
    s.switchStatic("under")
  elif cnt == 42:
    s.switchVariable("cryptoconf",1)
  elif cnt == 56:
    s.switchStatic("under")
  elif cnt == 57:
    s.switchVariable("isosinterface",1)
  elif cnt == 64:
    s.switchStatic("under")
  elif cnt == 65:
    s.switchVariable("enroutprotocol",1)
  elif cnt == 70:
    s.switchStatic("under")
  elif cnt == 71:
    s.switchVariable("llistescontrol",1)
  elif cnt == 77:
    s.switchStatic("under")
  elif cnt == 79:
    s.switchVariable("bannerex",1)
  elif cnt == 83:
    s.switchVariable("tlvar",2)
  elif cnt == 84:
    s.switchVariable("iosadconfiguration",2)
  elif cnt == 86:
    s.switchStatic("under")
  elif cnt == 87:
    s.switchVariable("cryptoconf",2)
  elif cnt == 89:
    s.switchStatic("under")
  elif cnt == 90:
    s.switchVariable("isosinterface",2)
  elif cnt == 97:
    s.switchStatic("under")
  elif cnt == 98:
    s.switchVariable("enroutprotocol",2)
  elif cnt == 104:
    s.switchStatic("under")
  elif cnt == 105:
    s.switchVariable("llistescontrol",2)
  elif cnt == 107:
    s.switchStatic("under")
  elif cnt == 109:
    s.switchVariable("bannerex",2)
  elif cnt == 115:
    s.switchVariable("tlvar",3)
  elif cnt == 116:
    s.switchVariable("iosadconfiguration",3)
  elif cnt == 118:
    s.switchStatic("under")
  elif cnt == 119:
    s.switchVariable("cryptoconf",3)
  elif cnt == 133:
    s.switchStatic("under")
  elif cnt == 134:
    s.switchVariable("isosinterface",3)
  elif cnt == 141:
    s.switchStatic("under")
  elif cnt == 142:
    s.switchVariable("enroutprotocol",3)
  elif cnt == 147:
    s.switchStatic("under")
  elif cnt == 148:
    s.switchVariable("llistescontrol",3)
  elif cnt == 154:
    s.switchStatic("under")
  elif cnt == 156:
    s.switchVariable("bannerex",3)
  elif cnt == 162:
    s.switchVariable("tlvar",4)
  elif cnt == 163:
    s.switchStatic("under")
  elif cnt == 164:
    s.switchVariable("isosinterface",4)
  elif cnt == 174:
    s.switchVariable("tlvar",5)
  elif cnt == 175:
    s.switchStatic("under")
  elif cnt == 176:
    s.switchVariable("isosinterface",5)
  elif cnt == 186:
    s.switchVariable("tlvar",6)
  elif cnt == 187:
    s.switchStatic("under")
  elif cnt == 189:
    s.switchVariable("alpput",6)
  elif cnt == 190:
    s.switchVariable("tlvar",7)
  elif cnt == 191:
    s.switchStatic("under")
  elif cnt == 193:
    s.switchVariable("alpput",7)
  elif cnt == 194:
    s.switchVariable("tlvar",8)
  elif cnt == 195:
    s.switchStatic("under")
  elif cnt == 197:
    s.switchVariable("alpput",8)
  elif cnt == 198:
    s.switchStatic("title")
  elif cnt == 200:
    s.switchStatic("interadd")
  elif cnt == 209:
    s.switchStatic("table")
  else:
    s.switchStatic("writeBasicText")
    

fstr=sourceCont.readline()
cnt=1
while fstr:
  pdfwrite(cnt)
  fstr=sourceCont.readline()
  cnt+=1



pdf.set_font('Arial', '', 14)
pdf.set_text_color(0,0,0)
pdf.add_page()
last=True
xp = 10
yp= 30


epw = pdf.w - pdf.r_margin -20
for k in indexfile:
  if k != '':
    x = k.split(",")
    pdf.write(5,x[0])
    xp=pdf.get_x()
    yp=pdf.get_y()
    pdf.set_xy(xp,yp)
    w=xp-pdf.w - pdf.r_margin
    pdf.dashed_line(xp + 3,yp + 4,epw,yp + 4,0.1,1)
    pdf.set_xy(epw,yp)
    pdf.write(5,str(int(x[1])+1) +"\n")

print("end")

fil=documents["lab"]["title"]
filpdf=fil+".pdf"


pdf.output(filpdf, 'F')

def split(path, name_of_split):
    pdf = PdfFileReader(path)
    pdf_writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
      if page == 1:
        pdf_writer.addPage(pdf.getPage(pdf.getNumPages()-1))
      if page != pdf.getNumPages()-1:
        pdf_writer.addPage(pdf.getPage(page))

    output = f'{name_of_split}.pdf'
    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)



split(filpdf,fil)






sourceCont.close()