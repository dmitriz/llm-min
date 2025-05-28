import openai

# Constants
DEFAULT_MODEL = "gpt-4o-mini"  # Cheapest OpenAI model
USER_ROLE = "user"

def text_chat(api_key, model=DEFAULT_MODEL):
  """
  Create a text chat function for OpenAI.
  
  Args:
    api_key (str): API key for OpenAI
    model (str): Model name to use (default: gpt-4o-mini - cheapest option)
  
  Returns:
    function: A send_message function that takes a message and returns a response
  """
  def send_message(message):
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
      model=model,
      messages=[{"role": USER_ROLE, "content": message}]
    )
    return response.choices[0].message.content
  
  return send_message
