from tensorflow.keras.preprocessing.image import ImageDataGenerator

image_size = (25,25)
batch_size = 32
train_direct_path = r"E:\data\Tùng\CV\L02_Nhom09\L02_Nhom09\BreastCancerDetection4\BreastCancerDetection4\Data\Original\NEW-train"
validation_direct_path = r"E:\data\Tùng\CV\L02_Nhom09\L02_Nhom09\BreastCancerDetection4\BreastCancerDetection4\Data\Original\NEW-val"

train_datagen = ImageDataGenerator(
      rotation_range=10,
      width_shift_range=0.1,
      height_shift_range=0.1,
      brightness_range=(-1,1),
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      vertical_flip=True,
      fill_mode='nearest',
      rescale=1./255,
#       validation_split=0.2
      )

val_datagen = ImageDataGenerator(
      rotation_range=10,
      width_shift_range=0.1,
      height_shift_range=0.1,
      brightness_range=(-1,1),
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      vertical_flip=True,
      fill_mode='nearest',
      rescale=1./255,
        )

train_generator = train_datagen.flow_from_directory(
        directory=train_direct_path,
        target_size=image_size,
        batch_size=batch_size,
        save_to_dir=None,
        save_prefix="train",
        save_format="png",
        # subset="training"
        )

val_generator = val_datagen.flow_from_directory(
        directory=validation_direct_path,
        target_size=image_size,
        batch_size=batch_size,
        save_to_dir=None,
        save_prefix="val",
        save_format="png",
        # subset="validation"
        )

