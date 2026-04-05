import os
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()
api_key = os.getenv("OPENROUTER_API_KEY")

def get_code_summary():
    """Project ki files padh kar ek text summary banata hai."""
    summary = ""
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith(('.', 'venv', 'tests'))]
        for file in files:
            if file.endswith(('.py', '.txt', '.md')) and file != ".env":
                summary += f"\n--- File: {file} ---\n"
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        summary += f.read()[:500] # Pehle 500 characters
                except: pass
    return summary

def generate_readme():
    console.print(Panel("[bold cyan]🏗️ AI-Doc Architect: Generating Professional README...[/bold cyan]"))
    code_context = get_code_summary()
    
    prompt = f"""
    You are a Senior Open Source Maintainer. 
    Based on this code context:
    {code_context}
    
    Write a high-quality, professional GitHub README.md in Markdown format.
    Include sections: Project Name, Why it exists, Features, and Tech Stack.
    Keep it professional and 'enterprise-grade'.
    """

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"},
            json={
                "model": "google/gemma-3-4b-it:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        result = response.json()
        if "choices" in result:
            markdown = result["choices"][0]["message"]["content"]
            # Nayi file mein save karo
            with open("AI_GENERATED_README.md", "w") as f:
                f.write(markdown)
            console.print("\n[bold green]✅ Success! Professional README generated in 'AI_GENERATED_README.md'[/bold green]")
        else:
            console.print(f"[bold red]❌ API Error: {result}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")

if __name__ == "__main__":
    generate_readme()