#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219_1;
Adafruit_INA219 ina219_2(0x41);
Adafruit_INA219 ina219_3(0x44);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    // Wait for serial connection
  }

  Wire.begin();

  ina219_1.begin();
  ina219_1.setCalibration_32V_2A();
  
  ina219_2.begin();
  ina219_2.setCalibration_32V_2A();

  ina219_3.begin();
  ina219_3.setCalibration_32V_2A();
}

void loop() {
  float busVoltage1 = ina219_1.getBusVoltage_V();
  float current1 = ina219_1.getCurrent_mA();
  float power1 = ina219_1.getPower_mW();

  float busVoltage2 = ina219_2.getBusVoltage_V();
  float current2 = ina219_2.getCurrent_mA();
  float power2 = ina219_2.getPower_mW();

  float busVoltage3 = ina219_3.getBusVoltage_V();
  float current3 = ina219_3.getCurrent_mA();
  float power3 = ina219_3.getPower_mW();

  Serial.print(power1);
  Serial.print(",");
  Serial.print(power2);
  Serial.print(",");
  Serial.println(power3);

  delay(3000);
}
