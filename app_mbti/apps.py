from django.apps import AppConfig
from .model import Model

model_types = ["E vs I","S vs N","T vs F","J vs P"]

class app_mbtiConfig(AppConfig):
    name = 'app_mbti'

    def ready(self) -> None:
        from .models import Weight        

        self.windows = {}
        
        for i in range(4):
            # Crea 4 objetos para cada modelo de la Inteligencia Emocional  
            print(Weight.objects.get(name=model_types[i]).mean_std.path.encode())
            self.windows[i] = Model(i,
                                    Weight.objects.get(name=model_types[i]).weights_file.path,
                                    Weight.objects.get(name=model_types[i]).mean_std.path)