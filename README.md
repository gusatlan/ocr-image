# Serviço de leitura de hidrômetro (ocr-image)

@since 2024-12-12

@author gustavooliveira

## Objetivo

Realizar a leitura de hidrômetro de forma remota e automática.


## Requisito


O serviço deve ligar a câmera e a luz utilizando um tópico mqtt, nesse tópico um microcontrolador ESP32 aguardo os comandos de ligar e desligar.

Após a luz e a camera wifi ligadas e operacional:

* Captura a imagem da câmera através do ffmpeg;
* Recorta a imagem, excluíndo a data e hora do topo da imagem;
* Através do Gemini é extraído o consumo de água;
* Envia o consumo através de tópico MQTT;
* Desliga a câmera e luz através de tópico MQTT para o ESP32;
* Excluí as imagens capturadas.

O serviço repete essa tarefa, em tempo pré determinado (360 minutos).


Utilizando node-red, o consumo de água é lido através do tópico correspondente MQTT e por fim é salvo em banco de dados PostgreSQL.



