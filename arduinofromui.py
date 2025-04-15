# When the "Start Measurement" button is clicked, the UI sends "START\n" over Serial.

#It then waits ~3 seconds and checks ThingSpeak to see if a new value has been posted to field1 of channel (2877004).

#If it finds a value, it shows a graph of the sensor readings over time

#code to add to arduino: 
if (Serial.available()) {
  String input = Serial.readStringUntil('\n');
  if (input == "START") {
    // Begin sensor reading and data upload process
  }
}

