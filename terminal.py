import os,shutil,stat,grp,pwd,time
#importing modules
l=raw_input()  #taking input as a string

l=l.split()  #splitting the string using default delimitter as space 
 

def check_hidden(i):            #checking for if the file or directory is hidden or visible 
     if list(i)[0] =="." and len(list(i))>1 and i!="." and (list(i))[1]!="/":
	return 1
     else:
	return 0

if len(l)==1 and l[0]=="ls":  #simple case when input is ls only
    w=""
    lslist=os.listdir(".")   #lslist has contents of current directory
    lslist.sort()              # sorting the list so to  get the output in sorted format as ls does
    for i in lslist:
       u=check_hidden(i)          
       if (u==0):
            w+=i+" "        #appending the contents as a string

    print w          #printing the string in ls format

elif len(l)==2 and l[0]=="ls" and (l[1]==".." or l[1]=="../"):  #case when ls .. or ls ../
     w=""
     lslist=os.listdir("..") #lslist has contents of previous directory
     lslist.sort()            # sorting the list so to  get the output in sorted format as ls does
     for i in lslist: 
         u=check_hidden(i)
	 if u==0:
              w+=i+" "        # apending the contents as a string 

     print w    #printing the string in ls format


elif len(l)>=2 and l[0]=="ls" and l[1]!="-l" and l[1]!="-a" and (l[1]!=".." or l[1]!="../" ):
  for j in range(1,len(l)):
     try :          # if no error do the code followed 
          w=""
          lslist=os.listdir(l[j])
	  lslist.sort()       # sorting the list so to  get the output in sorted format as ls does
          for i in lslist:
	      u=check_hidden(i)
	      if u==0:
                  w+=i+" "
	  print l[j]+":"
          print w
     except OSError: # else handle the error and  do this 
          print "ls: cannot access " +l[j]+ " : No such file or directory "



if len(l)==1 and (l[0]=="cp" or l[0]=="mv" or l[0]=="rm") :  # case when input is only cp or mv  or rm
      print l[0]+" : missing file operand"
      print "Try \'"+l[0]+" --help\' for more information. "


      
elif (len(l)==2 ) and (l[0]=="cp" or l[0]=="mv"):   #case when input is cp or mv  and source file 
      print  l[0]+" : missing destination file operand after \'"+l[1]+"\'"
      print "Try \'"+l[0]+"  --help\' for more information."



import errno   

def copy(src, dst):

	try:     #  if no error do this 
            shutil.copytree(src, dst)
	except OSError as exc:  # if error handle in this way
	    if exc.errno == errno.ENOTDIR:
	         shutil.copyfile(src, dst)
	    elif os.path.isfile(src)==False:
	        print "cp: cannot stat "+dst+" : No such file or directory"
	    else: 
		raise
        except IOError :
	    print "cp: cannot stat "+dst+" : No such file or directory"
		
if len(l)==4 and l[0]=="cp" and l[1]=="-r": # case when cp src dst  
       copy(l[2],l[3])  # calling the function  cp 


if len(l)==3 and l[0]=="cp" :
      copy(l[1],l[2])


def mv(src, dest):
	try:
	    shutil.move(src, dest)  # method to move file from src to dest
        except IOError:
	    print "mv: cannot stat "+dest+" : No such file or directory"

	    
if len(l)==3 and l[0]=="mv" : 
     mv(l[1],l[2])   # calling the function mv





     
if len(l)==2 and l[0]=="rm" :  # case when rm and a name 

         if os.path.isfile(l[1])==True:   # when given name is of existing file 
         
               os.remove(l[1])             
    	 
	 elif os.path.isfile(l[1])==False and os.path.isdir(l[1])==False:     # if given name is neither a directory nor a file name 
               
	       print "rm: cannot remove \'"+l[1]+"\' : No such file or directory" # returning error
    	 
	 elif os.path.isdir(l[1])==True:     # if it is a directory name but since  -r operand is missing it will throw an error
	       
	       print "rm: cannot remove \'"+l[1]+"\': Is a directory"
	       

elif len(l)==2 and l[0]=="rm" and l[1]=="-r" :    # case when it is rm -r but no file name is there  so an error will be shown 
         print "rm: missing operand"
	 print "Try 'rm --help' for more information."


elif len(l)==3 and l[0]=="rm" and l[1]=="-r" :    # case when rm -r directoryname
         if os.path.isdir(l[2])==False:       # if directory doesn't exist with the given name error will be raised 
	      print "rm: cannot remove \'"+l[2]+"\' : No such file or directory"

	 else:
	     shutil.rmtree(l[2])    # if not this will recursively delete the directory tree 


