from openai import OpenAI
import tiktoken
import os
from deep_translator import GoogleTranslator


class CommonMethods:
    client = OpenAI(
        organization=os.environ.get("ORG_OPENAI_KEY"),
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    enc = tiktoken.get_encoding("cl100k_base")  
    translator = GoogleTranslator(source='auto', target='en')

    @staticmethod
    def openai_embedding(text: str):
        """
        Genera los Embeddings del texto utilizando la API de OpenAI 
        Parámetros:
            text: texto a transformar en vectores o word embeddings
        Retorno:
            Retorna el vector de números originado a partir del texto
        """
        embeddings = CommonMethods.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text,
            encoding_format="float"
        )
        return embeddings.data[0].embedding

    @staticmethod
    def tokens_count(text: str):
        """
        Cuenta el número de tokens para calcular el precio de la API
        Parámetros:
            text: texto a transformar en tokens para proceder a contarlos
        Retorno:
            Retorna el número de tokens en la entrada
        """                    
        num_tokens = len(CommonMethods.enc.encode(text))
        print(f"Números de Tokens: {num_tokens}, Precio: ${num_tokens*0.0001/1000} USD")
        return num_tokens  

    @staticmethod
    def translate_text(text: str):
        """
        Permite traducir el texto de español a inglés utilizado Google Translate
        Parámetros:
            text: texto a traducir
        Retorno:
            Retorna el texto traducido
        """      
        print(text)
        translation = CommonMethods.translator.translate(text)
        return translation

    @staticmethod
    def speech_to_text(audio_path):
        
        with open(audio_path, "rb") as audio_file:
        #audio_file = open(audio_path, "rb")
            transcript = CommonMethods.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            return transcript.text
        
        return "No hay conexión con Whisper"
