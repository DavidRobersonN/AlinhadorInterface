#include <AccelStepper.h>

// =====================================
// CONFIGURAÇÕES
// =====================================

// LED interno da placa Arduino
#define LED_PIN 13

// Pinos do driver do motor de passo
#define STEP_PIN 2
#define DIR_PIN 3

// =====================================
// CLASSE MOTOR
// =====================================

class Motor {
  public:
    Motor(int stepPin, int dirPin)
      : _motor(AccelStepper::DRIVER, stepPin, dirPin) {
      _pinoStep = stepPin;
      _pinoDir = dirPin;

      _motor.setMaxSpeed(1000);
    }

    void giraMotor(int sent, int quantidadePassos) {
      int contador = 0;

      _motor.setSpeed(1000 * sent);

      while (contador < quantidadePassos) {
        if (_motor.runSpeed()) {
          contador++;
        }
      }
    }

    void darUmPasso(int sent) {
      _motor.setSpeed(1000 * sent);

      while (!_motor.runSpeed()) {
        // espera até executar 1 passo
      }
    }

  private:
    int _pinoStep;
    int _pinoDir;
    AccelStepper _motor;
};

// =====================================
// OBJETOS
// =====================================

Motor motor(STEP_PIN, DIR_PIN);

// Guarda o estado atual do LED
bool ledLigado = false;

// =====================================
// FUNÇÕES DO LED
// =====================================

void atualizarLed(bool estado) {
  ledLigado = estado;
  digitalWrite(LED_PIN, ledLigado ? HIGH : LOW);
}

void enviarStatusLed() {
  if (ledLigado) {
    Serial.println("LED_ON");
  } else {
    Serial.println("LED_OFF");
  }
}

void processarComandoLed(String comando) {
  comando.trim();

  if (comando == "LED_ON") {
    atualizarLed(true);
    enviarStatusLed();
    return;
  }

  if (comando == "LED_OFF") {
    atualizarLed(false);
    enviarStatusLed();
    return;
  }

  if (comando == "LED_TOGGLE") {
    atualizarLed(!ledLigado);
    enviarStatusLed();
    return;
  }

  if (comando == "LED_STATUS") {
    enviarStatusLed();
    return;
  }

  Serial.println("ERRO_LED_COMANDO_INVALIDO");
}

// =====================================
// FUNÇÕES DO MOTOR
// =====================================

void processarComandoMotor(String comando) {
  comando.trim();

  // Espera algo como:
  // MOTOR|1|800
  // MOTOR|-1|400

  int primeiroSeparador = comando.indexOf('|');
  int segundoSeparador = comando.indexOf('|', primeiroSeparador + 1);

  if (primeiroSeparador == -1 || segundoSeparador == -1) {
    Serial.println("ERRO_FORMATO_MOTOR_INVALIDO");
    return;
  }

  String sentidoStr = comando.substring(primeiroSeparador + 1, segundoSeparador);
  String passosStr = comando.substring(segundoSeparador + 1);

  int sentido = sentidoStr.toInt();
  int passos = passosStr.toInt();

  if (sentido != 1 && sentido != -1) {
    Serial.println("ERRO_SENTIDO_INVALIDO");
    return;
  }

  if (passos <= 0) {
    Serial.println("ERRO_PASSOS_INVALIDOS");
    return;
  }

  motor.giraMotor(sentido, passos);

  Serial.println("OK_MOTOR_FINALIZADO");
}

// =====================================
// PROCESSADOR GERAL
// =====================================

void processarComando(String comando) {
  comando.trim();

  if (comando.startsWith("LED")) {
    processarComandoLed(comando);
    return;
  }

  if (comando.startsWith("MOTOR")) {
    processarComandoMotor(comando);
    return;
  }

  Serial.println("ERRO_COMANDO_DESCONHECIDO");
}

// =====================================
// SETUP
// =====================================

void setup() {
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);
  atualizarLed(false);

  Serial.println("ARDUINO_PRONTO");
  enviarStatusLed();
}

// =====================================
// LOOP
// =====================================

void loop() {
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    processarComando(comando);
  }
}