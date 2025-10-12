# Mini Rag Application
This is an implementation of RAG application for question & Answer

## Requirements
Python >= 3.8
#### Installation 
- Download Python from [Here](https://www.python.org/).
- Create virtual environment.
```bash
python -m venv mini-rag
```
- Activate the mini-rag env
```bash
.\mini-rag\Scripts\activate.bat
```
- Install requriements.
```bash
pip install -r requirement.txt
```
#### Setup environment variables.
```bash
cp .env.example .env
```
Set your environment variables in the `.env` file. like `OPENROUTER_API_KEY` value.
## Run FastAPI server
```bash
uvicorn main:app --reload --host localhost --port 5000
```
