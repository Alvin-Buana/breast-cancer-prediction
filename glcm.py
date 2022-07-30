import cv2
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os

props = [
        "energy",
        "homogeneity",
        "contrast",
        "correlation"
        ]
degrees = [0,45,90,135]

DATASET_PATH = './tmp/dataset.csv'
TEST_PATH = './tmp/test.csv'

def kolom():
    """
    memberikan rotasi berapa derajat (degrees) pada nama tiap kolom (props)
    """
    col = []
    for degree in degrees:
        for prop in props:
            col.append(prop+'('+str(degree)+')')
    return col


def glcm_per_image(img):
    """
    memperoses glcm untuk semua derajat per satu gambar

    in: string (img, path ke gambar)
    out: 
    list (value, nilai mentah)
    dataframe (buat predict nanti sama disimpen ke csv)
    """
    row = []
    value = []
    file = img.split("/")[-1]
    img_read = cv2.imread(img,0)
    name_gray = "tmp/img/"+file[:-4]+" gray.jpg"
    # cv2.imwrite(name_gray,img_read)
    # image_disp = {
    #     'original'  : img,
    #     'gray'      : name_gray,
    # }
    for degree in degrees:
        glcm = graycomatrix(img_read, [5], [degree], symmetric=True, normed=True)
        ro = []
        ro.append(degree)
        for prop in props:
            ro.append(float(graycoprops(glcm, prop)))
            row.append(float(graycoprops(glcm, prop)))
        value.append(ro)
    
    # return image_disp, value, pd.DataFrame([row],columns=kolom())
    return value, pd.DataFrame([row],columns=kolom())

def labeling(glcm_data , label):
    """
    memberikan label pada tiap hasil glcm lalu dijadikan dataframe

    in: 
    dataframe (l_data, sebuah dataframe isinya label)
    out:
    dataframe (data, dataframe hasil glcm tapi ada labelnya)
    """
    data = glcm_data[1]
    data['label'] = label
    return data

def svm_predict(img):
    """
    predict menggunakan SVM
    in:
    string (img, lokasi gmabar)
    out:
    list of float (hasil glcm)
    string (label prediksi)
    """
    glcm_df = pd.read_csv(DATASET_PATH)
    X = glcm_df.drop('label',axis=1)
    Y = glcm_df['label']
    clf = svm.SVC(decision_function_shape='ovr')
    clf.fit(X, Y)
    #l, x,res = glcm_per_image(img)
    #return l,x, clf.predict(res)[0]
    x,res = glcm_per_image(img)
    return x, clf.predict(res)[0]

def create_dataset(data_train_path):
    data = pd.DataFrame()
    for folder_name in os.listdir(data_train_path):
        print(folder_name)
        images = os.path.join(data_train_path,folder_name)
        # print(images)
        for image_name in os.listdir(images):
            print(image_name)
            image = os.path.join(images, image_name)
            glcm_result = glcm_per_image(image)
            data = pd.concat([data,labeling(glcm_result,str(folder_name))],
            ignore_index = True)
    data.to_csv(DATASET_PATH, index=False)
    print("dataset created! Snapshot:")
    print(data[:5])

def evaluate(data_test_path):
    #basically melakukan hal yang sama dengan create dataset
    #dari ini
    data = pd.DataFrame()
    for folder_name in os.listdir(data_test_path):
        images = os.path.join(data_test_path,folder_name)
        for image_name in os.listdir(images):
            image = os.path.join(images, image_name)
            glcm_result = glcm_per_image(image)
            data = pd.concat([data,labeling(glcm_result,str(folder_name))],
            ignore_index = True)
    data.to_csv(TEST_PATH, index=False)
    #sampai ini

    #fit model seperti fungsi svm_predict
    glcm_df = pd.read_csv(DATASET_PATH)
    X = glcm_df.drop('label',axis=1)
    Y = glcm_df['label']
    clf = make_pipeline(StandardScaler(), 
        svm.SVC(gamma='auto',
                kernel = 'rbf',
                C = 10.0,
                decision_function_shape='ovr'
                ))
    #clf = svm.SVC()
    clf.fit(X, Y)
    #sampai ini

    test = pd.read_csv(TEST_PATH)
    testX = test.drop('label',axis=1)
    testy = test['label']

    hasilX = clf.predict(testX)
    confus = confusion_matrix(testy,hasilX)
    ConfusionMatrixDisplay(confus,display_labels=('benign', 'malignant')).plot()
    confusion = "./tmp/confus.jpg"
    plt.savefig(confusion)
    print("Akurasi: ",accuracy_score(testy,hasilX))

    return  accuracy_score(testy,hasilX)
