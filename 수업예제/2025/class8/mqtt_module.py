import paho.mqtt.client as mqtt
import json
import queue
import uuid
class MQTTClient:
    def __init__(self,islocal = False):
        # 새로운 클라이언트 생성
        client_id = str(uuid.uuid4())  # 고유한 클라이언트 ID 생성
        self.client = mqtt.Client(client_id=client_id) # 고유한 클라이언트 ID 설정
        self.Mqtt_Connection = False
        self.islocal = islocal
        self.State = None
        self.friend = {}
        
    def get_State_message(self):
        return self.State
        
    def mqtt_connecting(self):
        return self.Mqtt_Connection

    def update_friend(self,friend):
        self.friend = friend
        
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("on_connect")
            self.Mqtt_Connection = True
        else:
            self.Mqtt_Connection = False

    def on_disconnect(self,client, userdata, flags, rc=0):
        print("disconnect_MQTT = ",rc)
        pass
    
    def on_publish(self,client, userdata, mid):
        print("In on_pub callback mid= ", mid)
        
    def on_subscribe(self,client, userdata, mid, granted_qos):
        #print("subscribed: " + str(mid) + " " + str(granted_qos))
        pass    
    
    def on_message(self,client,userdata,msg):
        str_msg = msg.payload.decode("utf-8")
        if msg.topic == "Event/State/" :
            self.State = json.loads(str_msg)
        for friend in self.friend:
            if msg.topic == f"Event/Chat/{friend}" :
                self.State = json.loads(str_msg)
            
    def msg(self,topics,message):
        self.client.publish(topics,message, 1) #Event/T-MDS/YJSensing/
    
    def subscribe(self,subscribe):
        self.client.subscribe(subscribe) #
    
    def unsubscribe(self, subscribe):
        self.client.unsubscribe(subscribe)  # 특정 토픽에 대한 구독 해제
                
    def connecting(self):
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.username_pw_set('ari_mqtt', "25846ec82")
        self.client.connect('211.169.215.170', 53200, keepalive=120)
    
    def localconnect(self):
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.username_pw_set('admin', "solimatics")
        self.client.connect('localhost', 53200, keepalive=120)
        
    def loop_start(self):
        self.client.loop_start()
    
    def loop_forever(self): 
        self.client.loop_forever()
        
    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
    