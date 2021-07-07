import os
import lazyImage as li
import pickle
from pathlib import Path
#~ import pandas as pd
#~ from numpy import flip, array

## minor improves
#DONE : make load more os independent 
#DONE : turn this to class with : dump , smart_load
#TODO : imporve to load recursively all images in the dir.
#TODO : update docmuentaion
#DONE : overload + 

## major improve 
#TODO : add handling for a list of paths or one path
#TODO : add drop to drop lables and there data 
#       in __strict_load__ and __lazy_load__
#TODO : overload + to work lazy   

class lazyDataset(object):
    """ lazy reading of dataset set
    """
    def __init__(self
            ,path = "./Dataset/ExampleSet7/train/"
            ,labeled=False
            ,lazy=True
            ,dump=True,save_path=Path("./data/lazyDataset.pkl")
            ,img_class=li.Image):
        """ lazyDataset(...)
        in :(all optional)
            path : images dataset path
            labeled (bool) : if the dataset have folders named 
                        as the label of it's contents.
            save_path : file path to use to load-dump the result.
            lazy : True  : check first if data avilable.
                   False : load and compile dataset.
            dump (bool) :to dump data to save_path or not. 
        ------
        out : use load() to get dataset as (X,y)
        """
# check (strict) *-> load 
#                *-> read -> dump 
        self.path=Path(path)
        self.lazy=lazy
        self.dump=dump
        self.save_path=Path(save_path)
        self.images=[]
        self.img_class=img_class

    def load(self):
        if self.lazy == True :
            self.__lazy_load__()
        else :
            self.__strict_load__()
        if self.dump == True :
            self.__dump__()
        return self.images
    
    def __dump__(self):
        pickle.dump(self.images,open(self.save_path, 'wb'))

    def __lazy_load__ (self):
        try :
            self.images=pickle.load(open(self.save_path, 'rb'))
        except:
            self.__strict_load__()

    def __strict_load__(self):
        """ reads dataset strictly
        """
        images = []
        root= self.path
        folders= os.listdir(root) #list of directory files
        for label in folders :
            if (root / label).is_dir() : 
                imgs=os.listdir(root / label)
                for img in imgs: 
                    images.append(
                        self.img_class(root / label / img))
        self.images=self.img_class.toXy(images)

    def asDataFrame(self):
        return toDataFrame(self.load());
    
    def __add__(self,other):
        (X,y)  = self.load()
        (X_,y_)= other.load()
        return (X+X_,y+y_)


def summary(Xs_ys):
    try :
      X,y=Xs_ys
      y_=set(y)
      print ( "Summary :\n"
                  +"data : "+str(len(X))
              +"\t labels: "+str(len(y))
              +"\nuniqe labels: "+str(len(y_))+" \n"+str(y_))
    except:
        print ("error input of type : "+str(type(result)))

def drop(T,labels=[]):
    """ in : T : tuple with (X,y)
                where y is lables 
            lables : the lables to be droped
        out : tuple (X,y) without the droped labels
           and it's data
    """
    (a,b)=T
    (X,y)=(a.copy(),b.copy())
    for l in labels:
        try :
            while(l in y ):
                i= y.index(l)
                del(y[i]);del(X[i])
        except:
            continue
    return (X,y)

def pick(T,labels=[]):
    """ in : T : tuple with (X,y)
                where y is lables 
            lables : the lables to be droped
        out : tuple (X,y) with only the droped labels
           and it's data
    """
    (a,b)=T
    (X,y)=(a.copy(),b.copy())
    (X_,y_)=([],[])
    for l in labels:
        try :
            while(l in y ):
                i= y.index(l)
                y_.append(y[i]);X_.append(X[i])
                del(y[i]);del(X[i])
        except:
            continue
    return (X_,y_)

def rename(T,lables=[]):
    pass
def Dumpto(data,fname):
    pickle.dump(data,open(Path(fname), 'wb'))

def toDataFrame(T):
    import pandas as pd
    (X,y)=T
    data = pd.concat(
            [ 
            pd.DataFrame({'label':y}),
                pd.DataFrame(X)
            ],axis=1)
    return data

def concat(one=([],[]),other=([],[])):
    (X,y)  = one
    (X_,y_)= other
    return (X+X_,y+y_)

def sort_max(dataset):
    """ sort max first 
    """
    from numpy import flip, array
    (X,_)=dataset
    X_=[]
    for x in X :
        i=flip(array(x).argsort())
        X_.append(x[i])
    return (X_,dataset[1])
