Act as a professional AI engineer. 

Our task is to create a dataset for fine tuning. 
We are finetuning a model that extracts search filters from a user_input.

The script takes as input a csv file, with only one column, user_inputs. 

It feeds this column to the LLM. The system prompts asks for a reponse inside which there are <jsonl_response></jsonl_response> tags, with the jsonl line inside them. Our script must take this llm response, get only the contents inside the tags, and create a new line in a new file, called training_set.csv, with two columns, user_input and filters_json. The user_input column is EXACTLY the same as the input column. The script must write one line at a time, so we don't loose progress. If the script fails, or execution stops, the script must be able to restart from the last completed line. 

The base for the script (connection to aws, etc.) is in 1_generate_jsonl_response.py. Change this file so that it fulfills all the requirements above. 

The script should use both input and output variables for files reading/writing.

before coding, tell me if the task is clear, if it makes sense. Ask me any clarifying questions. 