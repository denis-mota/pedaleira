neste projeto estou aprendendo a criar uma pedaleira digital em python, os desafios são muito grandes porque não sei muito da linguagem em python estou usando inteligencia artificial para me ajudar ne projeto.
para executar esse projeto você precisar ter o python instalado em sua maquina.

dependencias:

customtkinter,
sounddevicer,
scipy

Se voce estiver no linux para instalar as dependencias precisa primeira esta no ambiente virtual do python: 



( source .venv/bin/activate ) # Linux/macOS

( .venv\Scripts\activate )    # Windows


para instalar virtualização do python:

( sudo apt install python3-venv -y )


para criar o ambiente virtual:

( python3 -m venv .venv )


para ativar ambiente virtual:

source .venv/bin/activate
###############################################################################################################################################################

resolvendo o problema do flet com libmpv.so.1 no linux

no terminal use
apt install libmpv-dev mpv 

depois que terminar execute esse tambem
ln -s /usr/lib/x86_64-linux-gnu/libmpv.so  /usr/lib/libmpv.so.1 
