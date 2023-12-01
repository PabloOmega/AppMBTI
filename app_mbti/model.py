
import numpy as np
import pandas as pd
import tensorflow as tf
from .api import CommonMethods
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from pycaret.classification import *

model_types = ["E vs I","S vs N","T vs F","J vs P"]
weight_paths = ["app_mbti/pesos/E_vs_I_Red_Neuronal.h5",
                "app_mbti/pesos/S_vs_N_Red_Neuronal.h5",
                "app_mbti/pesos/T_vs_F_Red_Neuronal.h5",
                "app_mbti/pesos/J_vs_P_Red_Neuronal.h5"]
mean_paths = ["app_mbti/mean_std/Mean_Std_E_vs_I.csv",
              "app_mbti/mean_std/Mean_Std_S_vs_N.csv",
              "app_mbti/mean_std/Mean_Std_T_vs_F.csv",
              "app_mbti/mean_std/Mean_Std_J_vs_P.csv"]

class Model:
    """
    Permite definir una plantilla para los cuatro modelos entrenados de inteligencia emocional
    Atributos:
        model_num: Número de modelo (0: E vs I, 1: S vs N, 2: T vs F, 3: J vs P)
        mean: Guarda la media de los datos originales para poder normalizar los datos
        std: Guarda la desviación estándar de los datos originales para poder normalizar los datos
        model: Guarda el modelo (red neuronal o ML) que permite generar una respuesta en función de la entrada
        
    Métodos:
        Constructor: __init__
        build_network(): Permite construir y cargar los pesos de la red neuronal entrenada por cada tipo de modelo (Modelos
                        de 0 a 2)
        load_ML_model(): Permite cargar el modelo de Machine Learning entrenado (Modelo 3)
        model_output(): Genera la respuesta del modelo en función del texto de entrada
        normalize(): Normaliza los datos de entrada para que se adecuen a los datos de entrenamiento
        
    """    
    def __init__(self, model_num: int, mean_path, weight_path):
        """
        Constructor del objeto
        Parámetros:
            model_num: Número de modelo (0: E vs I, 1: S vs N, 2: T vs F, 3: J vs P)      
        """      
        self.model_num = model_num
        
        if model_num == 4:
            self.load_ML_model()
        else:
            mean_std = pd.read_csv(mean_paths[model_num])
            self.mean = np.array(mean_std.loc[0,:])
            self.std = np.array(mean_std.loc[1,:])

            self.build_network(weight_path)
        
    def build_network(self, weight_path):
        """
        Permite construir y cargar los pesos de la red neuronal entrenada por cada tipo de modelo (Modelos de 0 a 2)
        """           
        self.model = Sequential()
        
        neurons_layer = [1024, 512, 64]

        if self.model_num == 2 or self.model_num == 3:
            neurons_layer[0] = 2048
            neurons_layer[2] = 128
        
        self.model.add(Dense(units=neurons_layer[0], activation='relu', input_shape=(1536, )))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(Dense(units=neurons_layer[1], activation='relu'))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(Dense(units=neurons_layer[2], activation='relu'))
        self.model.add(tf.keras.layers.Dropout(0.5))    
        self.model.add(Dense(units=2, activation='softmax'))
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])        
               
        #self.model.load_weights(model_types[self.model_num] + " Red Neuronal.h5")
        #self.model.load_weights(Weight.objects.get(name=model_types[self.model_num]).weights_file.path)
        self.model.load_weights(weight_paths[self.model_num])
        self.model.summary()   
        
    def load_ML_model(self):
        """
        Permite cargar el modelo de Machine Learning entrenado (Modelo 3)
        """           
        self.model = load_model('ML ' + model_types[self.model_num])

    def model_output(self, text: str):
        """
        Genera la respuesta del modelo en función del texto de entrada
        Parámetros:
            text: texto de entrada para procesarlo y generar la respuesta a través del modelo
        Retorno:
            Retorna la salida del modelo independientemente si es Red Neuronal o un algoritmo ML
        """           
        text = CommonMethods.translate_text(text)
        
        if self.model_num == 4:
            words_vector = self.openai_embedding(text) 
            y_pred = predict_model(self.model, data=pd.DataFrame([words_vector]))
            print(f"Resultado: {y_pred.loc[0,'prediction_label']},{y_pred.loc[0,'prediction_score']}")
            return y_pred.loc[0,'prediction_label']
        else:
            embeddings = CommonMethods.openai_embedding(text) 
            print(len(embeddings))
            embeddings = self.normalize(embeddings)
            y_pred = self.model.predict(np.array([embeddings]))
            print(f"Resultado: {y_pred}")
            return y_pred[0][0]
        
    def normalize(self, embeddings):
        """
        Normaliza los datos de entrada para que se adecuen a los datos de entrenamiento
        Parámetros:
            embeddings: vectores de texto a ser normalizados de acuerdo a los datos de entrenamiento
        Retorno:
            Retorna los vectores de texto normalizados
        """                
        return (embeddings - self.mean) / self.std          