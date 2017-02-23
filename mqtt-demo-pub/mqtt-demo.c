#include "stdio.h"
#include "contiki.h"
#include "contiki-net.h"
#include "mqtt-service.h"
/*---------------------------------------------------------------------------*/
PROCESS(mqtt_client_process, "MQTT Publishing Example");
AUTOSTART_PROCESSES(&mqtt_client_process);
/*---------------------------------------------------------------------------*/

PROCESS_THREAD(mqtt_client_process, ev, data)
{
    static uip_ip6addr_t server_address;
 
    // Allocate buffer space for the MQTT client
    static uint8_t in_buffer[64];
    static uint8_t out_buffer[64];
 
  static struct etimer et;
    // Setup an mqtt_connect_info_t structure to describe
    // how the connection should behave
    static mqtt_connect_info_t connect_info =
    {
        .client_id = "pclient",
        .username = NULL,
        .password = NULL,
        .will_topic = NULL,
        .will_message = NULL,
        .keepalive = 60,
        .will_qos = 0,
        .will_retain = 0,
        .clean_session = 0
    };
 
 
    PROCESS_BEGIN();
    // Set the server address
    uip_ip6addr(&server_address,
                0xbbbb, 0, 0, 0, 0xa, 0xbff, 0xfe0c, 0xd0e);
 
    // Initialise the MQTT client
    mqtt_init(in_buffer, sizeof(in_buffer),
              out_buffer, sizeof(out_buffer));
 
    // Ask the client to connect to the server
    // and wait for it to complete.
    mqtt_connect(&server_address, UIP_HTONS(1883),
                 1, &connect_info);
 
    etimer_set(&et, CLOCK_SECOND * 60);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
    if(mqtt_connected())
    {

        printf("Connected");
        while(1)
        {
 
                const char* topic1 = "localgateway_to_awsiot";
                const char* message1 = "{\"key\": \"helloFromcooja\"}";
                int level = 0;
 
                printf("%s = %s\n", topic1, message1);
 
                etimer_set(&et, CLOCK_SECOND * 60);
                // Relay the received message to a new topic
                mqtt_publish(topic1, message1, 0, 1);
                PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
                etimer_reset(&et);

        }
    }
    else
        printf("mqtt service connect failed\n");
    PROCESS_END();
}
