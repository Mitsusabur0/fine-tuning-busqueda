# Standard language modeling
{"text": "The sky is blue."}

# Conversational language modeling
{"messages": [{"role": "system", "content": "You answer questions."},
              {"role": "user", "content": "It is blue."},
              {"role": "assistant", "content": "It is blue."}]}

# Standard prompt-completion
{"prompt": "The sky is",
 "completion": " blue."}

# Conversational prompt-completion
{"prompt": [{"role": "user", "content": "What color is the sky?"}],
 "completion": [{"role": "assistant", "content": "It is blue."}]}