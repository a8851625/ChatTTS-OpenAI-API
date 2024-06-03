# ChatTTS-OpenAI-API
The `ChatTTS-OpenAI-API` is a project built upon the `ChatTTS` framework, implementing the v1/audio/speech endpoint in compliance with OpenAI protocols to transform text into speech.
## Requirements
- Python 3.8+
- FastAPI
- Pydantic
## Getting Started
1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Run the server with `uvicorn main:app --reload`
## Usage
The main endpoint is `/v1/audio/speech`, which takes a POST request with the following parameters:
- `model`: (required) The model to use for the speech synthesis.
- `input`: (required) The text to be transformed into speech.
- `voice`: (optional) The voice to use for the speech synthesis. Default is 'alloy'.
- `response_format`: (optional) The format of the response audio file. Default is 'wav'.
- `speed`: (optional) The speed of the speech. Default is 1.0.
- `temperature`: (optional) The randomness of the speech. Default is 0.3.
- `prompt`: (optional) The prompt to use for the speech synthesis. Default is '[oral_2][laugh_0][break_6]'.
The `voice` parameter can take the following values: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'. If an unrecognized voice is provided, 'alloy' will be used.
Example request:
```json
{
    "model": "model_name",
    "input": "Hello, world!",
    "voice": "nova"
}
```
This will return an audio file with the synthesized speech.
## Error Handling
If a required parameter is missing, a 400 error will be returned. If an error occurs during the speech synthesis process, a 500 error will be returned.
```
Please adjust the above as needed for your project.

