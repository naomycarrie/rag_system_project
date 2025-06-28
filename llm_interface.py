import subprocess

def run_llama_cpp(prompt, model_path, n_predict=128):
    command = [
        "/home/ubuntu/llama.cpp/build/bin/llama-cli",
        "-m", model_path,
        "-p", prompt,
        "-n", str(n_predict),
        "--temp", "0.7",
        "--top-k", "40",
        "--top-p", "0.5",
        "--repeat-penalty", "1.1",
        "--color",
        "-i",
        "-r", "User:",
        "-f", "/home/ubuntu/llama.cpp/prompts/chat-with-bob.txt"
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error running llama.cpp: {error}")
    return output

if __name__ == "__main__":
    model_path = "/home/ubuntu/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf"
    initial_prompt = "Olá, como posso ajudar hoje?"
    print("Modelo LLM local carregado. Digite suas perguntas (digite 'sair' para encerrar):\n")

    while True:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            break
        
        full_prompt = f"User: {user_input}\nAssistant:"
        response = run_llama_cpp(full_prompt, model_path)
        print(f"LLM: {response.strip()}")


