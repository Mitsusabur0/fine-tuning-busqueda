# CELL 1: INSTALL DEPENDENCIES
# Unsloth is optimized for NVIDIA GPUs like your T4.
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps xformers "trl<0.9.0" peft accelerate bitsandbytes
!pip install pandas scikit-learn datasets

# CELL 2: DATA PREPROCESSING AND SPLITTING
import pandas as pd
import json
from sklearn.model_selection import train_test_split

SYS_PROMPT = """
You will receive a `user_input`: a message written in Spanish by a user interacting with an AI concierge on a Chilean real estate/banking platform.

Your task is to extract search filters from that `user_input`.

These filters apply to the search for properties available for purchase.

Output requirements:
- Return exactly one JSON object wrapped between these tags: `<json_response></json_response>`.
- Do not include any text outside those tags.
- Only use filters from the predefined list below.
- Never invent filters that are not explicitly requested by the user.

There is a defined list of possible filters. You cannot add filters outside this list.

possible_filters =
{
    "tipo_inmueble": {
        "type": "string",
        "enum": ["casa", "departamento"],
        "description": "SOLO 'casa' o 'departamento'. Si aparecen ambos, usa solo 'departamento'"
    },
    "comuna": {
        "type": "string",
        "description": "Nombre de la comuna en Chile (ej. 'Las Condes', 'Santiago') o región."
    },
    "dormitorios": {
        "anyOf": [
            {"type": "integer"},
            {"type": "array", "items": {"type": "integer"}}
        ],
        "description": "Cantidad de dormitorios. Puede ser un número exacto o un arreglo [min, max]"
    },
    "banos": {
        "anyOf": [
            {"type": "integer"},
            {"type": "array", "items": {"type": "integer"}}
        ],
        "description": "Cantidad de baños. Puede ser un número exacto o un arreglo [min, max]. Puede estar en texto o como '2b' o '3d'."
    },
    "precio_min": {
        "type": "number",
        "description": "Valor mínimo o exacto del precio"
    },
    "precio_max": {
        "type": "number",
        "description": "Valor máximo o exacto del precio"
    },
    "moneda": {
        "type": "string",
        "enum": ["UF", "CLP"],
        "description": "Tipo de moneda del precio ('UF' o 'CLP')"
    },
    "superficie_min": {
        "type": "number",
        "description": "Superficie mínima en m²"
    },
    "superficie_max": {
        "type": "number",
        "description": "Superficie máxima en m²"
    },
    "estacionamientos": {
        "type": "integer",
        "description": "Cantidad de estacionamientos"
    },
    "bodegas": {
        "type": "integer",
        "description": "Cantidad de bodegas"
    },
    "sostenibilidad_certificada": {
        "type": "boolean",
        "description": "Amenidad: sostenibilidad certificada"
    },
    "con_subsidio": {
        "type": "boolean",
        "description": "Amenidad: con subsidio"
    },
    "piscina": {
        "type": "boolean",
        "description": "Amenidad: piscina"
    },
    "areas_verdes": {
        "type": "boolean",
        "description": "Amenidad: áreas verdes"
    },
    "gimnasio": {
        "type": "boolean",
        "description": "Amenidad: gimnasio"
    },
    "salon_eventos": {
        "type": "boolean",
        "description": "Amenidad: salón de eventos"
    },
    "zona_educacion": {
        "type": "boolean",
        "description": "Zonas: SOLO si menciona colegio, escuela, universidad"
    },
    "zona_transporte": {
        "type": "boolean",
        "description": "Zonas: SOLO si menciona metro, bus, transporte público"
    },
    "zona_centros_salud": {
        "type": "boolean",
        "description": "Zonas: SOLO si menciona hospital, clínica, centro médico"
    }
}

Extraction rules:
- Add a filter only if the user is clearly requesting it.
- Never add a filter the user did not ask for.
- If the `user_input` has no clear filters from the list, return an empty JSON object.
- User messages may include typos, misspellings, or informal phrasing. Infer the most likely intended meaning.
- If multiple comunas are mentioned, use the first one mentioned.
- If no comuna is mentioned but a region is mentioned, place the region in the `comuna` filter.
- Make sure to start your output with <json_response> and to end it with </json_response>. DO NOT include ANYTHING else.

Now extract the filters from the following `user_input`:
""".strip()

# Load raw data
df = pd.read_csv("full_dataset.csv", encoding="utf-8")
processed_data = []

