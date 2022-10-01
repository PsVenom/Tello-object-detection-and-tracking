import cv2
import numpy as np
import onnx
import onnxruntime
import os
import torch

def pytorch_onnx(onnx_model_path, input_image):
    # get onnx result
    session = onnxruntime.InferenceSession(onnx_model_path)
    input_name = session.get_inputs()[0].name
    onnx_result = session.run([], {input_name: input_image})
    onnx_result = np.squeeze(onnx_result, axis=0)

    for test_onnx_result in zip(onnx_result):
        print(test_onnx_result)

def get_onnx_model(
    original_model, input_image, model_path="models", model_name="pytorch_mobilenet",
):
    # create model root dir
    os.makedirs(model_path, exist_ok=True)

    model_name = os.path.join(model_path, model_name + ".onnx")

    torch.onnx.export(
        original_model, torch.Tensor(input_image), model_name, verbose=True,
    )
    print("ONNX model was successfully generated: {} \n".format(model_name))

    return model_name

cap=cv2.imread('../../../Pictures/drone-im/drone-im/images/_0_14.jpeg')
img = cap.reshape((1,cap.shape[0],cap.shape[1],cap.shape[2]))
print(img.shape)
pytorch_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

torch.onnx.export(
      pytorch_model,
      [cap],
      "yolodrone.onnx")
    # check if conversion succeeded
# onnx_model = onnx.load(onnx_model_path)
# onnx.checker.check_model(onnx_model)
# pytorch_onnx(onnx_model, cap)