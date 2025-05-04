from transformers import AutoModelForCausalLM, AutoTokenizer
import onnx
import onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType
import logging

logging.basicConfig(filename="quantize.log", level=logging.INFO)

def quantize_llama3(model_name="llama3"):
    # Export to ONNX (simplified)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    torch.onnx.export(
        model,
        (torch.randn(1, 128),),
        "llama3.onnx",
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
    )
    logging.info("Exported to ONNX")

    # Quantize to INT8
    quantize_dynamic(
        "llama3.onnx",
        "llama3_quantized.onnx",
        weight_type=QuantType.QInt8
    )
    logging.info("Quantized to INT8")

    # Test
    session = ort.InferenceSession("llama3_quantized.onnx")
    inputs = tokenizer("What is item ABC?", return_tensors="np")["input_ids"]
    outputs = session.run(None, {"input": inputs})[0]
    logging.info("Quantized model tested")

if __name__ == "__main__":
    quantize_llama3()

    
    
# Run the script from bash:
#
# python quantize_model.py