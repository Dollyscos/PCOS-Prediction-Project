import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.cm as cm


def get_img_array_from_pil(pil_image, size=(224, 224)):
    img = pil_image.resize(size).convert("RGB")
    arr = np.array(img).astype("float32")
    arr = np.expand_dims(arr, axis=0)
    return arr


def make_gradcam_heatmap_resnet_manual(
    pil_image,
    model,
    class_index=1,
    img_size=(224, 224),
    aug_layer_name="data_augmentation",
    base_model_name="resnet50",
    gap_layer_name="global_average_pooling2d_1",
    dropout_layer_name="dropout_1",
    dense_layer_name="dense_1",
):
    img_array = get_img_array_from_pil(pil_image, size=img_size)

    aug_layer = model.get_layer(aug_layer_name)
    base_model = model.get_layer(base_model_name)
    gap_layer = model.get_layer(gap_layer_name)
    dropout_layer = model.get_layer(dropout_layer_name)
    dense_layer = model.get_layer(dense_layer_name)

    kernel, bias = dense_layer.get_weights()

    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)

    with tf.GradientTape() as tape:
        x = aug_layer(img_tensor, training=False)
        x = tf.keras.applications.resnet50.preprocess_input(x)

        conv_outputs = base_model(x, training=False)
        tape.watch(conv_outputs)

        x = gap_layer(conv_outputs)
        x = dropout_layer(x, training=False)

        logits = tf.linalg.matmul(x, kernel) + bias
        preds = tf.sigmoid(logits)

        if class_index == 1:
            class_channel = logits[:, 0]
        else:
            class_channel = -logits[:, 0]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)

    heatmap = tf.maximum(heatmap, 0)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)

    return heatmap.numpy(), float(preds[0, 0].numpy())


def overlay_gradcam_on_pil(pil_image, heatmap, alpha=0.35):
    original = pil_image.convert("RGB")

    heatmap_uint8 = np.uint8(255 * heatmap)
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap_uint8]
    jet_heatmap = np.uint8(jet_heatmap * 255)

    heatmap_img = Image.fromarray(jet_heatmap).resize(original.size)
    overlay = Image.blend(original, heatmap_img.convert("RGB"), alpha=alpha)

    return overlay

