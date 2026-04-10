from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import machine.routing

# Este arquivo centraliza as rotas WebSocket do projeto inteiro.
# Se amanhã você criar mais apps com WebSocket, pode adicionar aqui.

application = ProtocolTypeRouter({
    # Tudo que for conexão WebSocket passa por aqui
    "websocket": AuthMiddlewareStack(
        URLRouter(
            machine.routing.websocket_urlpatterns
        )
    ),
})