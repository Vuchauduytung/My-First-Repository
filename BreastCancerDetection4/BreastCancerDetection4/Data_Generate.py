import tensorflow as tf

direct_path="Data/Train"
def LoadData(direct_path, image_size, batch_size, seed):
    
    # Train dataset
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    direct_path,
    validation_split=0.2,
    subset="training",
    seed=seed,
    image_size=image_size,
    batch_size=batch_size,
    )       # shuffle = True, batch_size = 32
    
    # Validate dataset
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    direct_path,
    validation_split=0.2,
    subset="validation",
    seed=seed,
    image_size=image_size,
    batch_size=batch_size,
    )       # shuffle = True, batch_size = 32
    
    return (train_ds, val_ds)