for index, row in df.iterrows():
    user_text = str(row['user_input']).strip()
    json_text = row['filters_json']
    
    if pd.isna(json_text) or str(json_text).strip() == "":
        json_text = "{}"
    else:
        json_text = str(json_text).strip()
        
    try:
        parsed_json = json.loads(json_text)
        clean_json_string = json.dumps(parsed_json, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        continue # Skip invalid rows
        
    assistant_content = f"<json_response>\n{clean_json_string}\n</json_response>"
    
    example = {
        "messages": [
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    processed_data.append(example)

# Split 80 / 10 / 10
train_val_data, test_data = train_test_split(processed_data, test_size=0.10, random_state=42)
train_data, val_data = train_test_split(train_val_data, test_size=0.1111, random_state=42) # 0.1111 of 0.90 is 0.10

# Save to jsonl
def save_jsonl(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

save_jsonl(train_data, "train.jsonl")
save_jsonl(val_data, "val.jsonl")
save_jsonl(test_data, "test.jsonl")

print(f"✅ Data processed and split: Train({len(train_data)}), Val({len(val_data)}), Test({len(test_data)})")




# CELL 3: LOAD LLAMA 3.2 3B IN 4-BIT
from unsloth import FastLanguageModel
import torch

max_seq_length = 2048 # Maximum context window. 2048 is perfect for your prompt.
dtype = None # Auto detection
load_in_4bit = True # Crucial for T4 GPU

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-3B-Instruct",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

print("✅ Model and Tokenizer loaded successfully!")








# CELL 4: CONFIGURE LORA ADAPTERS
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Rank. 16 is standard and highly effective.
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, 
    bias = "none",    
    use_gradient_checkpointing = "unsloth", # Reduces VRAM usage massively
    random_state = 3407,
)

print("✅ LoRA adapters applied. Ready for training.")







# CELL 5: PREPARE DATASETS FOR TRAINING
from datasets import load_dataset

train_dataset = load_dataset("json", data_files="train.jsonl", split="train")
val_dataset = load_dataset("json", data_files="val.jsonl", split="train")

# Apply Chat Template
def format_chat(example):
    # This turns the JSON messages into the raw text with <|start_header_id|> tags
    example["text"] = tokenizer.apply_chat_template(example["messages"], tokenize=False)
    return example

train_dataset = train_dataset.map(format_chat, batched=False)
val_dataset = val_dataset.map(format_chat, batched=False)

print(f"✅ Formatted {len(train_dataset)} training rows and {len(val_dataset)} validation rows.")






# CELL 6: START FINE-TUNING
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = train_dataset,
    eval_dataset = val_dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10, # Warms up the learning rate
        num_train_epochs = 1, # Set to 2 or 3 if the dataset is small (<500 rows)
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(), # T4 uses fp16
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 10,
        evaluation_strategy = "steps",
        eval_steps = 50, # Calculates validation loss every 50 steps
        optim = "adamw_8bit", # Saves VRAM
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none", # Turns off WandB logging
    ),
)

print("🚀 Starting training...")
trainer_stats = trainer.train()
print("🎉 Training Complete!")





# CELL 7: SAVE THE LORA ADAPTERS
model.save_pretrained("llama_json_extractor_lora")
tokenizer.save_pretrained("llama_json_extractor_lora")
print("✅ LoRA adapters saved successfully to ./llama_json_extractor_lora")




# CELL 8: TEST THE TRAINED MODEL
import random

# Enable native inference speedups in Unsloth
FastLanguageModel.for_inference(model)

# Load the test dataset
with open("test.jsonl", "r", encoding="utf-8") as f:
    test_lines = f.readlines()

# Pick a random test example
sample_line = json.loads(random.choice(test_lines))
messages = sample_line["messages"]

# We only want to feed the System and User prompt to the model so it can generate the Assistant part
input_messages = [messages[0], messages[1]] 
actual_answer = messages[2]["content"]

# Format and Tokenize
inputs = tokenizer.apply_chat_template(
    input_messages,
    tokenize = True,
    add_generation_prompt = True, # Adds the final <|start_header_id|>assistant tag
    return_tensors = "pt",
).to("cuda")

print("🔹 USER INPUT:")
print(messages[1]["content"])
print("\n" + "="*40 + "\n")

# Generate response
outputs = model.generate(input_ids = inputs, max_new_tokens = 512, use_cache = True)
decoded_output = tokenizer.batch_decode(outputs)[0]

# Extract just the newly generated part
generated_text = decoded_output.split("<|start_header_id|>assistant<|end_header_id|>")[1].replace("<|eot_id|>", "").strip()

print("🤖 MODEL OUTPUT:")
print(generated_text)

print("\n" + "="*40 + "\n")
print("🎯 ACTUAL EXPECTED OUTPUT (From Test Set):")
print(actual_answer)