import paho.mqtt.client as mqtt
import requests


def on_message(client, userdata, message):
    global API_URL
    splited = message.topic.split("/")
    origin = splited[0]
    destination = splited[1]
    command = splited[2]

    if command == "storePosition":
        print("Store new position")
        # get the new position coming from the autopilot controller
        position_str = str(message.payload.decode("utf-8"))
        position = position_str.split("*")
        # send the position to the API
        requests.post(API_URL, json={"lat": position[0], "lon": position[1]})

    if command == "getStoredPositions":
        print("get stored positions")
        # get the stored positions from the API
        r = requests.get(API_URL)
        # jsonData = r.json()
        # convert the request to string
        data_string = r.text
        # send answer to subscribed clients (by the moment, only dashboard)
        client.publish("dataService/" + origin + "/storedPositions", data_string)


def DataService(external_broker, username, password):
    global API_URL
    API_URL = "http://localhost:4000/data"
    print("External broker: ", external_broker)
    client = mqtt.Client("Data service", transport="websockets")
    external_broker_address = external_broker
    external_broker_port = 8000
    if external_broker_address == "classpip.upc.edu":
        client.username_pw_set(username, password)

    client.on_message = on_message
    client.connect(external_broker_address, external_broker_port)

    # By the moment, the data service only can store positions (sent by the autopilot service)
    # and provide the stored positions
    client.subscribe("autopilotService/dataService/storePosition")
    client.subscribe("+/dataService/getStoredPositions")
    print("Waiting commands")

    client.loop_forever()


if __name__ == "__main__":
    import sys

    username = None
    password = None
    external_broker = sys.argv[1]
    if external_broker == "classpip.upc.edu":
        username = sys.argv[2]
        password = sys.argv[3]

    DataService(external_broker, username, password)