# function to compute the ls -l for simple files and directory
def ls_l(i):
	    w=""
	    avr=0
	    temp=[]
	    if os.path.isdir(i)==True and os.path.islink(i)==False: #if it is a directory appending 'd' 
	       w+="d"                        
	    elif os.path.islink(i)==True: # if it is link appending 'l' 
	       w+="l" 
	       avr=1
	       get=os.path.realpath(i).split('/')    #getting the name of the file \n
	       newavr=get[len(get)-1]                #and directory of while the i is link .
	    else:
	       w+="-"


	    z=str (oct(stat.S_IMODE(os.lstat(i).st_mode)))      # getting the permissions in octal format and converting it into string  
            z= list(z)      
	    for j in range(1,len(z)):
		if z[j]=="7":
		    w+="rwx"
		elif z[j]=="6":
		    w+="rw-"
		elif z[j]=="5":
		    w+="r-x"
		elif z[j]=="4":
		    w+="r--"
		elif z[j]=="2":
		    w+="-w-"
		elif z[j]=="1":
		    w+="--x"
		elif z[j]=="3":
		    w+="-wx"
		elif z[j]=="0":
		    w+="---"
            temp.append(w)
	    links=os.stat(i).st_nlink
	    linkshift=("%4d"%links)
	    temp.append(linkshift)
	    temp.append(pwd.getpwuid(os.stat(i).st_uid)[0])
	    temp.append(grp.getgrgid(os.stat(i).st_gid)[0])
	    siz=os.stat(i).st_size
	    size=("%6d"%siz)             
	    temp.append(size)
	    modtime=time.ctime(os.path.getmtime(i))
	    modtime=modtime.split()
	    newl3=modtime[3].split(':')
	    temp.append(modtime[1])
	    date=modtime[2]
	    temp.append(date)
	    temp.append(newl3[0]+":"+newl3[1])
	    if avr==0:
	       temp.append(i)
            else:
	       temp.append(i+" -> "+newavr)
            print ' '.join([str(iterator) for iterator in temp])	       


def ls_l1(x):	# function to compute ls -l when input is directory  
	lslist=os.listdir(x)
        lslist.sort()
        u=check_hidden(x)
        if u==0 :
	    os.chdir(x)          # changing the  directory to the path of input directory
	    for k in lslist:
		m=check_hidden(k)
		if m==0:
	          ls_l(k)

	    
	    
if len(l)>=2 and l[0]=="ls" and l[1]=="-l":           # case when the input is ls -l .....
   if len(l)==2:        # case when input is ls -l only
     x="."
     ls_l1(x)      #calling the function ls_l1()
   elif len(l)>2 and os.path.isdir(l[2])==True:       #case when the input is ls -l dirname ....
     ls_l1(l[2])
   elif len(l)>2 and os.path.isfile(l[2])==True:        #case  when the input is ls -l filename ...
     ls_l(l[2])             #caling the function ls_l()

   elif os.path.isdir(l[2])==False and os.path.isfile(l[2])==False:        # case when given filename or dirname not exist
        print "ls : cannot access "+ l[2]+" : No such file or directory"


def list_files(startpath):
	for root, dirs, files in os.walk(startpath):            #os.walk returns tuple of 3 entries
		level = root.replace(startpath, '').count(os.sep)+1     #counting level of each directory 
		indent = '#'+'-' * 5* (level)       # indenting pattern
		if level==1:      # if it is root of  the directory tree 
		        print('{} {}{}/ {}'.format(indent,"Folder Name:  " ,os.path.basename(root),indent[::-1]))  # print this 
		else:            # else for any other directory   
		        print ('{}{}'.format(' '*5*(level),"|"))  # print this 
		        print ('{}{}{}/ {}'.format(' '*5*(level),indent,os.path.basename(root),indent[::-1]))
		subindent = ' ' * 5 * (level + 1)+"#"
		count=0       # count variable for counting number of files in directory 
		for f in files:
		     count+=1     
		if count ==0:
		     print ' '*5*(level+1)+"(EMPTY FOLDER)"      # if empty folder print this 
 		else:

    	             for f in files:            # for every file print this in this format 
		           print ('{}{}'.format(' '*5*(level+1),"|"))
		           print('{}{}{}'.format(subindent,"-" ,f))




		           

if len(l)==1 and l[0]=="dirstr":
	list_files(".")

elif len(l)==2 and l[0]=="dirstr" :
	if (os.path.isdir(l[1])==True ):
		list_files(l[1])
        else:
    	        print ('{} {}'.format(l[1]," [error opening dir]"))
    	        print ""
    	        print "0 directories, 0 files"

if len(l)==2 and l[0]=="ls" and l[1]=="-a" :
      w=""
      lslist =os.listdir(".")
      lslist.sort()
      for i in lslist:
          w+=i+" "
      print w



elif len(l)>2 and l[0]=="ls" and l[1]=="-a" and os.path.isdir(l[2])==True:
      w=""
      lslist=os.listdir(l[2])
      lslist.sort()
      for i in lslist:
            w+=i+" "
      print w
