import os
import lazyImage as li
import pickle

#TODO : make load more os independent 
#TODO turn this to class with : dump , smart_load
class lazyDataset(object):
    """ lazy reading of dataset set
    """
    def __init__(self
            ,path = "/home/loxymondor/docs/facu/Gproj/Proj/DataSet/EgyptianHieroglyphDataset/ExampleSet7/train/"
            ,seprator="/" # Warning os dependent
            ,labeled=False
            ,lazy=True,save_path="./data/lazyDataset.ss"):
        """ __init__ (path,seprator)
        this method assumes that each folder name is the lable of the images it contains.
        path : is dir of dataset
                must end with a seprator 
                example : /home/s/d/ is right
                          /home/s/d is wrong

        seprator : is the os seprator 
                linux -> /
                win   -> \\
        ## not implemented
        save_path : file path to use to load-dump the result.
        lazy : True  : check first if data avilable .
               False : load and compile dataset .
        ------
        out : lazyImage array
        """
# check (strict) *-> load 
#                *-> read -> dump 
        self.path=path
        self.seprator=seprator
        self.lazy=lazy
        self.save_path=save_path
        self.images=[]

    def load(self):
        if self.lazy == True :
            self.__lazy_load__()
        else :
            self.__strict_load__()
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
        root= os.listdir(self.path) #list of directory files
        for label in root :
            if os.path.isdir(self.path+label): 
                imgs=os.listdir(self.path+label)
                for img in imgs: 
                    images.append(
                        li.Image(
                             self.path+self.seprator
                            +label+self.seprator+img))
        self.images=li.Image.toXy(images)

#        images=pickle.load( open("./data/lazyDataset.ss", 'rb'))
#           pickle.dump(images, open(save_dir, 'wb'))
#        if save_dir != "" :