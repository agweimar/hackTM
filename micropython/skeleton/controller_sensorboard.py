import controller_esp
import config_sensorboard
import display_basic

import machine
import zlib

import SGP30, SHTC1

class Controller(controller_esp.Controller, display_basic.Display):

    # Sensorboard config
    PAYLOAD_VERSION=2
    QOS=0

    PIN_NO_I2C_SCL = 22
    PIN_NO_I2C_SDA = 21
    FREQ_I2C = 10000


    #WIFI_IP        = '192.168.0.151'
    #WIFI_SUBNET    = '255.255.255.0'
    #WIFI_GATEWAY   = '192.168.0.1'
    #WIFI_DNS       = '84.200.69.80'
    #WIFI_SSID      = ""
    #WIFI_PASSWORD  =  ""

    # LoRa config
    PIN_ID_FOR_LORA_RESET = 14
    
    PIN_ID_FOR_LORA_SS = 18
    PIN_ID_SCK = 5
    PIN_ID_MOSI = 27
    PIN_ID_MISO = 19
    
    PIN_ID_FOR_LORA_DIO0 = 26
    PIN_ID_FOR_LORA_DIO1 = None 
    PIN_ID_FOR_LORA_DIO2 = None 
    PIN_ID_FOR_LORA_DIO3 = None
    PIN_ID_FOR_LORA_DIO4 = None
    PIN_ID_FOR_LORA_DIO5 = None 
    
    
    # OLED config
    PIN_ID_FOR_OLED_RESET = 16
    PIN_ID_SDA = 4
    PIN_ID_SCL = 15
    OLED_I2C_ADDR = 0x3C    
    OLED_I2C_FREQ = 400000
    OLED_WIDTH = 128
    OLED_HEIGHT = 32
    
    
    # ESP config
    ON_BOARD_LED_PIN_NO = 15
    ON_BOARD_LED_HIGH_IS_ON = False
    GPIO_PINS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                 12, 13, 14, 15, 16, 17, 18, 19, 21, 22,
                 23, 25, 26, 27, 32, 34, 35, 36, 37, 38, 39) 
                 
    
    def __init__(self, 
                 pin_id_led = ON_BOARD_LED_PIN_NO, 
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = PIN_ID_FOR_LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5),
                 oled_width = OLED_WIDTH, oled_height = OLED_HEIGHT, 
                 scl_pin_id = PIN_ID_SCL, sda_pin_id = PIN_ID_SDA, 
                 freq = OLED_I2C_FREQ):
                 
        controller_esp.Controller.__init__(self,
                                           pin_id_led,
                                           on_board_led_high_is_on,
                                           pin_id_reset,
                                           blink_on_start)
                                           
        self.reset_pin(self.prepare_pin(self.PIN_ID_FOR_OLED_RESET))        
        display_basic.Display.__init__(self, 
                                             width = oled_width, height = oled_height, 
                                             scl_pin_id = scl_pin_id, sda_pin_id = sda_pin_id, 
                                             freq = freq)                                             
        # init i2c with sensirion sensors
        self.i2c = machine.I2C(1,scl = machine.Pin(self.PIN_NO_I2C_SCL), sda = machine.Pin(self.PIN_NO_I2C_SDA), freq = self.FREQ_I2C)

        self.sgp = SGP30.SGP30_Sensor(self.i2c)
        self.shtc = SHTC1.SHTC1_Sensor(self.i2c)
        #send sgp to sleep
        self.sgp.soft_reset()
        
    def add_transceiver(self, 
                        transceiver, 
                        pin_id_ss = PIN_ID_FOR_LORA_SS,
                        pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
                        pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
                        pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
                        pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,     
                        pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
                        pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5):
         
        transceiver.show_text = self.show_text
        transceiver.show_packet = self.show_packet
        
        return super().add_transceiver(transceiver, 
                                       pin_id_ss,
                                       pin_id_RxDone,
                                       pin_id_RxTimeout,
                                       pin_id_ValidHeader,
                                       pin_id_CadDone,
                                       pin_id_CadDetected,
                                       pin_id_PayloadCrcError) 
                                       
                                       
    def show_packet(self, payload_string, rssi = None):
        self.clear()
        line_idx = 0
        if rssi:
            self.show_text('RSSI: {}'.format(rssi), x = 0, y = line_idx * 10, clear_first = False, show_now = False)
            line_idx += 1        
        self.show_text_wrap(payload_string, start_line = line_idx, clear_first = False)


    def collect_data(self):
        print("Reading sensors")
        self.sgp.iaq_init()
        sgp_data = self.sgp.get_data()
        shtc_data = self.shtc.get_data()

        # send sgp to sleep
        self.sgp.soft_reset()
        
        data = sgp_data
        data.update(shtc_data)
        print("sensirion raw sensor data: {0}".format(data))
    
        return data

    def assemble_payload(self, data):
    
        data.update({'mac': config_sensorboard.UUID})
        data.update({'payload_version': self.PAYLOAD_VERSION})
        #data.update({'QoS': QOS})
        #data.update({'scenario_code': scenario_code})
        
        payload = ",".join(str(i) for i in [
                    data['mac'],
                    data['payload_version'],
                    #data['QoS'],
                    #data['scenario_code'],
                    round(data['T'], 1),
                    round(data['RH'], 1),
                    data['SGP30_CO2EQ'],
                    data['SGP30_TVOC'],
                    data['SGP30_ETOH_RAW'],
                    data['SGP30_H2_RAW']
                    ])

        return payload
        #return payload.decode()

    def lora_send(self, lora, payload):
    
        print("LoRa Sender:")
        print("Sending packet: \n{}\n".format(payload))
    
        lora.println(payload) 

#    def wifi_connect(self):
#        import network
#        
#        station = network.WLAN(network.STA_IF)
#     
#        if station.isconnected() == True:
#            print("Already connected")
#            return
#     
#        station.active(True)
#        #station.ifconfig((WIFI_IP,WIFI_SUBNET,WIFI_GATEWAY,WIFI_DNS))
#        station.connect(WIFI_SSID, WIFI_PASSWORD)
#     
#        while station.isconnected() == False:
#            pass
#     
#        print("Connection successful")
#        print(station.ifconfig())
#    
#    def wifi_disconnect(self):
#        import network
#        station = network.WLAN(network.STA_IF)
#        station.disconnect()
#        station.active(False)
            
