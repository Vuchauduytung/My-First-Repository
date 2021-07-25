import tensorflow as tf
from keras.models import load_model

#model_direct_path = r"Data\breast_cancer_report2.h5"
model = load_model(r"E:\data\Tùng\CV\L02_Nhom09\L02_Nhom09\BreastCancerDetection4\BreastCancerDetection4\Data\breast_cancer_report_final.h5")


direct_path = r"E:\data\Tùng\CV\L02_Nhom09\L02_Nhom09\BreastCancerDetection4\BreastCancerDetection4\Data\Original\Test\Malignant"



validation_split=None
label_mode = None
subset=None
seed = None
image_size = (25,25)
batch_size = 32

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    direct_path,
    validation_split=validation_split,
    label_mode = label_mode,
    subset=validation_split,
    seed=seed,
    image_size=image_size,
    batch_size=batch_size,
    )

result = model.predict(x = test_ds, 
                       batch_size=batch_size, 
                       verbose=0)
import numpy as np
unique, counts = np.unique(result[:,1]<0.5, return_counts=True)
print(dict(zip(unique, counts)))
