from transformers import AutoTokenizer, AutoModel
import torch
import onnx

model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

dummy_input = tokenizer("test", return_tensors="pt", padding=True, truncation=True)

torch.onnx.export(
    model,
    (dummy_input["input_ids"], dummy_input["attention_mask"]),
    "model.onnx",
    export_params=True,
    opset_version=11,
    input_names=["input_ids", "attention_mask"],
    output_names=["output"]
)