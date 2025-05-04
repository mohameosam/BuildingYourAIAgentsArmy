import torch
import torch_pruning as tp
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

logging.basicConfig(filename="prune.log", level=logging.INFO)

def prune_llama3(model_name="llama3", sparsity=0.3):
    # Load model (simplified for Ollama; use local path if exported)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model.eval()

    # Define pruning strategy (30% sparsity)
    pruner = tp.pruner.MagnitudePruner(
        model,
        example_inputs=torch.randn(1, 128, model.config.hidden_size),
        importance=tp.importance.MagnitudeImportance(),
        iterative_steps=5,
        ch_sparsity=sparsity
    )

    # Prune
    for i in range(5):
        pruner.step()
        logging.info(f"Pruning iteration {i+1}/5")

    # Fine-tune (simplified)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    sample_input = tokenizer("What is item ABC?", return_tensors="pt")
    for _ in range(10):
        outputs = model(**sample_input)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        logging.info(f"Fine-tuning loss: {loss.item()}")

    # Save
    model.save_pretrained("pruned_llama3")
    tokenizer.save_pretrained("pruned_llama3")
    logging.info("Pruned model saved")

if __name__ == "__main__":
    prune_llama3()

    
    
# Run the script from bash:
#
# python prune_model.py